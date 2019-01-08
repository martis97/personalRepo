import getpass
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

class FBBot(object):

    def __init__(self):  
        self.browser = None  
        self.timeout = 60
        self.url = "https://www.facebook.com/"
        self.username = input("Enter username: ")
        self.password = input(getpass.getpass \
                ("Enter password for %s : " % self.username))

    def create_browser(self, notifications_off=True):  
        """Creates a Webdriver instance of Chrome to drive the automation.
        
        Args:
            Notification_actions: (Default: True) Boolean value if browser 
                required with notifications off. FB requires access to 
                notifications when first time accessed.
        Returns:
            browser: Webdriver element used to drive automation.
        """
        if notifications_off: 
            chrome_options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications" : 2}
            chrome_options.add_experimental_option("prefs",prefs)
            self.browser = webdriver.Chrome(chrome_options=chrome_options)
            return self.browser
        else:
            self.browser = webdriver.Chrome()
            return self.browser

    def navigate_to_url(self):
        """ Makes the browser window fullscreen and navigates to the web page
            TODO: Parameterise the target URL
        """

        self.browser.fullscreen_window()
        self.browser.get(self.url)

    def login_process(self, password):
        """Enters username and password to the respective fields and
        presses 'Log in'

        Exceptions:
            TimeoutException: Will look for the 'Incorrect Credentials'
            error message - if this message is not displayed within 4 seconds,
            it will carry on executing the rest of the script
            
        TODO: Import WaitFor module from WSAuthTest
        """

        email_entry = WebDriverWait(self.browser, self.timeout) \
            .until(EC.presence_of_element_located((By.ID, "email")))   # This will

        email_entry.send_keys(self.username)

        password_entry = WebDriverWait(self.browser, self.timeout) \
            .until(EC.presence_of_element_located((By.ID, "pass")))    # be replaced with

        password_entry.send_keys(password)

        login_btn = WebDriverWait(self.browser, self.timeout) \
            .until(EC.element_to_be_clickable((By.ID, "loginbutton"))) # WaitFor module

        login_btn.click()                                              # for cleaner code

        try:
            WebDriverWait(self.browser, 4) \
                .until(EC.visibility_of_element_located \
                ((By.CLASS_NAME, "_4rbf")))

            incorrectCredsElement = self.browser.find_element_by_class_name("_4rbf")

            if incorrectCredsElement.is_displayed():
                print("Incorrect credentials have been entered!")
                self.browser.quit()

        except TimeoutException:
            pass

    def enter_to_search(self,search_value):
        
        """ Looks for a Facebook using a search bar.

            Exceptions:
                WebDriverException - will re-enter the search value if the 
                    exception is raised.  
        """

        while not WebDriverException:
            search_bar_element = '//input[@placeholder = "Search"]'
            WebDriverWait(self.browser, 4) \
                .until(EC.visibility_of_element_located \
                ((By.XPATH, search_bar_element))) # Again needs WaitFor

            search_bar = self.browser.find_element_by_xpath(search_bar_element)
            return search_bar.send_keys(search_value)
        
        self.enter_to_search(search_value)

    def press_search(self):
        """ Initiating the search by pressing the 'Search' button """

        search_btn = WebDriverWait(self.browser, self.timeout) \
            .until(EC.element_to_be_clickable((By.CLASS_NAME, "_585_"))) # And again

        search_btn.click()


    def select_page(self,number):
        """Selects the search result"""

        WebDriverWait(self.browser, self.timeout) \
            .until(EC.element_to_be_clickable \
            ((By.LINK_TEXT, "Dank Memes"))) # And again lol

        available_pages = self.browser.find_elements_by_class_name("_52eh")
        available_pages[number].click()

    def press_like(self, posts_to_like): 
        """ Likes the last 30 posts on the timeline 
            It will first unlike any posts that have been liked already

            Exceptions:
                TimeoutException - Will look for liked posts for 3 seconds 
                upon timeout, it will continue running the script
        """

        liked_xpath = '//a[@aria-pressed = "true"]'
        not_liked_xpath = '//a[@aria-pressed = "false"]'
        post_like = 'fb-ufi-likelink'
        random_wait = random.uniform(1, 1.99)

        try:
            WebDriverWait(self.browser, 3) \
                .until(EC.element_to_be_clickable((By.XPATH, liked_xpath)))

            liked_btns = self.browser.find_elements_by_xpath(liked_xpath)
            
            print("Unliking pages that have been already liked...")
            for like_button in liked_btns:
                if like_button.get_attribute("data-testid") == post_like:
                    like_button.click()
                    time.sleep(random_wait)
                else:
                    continue

        except TimeoutException: 
            print("No liked posts found")

        
        WebDriverWait(self.browser, self.timeout) \
            .until(EC.element_to_be_clickable((By.XPATH, not_liked_xpath)))

        liked_posts = 0
        not_liked_btns = self.browser.find_elements_by_xpath(not_liked_xpath)

        for like_button in not_liked_btns:
            if like_button.get_attribute("data-testid") == post_like:
                like_button.click()
                time.sleep(random_wait)
                liked_posts += 1
            else:
                continue

            if liked_posts == posts_to_like:
                print("%d most recent posts have been liked" % posts_to_like)
                break

def mr_robot():
    """Function call and parameter definition"""

    # Param definitions
    search_value = "Crazy Programmer"


    # Class instance
    fb = FBBot()

    # Orchestra
    fb.create_browser()
    fb.navigate_to_url()
    fb.login_process()
    fb.enter_to_search()
    fb.press_search()
    fb.select_page(page_number)
    fb.press_like(25)
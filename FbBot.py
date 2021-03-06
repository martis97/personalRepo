# Selenium Webdriver
from selenium import webdriver

# Selenium Exceptions
from selenium.common.exceptions import NoSuchElementException,\
    TimeoutException, WebDriverException

# Selenium Explicit wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ExplicitWait
from FbBot.ExplicitWait import ExplicitWait

# Misc.
import getpass
import time
import random


class FBBot(object):
    """Facebook bot class defining actions required to log in to Facebook,
    find a page and like the first 30 (default amount) posts on the timeline.

    Attributes:
        browser: Webdriver instance of Chrome used to drive automation.
        timeout: Amount of seconds the WebDriver will wait for a 
            specified condition.
        url: Facebook URL 
        email: Email used to log in to Facebook
        password: Password used to authenticate the user
        Wait: Instance of ExcplicitWait class
    """

    def __init__(self, email, password):
        """Class initialisation."""

        self.browser = self.create_browser()
        self.timeout = 60
        self.url = "https://www.facebook.com/"
        self.email = email
        self.password = password
        self.Wait = ExplicitWait(self.browser, self.timeout)

    def create_browser(self, notifications_off=True):  
        """Creates a Webdriver instance of Chrome to drive the automation.
        
        Args:
            notifications_off: (Default: True) Boolean value if browser 
                required with notifications off. FB requests access to 
                notifications upon a first user's visit to the website.

        Returns:
            browser: Webdriver instance of Chrome used to drive automation.
                Set to be fullscreen.
        TODO: Add more Chrome settings 
        """

        if notifications_off: 
            # Changing settings to disable notifications
            chrome_options = webdriver.ChromeOptions()
            prefs =  \
                {"profile.default_content_setting_values.notifications" : 2}
            chrome_options.add_experimental_option("prefs",prefs)
            self.browser = webdriver.Chrome(chrome_options=chrome_options)

            return self.browser.fullscreen_window()
            
        else:
            self.browser = webdriver.Chrome()
            return self.browser.fullscreen_window()

    def navigate_to_fb(self):
        """Navigates to the web page. """

        self.browser.get(self.url)

    def login(self):
        """Enters email and password to the respective fields and
        presses 'Log in'.
        """

        email_entry = self.Wait.id_visible("email")
        email_entry.send_keys(self.email)

        password_entry = self.Wait.id_visible("pass")
        password_entry.send_keys(self.password)

        login_btn = self.Wait.id_visible("loginbutton")
        login_btn.click()

        try:
            WebDriverWait(self.browser, 4) \
                .until(EC.visibility_of_element_located \
                ((By.CLASS_NAME, "_4rbf")))

            print("Incorrect credentials have been entered!")
            self.browser.quit()

        except TimeoutException:
            pass

    def enter_to_search(self, page_name):
        """Looks for a Facebook using a search bar.
        
        Args:
            page_name: (str) Text to send to the search box.
        """

        search_bar_element = '//input[@placeholder="Search"]'

        WebDriverWait(self.browser, 4) \
            .until(EC.visibility_of_element_located \
                        ((By.XPATH, search_bar_element)))
        
        search_bar = self.browser. \
                        find_element_by_xpath(search_bar_element)
        search_bar.send_keys(page_name)

    def press_search(self):
        """Initiating the search by pressing the 'Search' button."""

        search_btn = self.Wait.class_name_clickable("_585_")
        search_btn.click()

    def select_page_index(self,number):
        """Selects the search result by its position, starting from 0.

        Args:
            number: (int) Order number of available pages. 
                0 for the fist page, 1 for second etc.
        """

        self.Wait.class_name_clickable("_52eh")
        all_pages = self.browser.find_elements_by_class_name("_52eh")
        all_pages[number].click()

    def select_page_name(self, page_name):
        """Selects the search result, given expected page name.

        Args:
            page_name: Name of the page to search for.
        """

        self.Wait.class_name_clickable("_52eh") 
        all_pages = self.browser.find_elements_by_class_name("_52eh")

        for page in all_pages: 
            if page.text == page_name:
                page.click()
            else:
                continue

    def unlike_all_posts(self): 
        """Unlike any posts that have been liked already"""

        liked_xpath = '//a[@aria-pressed = "true"]'

        try:
            WebDriverWait(self.browser, 5) \
                .until(EC.element_to_be_clickable((By.XPATH, liked_xpath)))
            liked_btns = self.browser.find_elements_by_xpath(liked_xpath)

            print("Unliking pages that have been already liked..")
            for like_button in liked_btns:
                if like_button.get_attribute("data-testid") == 'fb-ufi-likelink':
                    like_button.click()
                    time.sleep(float("%.2f" % random.uniform(1, 3)))
                else:
                    continue
        except TimeoutException: 
            print("No liked posts found")
            
    def like_posts(self, posts_to_like): 
        """Likes the last 30 posts on the timeline.

        Args:
            posts_to_like: The amount of posts to like, starting from the
            beginning.
        """

        not_liked_btns_xpath = '//a[@aria-pressed = "false"]'
        self.Wait.xpath_clickable(not_liked_btns_xpath)

        like_count = 0
        not_liked_btns = self.browser.find_elements_by_xpath(not_liked_btns_xpath)
        print(f"Liking the latest {posts_to_like} posts on the timeline")
        for like_button in not_liked_btns:
            if like_count == posts_to_like:
                print(f"{like_count} most recent posts have been liked")
                break
            if like_button.get_attribute("data-testid") == 'fb-ufi-likelink':
                like_button.click()
                time.sleep(float("%.2f" % random.uniform(1, 3)))
                like_count += 1
            else:
                continue
            


def mr_robot(page_name="Crazy Programmer", posts_to_like=25):
    """Function call and parameter definition.
    
    Args:
        page_name: Name of the page to search for. Set default to 
            "Crazy Programmer".
        posts_to_like: The amount of posts to like, starting from the
            beginning.
    """
    
    # Get Credentials
    creds = \
    {
        "email" : input("Enter email: "),
        "password" : getpass.getpass("Enter password : ")
    }

    # Class instance
    fb = FBBot(**creds)

    # Orchestra
    fb.navigate_to_fb()
    fb.login()
    fb.enter_to_search(page_name)
    fb.press_search()
    fb.select_page_name(page_name)
    fb.unlike_all_posts()
    fb.like_posts(posts_to_like)
    fb.browser.quit()

mr_robot()

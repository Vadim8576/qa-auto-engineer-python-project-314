import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from kanban_board_tests.pages.locators.base_locators import BaseLocators

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        self.driver.get(url)
        self.url = url
    
    def get_title(self):
        return self.driver.title
    
    @property
    def current_url(self):
        return self.driver.current_url

    def click(self, locator):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.click()

    def type(self, locator, text):
        el = self.wait.until(EC.visibility_of_element_located(locator))         
        el.send_keys(Keys.CONTROL, 'a')
        el.send_keys(Keys.DELETE)
        el.send_keys(text)
        self.wait.until(lambda driver: el.get_attribute('value') == text)

    def text_of(self, locator):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        return el.text
    
    def value_of(self, locator):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        return el.get_attribute('value')

    def header_text(self):
        return self.text_of(BaseLocators.HEADER)
    
    def get_alert_text(self):
        text = self.text_of(BaseLocators.ALERT)
        self.wait_alert_invisibility()
        return text

    def wait_alert_invisibility(self):
            try:
                self.wait.until(EC.invisibility_of_element_located(BaseLocators.ALERT))
            except TimeoutException:
                pass
            
    def is_element_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_clickable(self, locator):
        try:
            self.wait.until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False
    
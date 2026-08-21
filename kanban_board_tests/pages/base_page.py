from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


import time
import logging

logger = logging.getLogger(__name__)

class BasePage:
    HEADER = (By.ID, 'react-admin-title')
        
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

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
        
        el.send_keys(Keys.CONTROL, "a")
        # time.sleep(1)
        el.send_keys(Keys.DELETE)
        # time.sleep(1)
        el.send_keys(text)
        self.wait.until(lambda driver: el.get_attribute("value") == text)
        # time.sleep(1)
    

    def text_of(self, locator):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        return el.text
    
    def value_of(self, locator):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        return el.get_attribute('value')

    def header_text(self):
        return self.text_of(self.HEADER)
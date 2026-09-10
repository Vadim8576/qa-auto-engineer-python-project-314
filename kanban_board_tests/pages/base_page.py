import logging
import random
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from kanban_board_tests.pages.locators.base_locators import BaseLocators
from kanban_board_tests.pages.locators.table_locators import TableLocators

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
        # el = self.wait.until(EC.element_to_be_clickable(locator))
        el = self.wait.until(EC.presence_of_element_located(locator))
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
    
    def wait_alert_invisibility(self):
        """Ждёт, пока существующий алерт исчезнет (станет невидимым или уйдёт из DOM)."""
        try:
            self.wait.until(EC.invisibility_of_element_located(BaseLocators.ALERT))
        except TimeoutException:
            pass
    
    def get_alert_text(self):
        text = self.text_of(BaseLocators.ALERT)
        self.wait_alert_invisibility()
        return text

    def click_to_create(self):
        self.click(TableLocators.CREATE_BUTTON)
    
    def click_to_delete(self):
        self.click(TableLocators.DELETE_BUTTON)

    def get_random_id(self):
        records = self.table_parse()
        if not records:
            return None
        random_records = random.choice(records)
        return random_records['id']
    
    def table_loads(self):
        try:
            self.wait.until(
                lambda d: [r for r in d.find_elements(*TableLocators.DATA_ROWS) if r.is_displayed()]
            )
            return True
        except TimeoutException:
            return False
    
    def select_all_records(self):        
        table_head = self.wait.until(EC.visibility_of_element_located(TableLocators.TABLE_HEAD))
        head = table_head.find_element(*TableLocators.ROW)
        checkbox = head.find_element(*TableLocators.CHECKBOX)
        checkbox.click()

    def click_to_dropdown(self, selector):
        trigger = self.driver.find_element(*selector)

        self.wait.until(lambda d: trigger.is_displayed() and trigger.is_enabled())
        try:
            trigger.click()
        except Exception:
            self.driver.execute_script('arguments[0].click();', trigger)
        # time.sleep(1)           
        
    
    def click_to_option(self, option_text):
        
        option = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//li[normalize-space()='{option_text}']"))
        )
        option.click()  
        # time.sleep(1)
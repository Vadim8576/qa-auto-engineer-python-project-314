from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.base_page import BasePage


import logging

import re

import time


logger = logging.getLogger(__name__)

class EditUserPage(BasePage):  
    EMAIL = (By.CSS_SELECTOR, 'input[name="email"]')
    ALERT = (By.CSS_SELECTOR, 'div[role="alert"] div[class*="message"]')
    FIRST_NAME = (By.CSS_SELECTOR, 'input[name="firstName"]')
    LAST_NAME = (By.CSS_SELECTOR, 'input[name="lastName"]')
    SAVE = (By.CSS_SELECTOR, 'button[type="submit"]')
    
    def is_opened(self, user_id):
        return f'/users/{user_id}' in self.current_url
    
    def get_user_data_from_form(self):
        email = self.value_of(self.EMAIL)
        first_name = self.value_of(self.FIRST_NAME)
        last_name = self.value_of(self.LAST_NAME)
        return {
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        }
        
    def set_user_email(self, email):
        self.type(self.EMAIL, email)
    
    def set_user_first_name(self, first_name):
        self.type(self.FIRST_NAME, first_name)
    
    def set_user_last_name(self, last_name):
        self.type(self.LAST_NAME, last_name)
    
    def click_save(self):
        self.click(self.SAVE)
        
    def set_user_data(self, new_user_data):
        self.set_user_email(new_user_data['email'])
        self.set_user_first_name(new_user_data['first_name'])
        self.set_user_last_name(new_user_data['last_name'])
        # time.sleep(1)
        self.click_save()
    
    def wait_alert_invisibility(self):
        """Ждёт, пока существующий алерт исчезнет (станет невидимым или уйдёт из DOM)."""
        try:
            self.wait.until(EC.invisibility_of_element_located(self.ALERT))
        except Exception:
            pass
    
    def is_email_incorrect(self):
        # self.wait_alert_disappear()
        try:           
            text = self.text_of(self.ALERT)
            self.wait_alert_invisibility()
            return 'The form is not valid' in text
        except Exception:
            return False
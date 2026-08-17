
from selenium.webdriver.common.by import By

from kanban_board_tests.pages.base_page import BasePage


class UserCreationPage(BasePage):
    EMAIL = (By.CSS_SELECTOR, 'input[name="email"]')
    FIRST_NAME = (By.CSS_SELECTOR, 'input[name="firstName"]')
    LAST_NAME = (By.CSS_SELECTOR, 'input[name="lastName"]')
    SAVE_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Save"]')
    
    def is_opened(self):
        return '/users/create' in self.current_url

    def type_email(self, email):
        self.type(self.EMAIL, email)
    
    def type_first_name(self, first_name):
        self.type(self.FIRST_NAME, first_name)
    
    def type_last_name(self, last_name):
        self.type(self.LAST_NAME, last_name)
        
    def save_user(self):
        self.click(self.SAVE_BUTTON)

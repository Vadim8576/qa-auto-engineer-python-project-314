
from selenium.webdriver.common.by import By

from kanban_board_tests.pages.base_page import BasePage


class UserCreationPage(BasePage):
    EMAIL = (By.CSS_SELECTOR, 'input[name="email"]')
    FIRST_NAME = (By.CSS_SELECTOR, 'input[name="firstName"]')
    LAST_NAME = (By.CSS_SELECTOR, 'input[name="lastName"]')
    SAVE_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Save"]')
    
    def is_opened(self):
        return '/users/create' in self.current_url
        
    def create(self, user_data):
        self.type(self.EMAIL, user_data['email'])
        self.type(self.FIRST_NAME, user_data['first_name'])
        self.type(self.LAST_NAME, user_data['last_name'])
        self.click(self.SAVE_BUTTON)
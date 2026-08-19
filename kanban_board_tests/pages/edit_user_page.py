from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.base_page import BasePage


class EditUserPage(BasePage):  
    EMAIL = (By.CSS_SELECTOR, 'input[name="email"]')
    FIRST_NAME = (By.CSS_SELECTOR, 'input[name="firstName"]')
    LAST_NAME = (By.CSS_SELECTOR, 'input[name="lastName"]')
    SAVE = (By.CSS_SELECTOR, 'button[aria-label="Save"]')
    
    def is_opened(self, user_id):
        return f'/users/{user_id}' in self.current_url
    
    def get_editing_user_data(self):
        email = self.value_of(self.EMAIL)
        first_name = self.value_of(self.FIRST_NAME)
        last_name = self.value_of(self.LAST_NAME)
        return {
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        }
        



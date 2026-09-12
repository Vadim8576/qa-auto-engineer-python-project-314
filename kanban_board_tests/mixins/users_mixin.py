from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.locators.users_locators import (
    UserLocators,
)


class UsersMixin:
    def set_user_email(self, email):
        self.type(UserLocators.EMAIL, email)
    
    def set_user_first_name(self, first_name):
        self.type(UserLocators.FIRST_NAME, first_name)
    
    def set_user_last_name(self, last_name):
        self.type(UserLocators.LAST_NAME, last_name)
        
    def set_user_data(self, user_data):
        self.set_user_email(user_data['email'])
        self.set_user_first_name(user_data['first_name'])
        self.set_user_last_name(user_data['last_name'])
        self.click_save()
import logging

from selenium.common.exceptions import TimeoutException

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.table_locators import TableLocators
from kanban_board_tests.pages.locators.user_locators import UserLocators

logger = logging.getLogger(__name__)

class EditUserPage(BasePage):
    def is_opened(self, user_id):
        return f'/users/{user_id}' in self.current_url
    
    def get_user_data_from_form(self):
        email = self.value_of(UserLocators.EMAIL)
        first_name = self.value_of(UserLocators.FIRST_NAME)
        last_name = self.value_of(UserLocators.LAST_NAME)
        return {
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        }
        
    def set_user_email(self, email):
        self.type(UserLocators.EMAIL, email)
    
    def set_user_first_name(self, first_name):
        self.type(UserLocators.FIRST_NAME, first_name)
    
    def set_user_last_name(self, last_name):
        self.type(UserLocators.LAST_NAME, last_name)
        
    def set_user_data(self, new_user_data):
        self.set_user_email(new_user_data['email'])
        self.set_user_first_name(new_user_data['first_name'])
        self.set_user_last_name(new_user_data['last_name'])
        self.click_save()
    
    def is_email_incorrect(self):
        try:           
            text = self.get_alert_text()
            return 'The form is not valid' in text
        except TimeoutException:
            return False
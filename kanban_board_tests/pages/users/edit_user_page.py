import logging

from selenium.common.exceptions import TimeoutException

from kanban_board_tests.mixins.buttons_mixin import ButtonsMixin
from kanban_board_tests.mixins.table_mixin import TableMixin
from kanban_board_tests.mixins.users_mixin import UsersMixin
from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.users_locators import UserLocators

logger = logging.getLogger(__name__)

class EditUserPage(BasePage, UsersMixin, TableMixin, ButtonsMixin):
    PATH = '/users'
    def is_opened(self, user_id):
        return f'{self.PATH}/{user_id}' in self.current_url
    
    def get_user_data_from_form(self):
        email = self.value_of(UserLocators.EMAIL).strip()
        first_name = self.value_of(UserLocators.FIRST_NAME).strip()
        last_name = self.value_of(UserLocators.LAST_NAME).strip()
        return {
            'email': self.normalize_text(email),
            'first_name': self.normalize_text(first_name),
            'last_name': self.normalize_text(last_name)
        }
        
    def is_email_incorrect(self):
        try:           
            text = self.get_alert_text()
            return 'The form is not valid' in text
        except TimeoutException:
            return False
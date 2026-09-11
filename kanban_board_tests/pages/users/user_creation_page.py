

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.mixins.users_mixin import UsersMixin
from kanban_board_tests.mixins.table_mixin import TableMixin

class UserCreationPage(BasePage, UsersMixin, TableMixin):
    def is_opened(self):
        return '/users/create' in self.current_url
        
    # def create(self, user_data):
    #     self.type(UserLocators.EMAIL, user_data['email'])
    #     self.type(UserLocators.FIRST_NAME, user_data['first_name'])
    #     self.type(UserLocators.LAST_NAME, user_data['last_name'])
    #     self.click(TableLocators.SAVE_BUTTON)
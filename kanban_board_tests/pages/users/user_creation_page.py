from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.mixins.users_mixin import UsersMixin

class UserCreationPage(BasePage, UsersMixin):
    PATH = '/users/create'
    def is_opened(self):
        return self.PATH in self.current_url
        
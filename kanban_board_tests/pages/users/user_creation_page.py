from kanban_board_tests.mixins.buttons_mixin import ButtonsMixin
from kanban_board_tests.mixins.table_mixin import TableMixin
from kanban_board_tests.mixins.users_mixin import UsersMixin
from kanban_board_tests.pages.base_page import BasePage


class UserCreationPage(BasePage, UsersMixin, TableMixin, ButtonsMixin):
    PATH = '/users/create'
    def is_opened(self):
        return self.PATH in self.current_url
        
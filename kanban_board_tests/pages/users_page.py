
from kanban_board_tests.pages.base_page import BasePage


class UsersPage(BasePage):

    def is_opened(self):
        return '/users' in self.current_url

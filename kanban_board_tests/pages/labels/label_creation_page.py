from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.mixins.labels_mixin import LabelsMixin


class LabelCreationPage(BasePage, LabelsMixin):
    def is_opened(self):
        return '/labels/create' in self.current_url
        
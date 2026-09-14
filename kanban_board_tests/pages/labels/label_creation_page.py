from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.mixins.labels_mixin import LabelsMixin
from kanban_board_tests.mixins.table_mixin import TableMixin


class LabelCreationPage(BasePage, LabelsMixin, TableMixin):
    def is_opened(self):
        return '/labels/create' in self.current_url
        
from kanban_board_tests.mixins.buttons_mixin import ButtonsMixin
from kanban_board_tests.mixins.labels_mixin import LabelsMixin
from kanban_board_tests.mixins.table_mixin import TableMixin
from kanban_board_tests.pages.base_page import BasePage


class LabelCreationPage(BasePage, LabelsMixin, TableMixin, ButtonsMixin):
    def is_opened(self):
        return '/labels/create' in self.current_url
        
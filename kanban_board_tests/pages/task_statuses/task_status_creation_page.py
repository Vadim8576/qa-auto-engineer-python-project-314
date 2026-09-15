from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.mixins.task_statuses_mixin import TaskStatusesMixin
from kanban_board_tests.mixins.table_mixin import TableMixin
from kanban_board_tests.mixins.buttons_mixin import ButtonsMixin


class TaskStatusCreationPage(BasePage, TaskStatusesMixin, TableMixin, ButtonsMixin):
    PATH = '/task_statuses/create'
    def is_opened(self):
        return self.PATH in self.current_url
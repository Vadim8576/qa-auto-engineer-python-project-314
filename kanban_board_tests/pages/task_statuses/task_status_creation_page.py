from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.mixins.task_statuses_mixin import TaskStatusesMixin


class TaskStatusCreationPage(BasePage, TaskStatusesMixin):
    PATH = '/task_statuses/create'
    def is_opened(self):
        return self.PATH in self.current_url
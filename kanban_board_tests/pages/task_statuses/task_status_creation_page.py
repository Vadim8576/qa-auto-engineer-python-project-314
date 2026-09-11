

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.table_locators import TableLocators
from kanban_board_tests.mixins.task_statuses_mixin import TaskStatusesMixin
from kanban_board_tests.pages.locators.task_statuses_locators import (
    TaskStatusesLocators,
)


class TaskStatusCreationPage(BasePage, TaskStatusesMixin):  
    def is_opened(self):
        return '/task_statuses/create' in self.current_url
        
    def create(self, task_status_data):
        self.type(TaskStatusesLocators.NAME, task_status_data['name'])
        self.type(TaskStatusesLocators.SLUG, task_status_data['slug'])
        self.click(TableLocators.SAVE_BUTTON)
import logging

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.table_locators import TableLocators
from kanban_board_tests.mixins.task_statuses_mixin import TaskStatusesMixin
from kanban_board_tests.mixins.table_mixin import TableMixin
from kanban_board_tests.pages.locators.task_statuses_locators import (
    TaskStatusesLocators,
)

logger = logging.getLogger(__name__)

class EditTaskStatusesPage(BasePage, TaskStatusesMixin, TableMixin):  
    def is_opened(self, task_status_id):
        return f'/task_statuses/{task_status_id}' in self.current_url
    
    def get_task_status_data_from_form(self):
        name = self.value_of(TaskStatusesLocators.NAME)
        slug = self.value_of(TaskStatusesLocators.SLUG)
        return {
            'name': name,
            'slug': slug,
        }
        
    
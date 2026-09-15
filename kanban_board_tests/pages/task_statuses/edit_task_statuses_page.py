import logging

from kanban_board_tests.mixins.buttons_mixin import ButtonsMixin
from kanban_board_tests.mixins.table_mixin import TableMixin
from kanban_board_tests.mixins.task_statuses_mixin import TaskStatusesMixin
from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.task_statuses_locators import (
    TaskStatusesLocators,
)

logger = logging.getLogger(__name__)

class EditTaskStatusesPage(BasePage, TaskStatusesMixin, TableMixin, ButtonsMixin): 
    PATH = '/task_statuses' 
    def is_opened(self, task_status_id):
        return f'{self.PATH}/{task_status_id}' in self.current_url
    
    def get_task_status_data_from_form(self):
        name = self.value_of(TaskStatusesLocators.NAME)
        slug = self.value_of(TaskStatusesLocators.SLUG)
        return {
            'name': self.normalize_text(name),
            'slug': self.normalize_text(slug),
        }
        
    
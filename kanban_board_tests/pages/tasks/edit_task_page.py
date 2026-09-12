import logging

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.mixins.tasks_mixin import TaksMixin
from kanban_board_tests.pages.locators.tasks_locators import (
    TasksLocators,
)

logger = logging.getLogger(__name__)

class EditTaskPage(BasePage, TaksMixin):
    PATH = '/tasks' 
    def is_opened(self, task_id):
        return f'/self.PATH/{task_id}' in self.current_url
    
    def get_task_data_from_form(self):
        assignee = self.text_of(TasksLocators.ASSIGNEE_COMBOBOX)
        title = self.value_of(TasksLocators.TITLE)
        description = self.text_of(TasksLocators.DESCRIPTION)
        status = self.text_of(TasksLocators.STATUS_COMBOBOX)
        return {
            'assignee': assignee,
            'title': title,
            'description': description,
            'status': status,
        }
    
    
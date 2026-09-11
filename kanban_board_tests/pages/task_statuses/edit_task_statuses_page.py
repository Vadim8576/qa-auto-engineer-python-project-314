import logging

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.table_locators import TableLocators
from kanban_board_tests.pages.locators.task_statuses_locators import (
    TaskStatusesLocators,
)

logger = logging.getLogger(__name__)

class EditTaskStatusesPage(BasePage):  
    def is_opened(self, task_status_id):
        return f'/task_statuses/{task_status_id}' in self.current_url
    
    def get_task_status_data_from_form(self):
        name = self.value_of(TaskStatusesLocators.NAME)
        slug = self.value_of(TaskStatusesLocators.SLUG)
        return {
            'name': name,
            'slug': slug,
        }
        
    def set_task_status_name(self, name):
        self.type(TaskStatusesLocators.NAME, name)
    
    def set_task_status_slug(self, slug):
        self.type(TaskStatusesLocators.SLUG, slug)
        
    def set_task_status_data(self, new_task_status_data):
        self.set_task_status_name(new_task_status_data['name'])
        self.set_task_status_slug(new_task_status_data['slug'])
        self.click_save()
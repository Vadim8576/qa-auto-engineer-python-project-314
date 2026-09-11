import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.locators.task_statuses_locators import (
    TaskStatusesLocators,
)


class TaskStatusesMixin:
    def set_task_status_name(self, name):
        self.type(TaskStatusesLocators.NAME, name)
    
    def set_task_status_slug(self, slug):
        self.type(TaskStatusesLocators.SLUG, slug)
        
    def set_task_status_data(self, new_task_status_data):
        self.set_task_status_name(new_task_status_data['name'])
        self.set_task_status_slug(new_task_status_data['slug'])
        self.click_save()
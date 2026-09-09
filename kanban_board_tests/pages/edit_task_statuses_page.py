from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.base_page import BasePage


import logging

import re

import time


logger = logging.getLogger(__name__)

class EditTaskStatusesPage(BasePage):  
    NAME = (By.CSS_SELECTOR, 'input[name="name"]')
    SLUG = (By.CSS_SELECTOR, 'input[name="slug"]')
    SAVE = (By.CSS_SELECTOR, 'button[type="submit"]')
    
    def is_opened(self, task_status_id):
        return f'/task_statuses/{task_status_id}' in self.current_url
    
    def get_task_status_data_from_form(self):
        name = self.value_of(self.NAME)
        slug = self.value_of(self.SLUG)
        return {
            'name': name,
            'slug': slug,
        }
        
    def set_task_status_name(self, name):
        self.type(self.NAME, name)
    
    def set_task_status_slug(self, slug):
        self.type(self.SLUG, slug)
    
    def click_save(self):
        self.click(self.SAVE)
        
    def set_task_status_data(self, new_task_status_data):
        self.set_task_status_name(new_task_status_data['name'])
        self.set_task_status_slug(new_task_status_data['slug'])
        # time.sleep(1)
        self.click_save()
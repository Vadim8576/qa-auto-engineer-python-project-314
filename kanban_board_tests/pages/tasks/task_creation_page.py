import time
import logging
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.tasks_locators import TasksLocators
from kanban_board_tests.pages.locators.table_locators import TableLocators


logger = logging.getLogger(__name__)

class TaskCreationPage(BasePage):  
    def is_opened(self):
        return '/tasks/create' in self.current_url
        
    def create(self, task_data):
        random_option = self.get_random_assignee_option()
        self.click_to_option(random_option)
        
        random_status = self.get_random_status_option()
        self.click_to_option(random_status)
             
        self.type(TasksLocators.TITLE, task_data['title'])
        self.type(TasksLocators.CONTENT, task_data['description'])    
        self.click(TableLocators.SAVE_BUTTON)
    
    def select_assignee(self, option_text):
        self.click_to_dropdown(TasksLocators.ASSIGNEE_COMBOBOX)
        self.click_to_option(option_text)
    
    def get_options_list(self, locator):
        self.click_to_dropdown(locator)
        presentaion = self.wait.until(EC.visibility_of_element_located(TasksLocators.PRESENTATION))
        menu = self.wait.until(EC.visibility_of_element_located(TasksLocators.LISTBOX))
        options = self.wait.until(EC.presence_of_all_elements_located(TasksLocators.LISTBOX_OPTION))
        
        options_list = []
        for option in options:
            options_list.append(option.text)
        return options_list

    def get_random_option(self, locator):
        options = self.get_options_list(locator)
        if not options:
            return None
        random_options = random.choice(options)
        return random_options

    def get_random_assignee_option(self):
        return self.get_random_option(TasksLocators.ASSIGNEE_COMBOBOX)
    
    def get_random_status_option(self):
        return self.get_random_option(TasksLocators.STATUS_COMBOBOX)
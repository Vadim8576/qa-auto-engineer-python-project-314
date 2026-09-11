import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.tasks_locators import TasksLocators
from kanban_board_tests.pages.locators.table_locators import TableLocators
from kanban_board_tests.mixins.tasks_mixin import TaksMixin
from kanban_board_tests.constants.task_const import COLUMN_INDICES

logger = logging.getLogger(__name__)



class TasksPage(BasePage, TaksMixin):   
    NO_RECORDS_MESSAGE = (By.XPATH, "//p[contains(text(), 'No Task statuses yet')]")
    
    def records_is_missing(self):
        elements = self.driver.find_elements(*self.NO_RECORDS_MESSAGE)
        return len(elements) > 0
    
    def is_opened(self):
        return '/tasks' in self.current_url
    
    # def get_all_status_columns(self):
    #     return self.driver.find_elements(*TasksLocators.STATUS_COLUMNS)
    
    def are_all_tasks_visible(self):
        def all_visible(driver):
            elements = self.driver.find_elements(*TasksLocators.TASKS)
            if not elements:
                return False

            for el in elements:
                try:
                    if not el.is_displayed():
                        return False
                except StaleElementReferenceException:
                    return False
            return True
        try:
            self.wait.until(all_visible)
            return True
        except TimeoutException:
            return False
    
    def are_all_tasks_clickable(self, timeout=10):
        def all_clickable(_):
            elements = self.driver.find_elements(*TasksLocators.TASKS)
            if not elements:
                return False

            for el in elements:
                try:
                    if not (el.is_displayed() and el.is_enabled()):
                        return False
                except StaleElementReferenceException:
                    return False
            return True
        try:
            self.wait.until(all_clickable)
            return True
        except TimeoutException:
            return False
    
    
    def get_all_tasks(self):
        return self.driver.find_elements(*TasksLocators.TASKS)
    
    
    def wait_for_task_count_change(self, old_count):
        self.wait.until(lambda d: len(self.get_all_tasks()) != old_count)
    
    def get_all_assignees(self):
        assignees = self.get_options_list(TasksLocators.ASSIGNEE_COMBOBOX)
        filtered_assignees = [a for a in assignees if a.strip()]
        return filtered_assignees
    
    def get_all_labels(self):
        labels = self.get_options_list(TasksLocators.LABEL_COMBOBOX)
        filtered_labels = [l for l in labels if l.strip()]
        return filtered_labels
      
    def get_task_list_by_status(self, status):
        column_number = COLUMN_INDICES[status]
        column = self.driver.find_element(*TasksLocators.column_container(column_number))
        tasks = column.find_elements(*TasksLocators.TASK) 
        return tasks

    def get_parse_task_list(self, task_list):
        parse_tasks = []
        for task in task_list:
            title = task.find_elements(*TasksLocators.CARD_TITLE)[0]
            description = task.find_elements(*TasksLocators.CARD_DESCRIPTION)[0]
            parse_tasks.append({
                'title': title.text,
                'description': description.text
            })
        return parse_tasks

    def has_task(self, tasks, title, description):
        return any(
            t['title'] == title and t['description'] == description
            for t in tasks
        )
    
    def click_edit(self, task):
        edit_button = task.find_element(*TasksLocators.EDIT_BUTTON)
        edit_button.click()
        
    def find_first_available_task(self):
        task = None
        for column_status in COLUMN_INDICES:
            task_list = self.get_task_list_by_status(column_status)
            if len(task_list) > 0:
                task = task_list[0]
                break
        return task
    
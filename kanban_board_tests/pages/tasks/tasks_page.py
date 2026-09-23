import logging

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.constants.task_consts import STATUS_TO_ID
from kanban_board_tests.mixins.buttons_mixin import ButtonsMixin
from kanban_board_tests.mixins.table_mixin import TableMixin
from kanban_board_tests.mixins.tasks_mixin import TaksMixin
from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.tasks_locators import TasksLocators

logger = logging.getLogger(__name__)

class TasksPage(BasePage, TaksMixin, TableMixin, ButtonsMixin):   
    NO_RECORDS_MESSAGE = (By.XPATH, "//p[contains(text(), 'No Task statuses yet')]")
    PATH = '/tasks'
    def records_is_missing(self):
        elements = self.driver.find_elements(*self.NO_RECORDS_MESSAGE)
        return len(elements) > 0
    
    def is_opened(self):
        return self.PATH in self.current_url
    
    def are_all_tasks_visible(self):
        def all_visible(_):
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
        self.wait.until(
            EC.visibility_of_any_elements_located(TasksLocators.COLUMN_CONTAINER)
        )
        return self.driver.find_elements(*TasksLocators.TASKS)


    
    def get_all_assignees(self):
        assignees = self.get_options_list(TasksLocators.ASSIGNEE_COMBOBOX)
        filtered_assignees = [a for a in assignees if a.strip()]
        
        return filtered_assignees
    
    def get_all_labels(self):
        labels = self.get_options_list(TasksLocators.LABEL_COMBOBOX)
        filtered_labels = [l for l in labels if l.strip()]
        return filtered_labels
      
    def get_task_list_by_status(self, status):
        column_id = STATUS_TO_ID[status]
        column = self.wait.until(
            EC.presence_of_element_located(TasksLocators.column_container(column_id))
        )
        
        tasks = column.find_elements(*TasksLocators.TASKS) 
        
        column = self.wait.until(
        EC.presence_of_element_located(TasksLocators.column_container(column_id))
    )
        return tasks
    
    def get_column_by_status(self, status):
        column_id = STATUS_TO_ID[status]
        return self.driver.find_element(*TasksLocators.column_container(column_id))
    
    def get_status_column_by_id(self, column_id):
        return self.driver.find_element(*TasksLocators.column_container(column_id))

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
        for column_status in STATUS_TO_ID:
            task_list = self.get_task_list_by_status(column_status)
            if len(task_list) > 0:
                task = task_list[0]
                break
        return task
        
    def get_status_column_by_task(self, task):
        return task.find_element(By.XPATH, './parent::*')
    
    def get_task_count_in_column(self, column):
        return len(column.find_elements(*TasksLocators.TASKS))
    
    def get_status_column_id(self, status_column):
        return status_column.get_attribute('data-rfd-droppable-id')

    def get_task_count_in_column_by_id(self, column_id):
        column = self.get_status_column_by_id(column_id)
        tasks = column.find_elements(*TasksLocators.TASKS)
        return len(tasks)

    def wait_for_task_removal_in_column_by_id(self, status_column_id, old_count):
        def check(driver):
            try:
                current_count = self.get_task_count_in_column_by_id(status_column_id)
                return current_count < old_count
            except StaleElementReferenceException:
                return False

        try:
            self.wait.until(
                check, 
                message=f'The quantity has not changed, it remains {old_count}'
            )
        except TimeoutException as e:
            logger.warning(e)

    def wait_for_task_count_change(self, old_count):
        def check(driver):
            try:
                current_count = len(self.get_all_tasks())
                return current_count != old_count
            except StaleElementReferenceException:
                return False
            
        try:
            self.wait.until(
                check, 
                message=f'The quantity has not changed, it remains {old_count}'
            )
        except TimeoutException as e:
            
            logger.warning(e)
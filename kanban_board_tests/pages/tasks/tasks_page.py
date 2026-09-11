import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.tasks_locators import TasksLocators
from kanban_board_tests.pages.locators.table_locators import TableLocators
from kanban_board_tests.constants.task_const import COLUMN_INDICES

logger = logging.getLogger(__name__)



class TasksPage(BasePage):   
    NO_RECORDS_MESSAGE = (By.XPATH, "//p[contains(text(), 'No Task statuses yet')]")
    
    def records_is_missing(self):
        elements = self.driver.find_elements(*self.NO_RECORDS_MESSAGE)
        return len(elements) > 0
    
    def is_opened(self):
        return '/tasks' in self.current_url
    
    
    
    ##################################
    
    def get_column_container(self, column_title: str):
        xpath = TasksLocators.TASKS_CONTAINER.format(column_title=column_title)
        return (By.XPATH, xpath)
    
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
    
    ################################
    
    
    
    
    

    
    def table_parse(self):
        table = self.wait.until(EC.visibility_of_element_located(TableLocators.TABLE))
        rows = table.find_elements(*TableLocators.ROW)

        parsed_data = []
        for row in rows:
            cells = row.find_elements(*TableLocators.CELL)
            row_data = [cell.text.strip() for cell in cells]
            status_id, name, slug, created_at = row_data[1:5]
            
            parsed_data.append({
                'id': status_id,
                'name': name,
                'slug': slug,
                'created_at': created_at
            })
        return parsed_data
      
    def is_record_added(self, status):
        parsed_records = self.table_parse()
        return any(
            r['name'] == status['name']
            and r['slug'] == status['slug']
            for r in parsed_records
        )
    
    def click_on_record(self, status_id):       
        table = self.wait.until(EC.visibility_of_element_located(TableLocators.TABLE))
        rows = table.find_elements(*TableLocators.ROW)

        for row in rows:
            cells = row.find_elements(*TableLocators.CELL)
            row_data = [cell.text.strip() for cell in cells]
            row_status_id, name, slug, _ = row_data[1:]
            if row_status_id == status_id:
                row.click()
                return {
                    'name': name,
                    'slug': slug
                }
    
                

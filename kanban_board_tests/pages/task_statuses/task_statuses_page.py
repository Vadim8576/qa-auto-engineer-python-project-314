import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from kanban_board_tests.mixins.buttons_mixin import ButtonsMixin
from kanban_board_tests.mixins.table_mixin import TableMixin
from kanban_board_tests.mixins.task_statuses_mixin import TaskStatusesMixin
from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.table_locators import TableLocators
from kanban_board_tests.pages.locators.task_statuses_locators import (
    TaskStatusesLocators,
)

logger = logging.getLogger(__name__)

class TaskStatusesPage(BasePage, TableMixin, TaskStatusesMixin, ButtonsMixin):   
    PATH = '/task_statuses'
    def records_is_missing(self):
        elements = self.driver.find_elements(*TaskStatusesLocators.NO_RECORDS_MESSAGE)
        return len(elements) > 0
    
    def is_opened(self):
        return self.PATH in self.current_url
    
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
    
    def select_record(self, status_id):
        table = self.wait.until(EC.visibility_of_element_located(TableLocators.TABLE))
        rows = table.find_elements(*TableLocators.ROW)

        for row in rows:
            cells = row.find_elements(*TableLocators.CELL)         
            row_data = [cell.text.strip() for cell in cells]
            row_status_id, name, slug, _ = row_data[1:]
            
            if row_status_id == status_id:
                logger.info(f'Click on checkbox with ID = {status_id}')
                checkbox = row.find_element(*TableLocators.CHECKBOX)
                checkbox.click()
                return {
                    'name': name,
                    'slug': slug,
                }

    def wait_for_task_status_removal(self, old_count):
        def check(driver):
            try:
                current_count = len(self.table_parse())
                return current_count < old_count
            except StaleElementReferenceException:
                return False
        
        try:
            self.wait.until(
                check, 
                message=f'The expected quantity should be < {old_count}'
            )
        except TimeoutException as e:
            logger.warning(e)
        
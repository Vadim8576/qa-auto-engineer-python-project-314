import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.table_locators import TableLocators

logger = logging.getLogger(__name__)

class TaskStatusesPage(BasePage):   
    NO_RECORDS_MESSAGE = (By.XPATH, "//p[contains(text(), 'No Task statuses yet')]")
    
    def records_is_missing(self):
        elements = self.driver.find_elements(*self.NO_RECORDS_MESSAGE)
        return len(elements) > 0
    
    def is_opened(self):
        return '/task_statuses' in self.current_url
    
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
                
    
        
        
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.table_locators import TableLocators
from kanban_board_tests.pages.locators.labels_locators import LabelsLocators
from kanban_board_tests.mixins.table_mixin import TableMixin


logger = logging.getLogger(__name__)

class LabelsPage(BasePage, TableMixin):  
    PATH = '/labels'
    def records_is_missing(self):
        elements = self.driver.find_elements(*LabelsLocators.NO_RECORDS_MESSAGE)
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
            label_id, name, created_at = row_data[1:4]
            
            parsed_data.append({
                'id': label_id,
                'name': name,
                'created_at': created_at
            })
        return parsed_data
      
    def is_record_added(self, label):
        parsed_records = self.table_parse()
        return any(
            r['name'] == label
            for r in parsed_records
        )
    
    def click_on_record(self, label_id):       
        table = self.wait.until(EC.visibility_of_element_located(TableLocators.TABLE))
        rows = table.find_elements(*TableLocators.ROW)

        for row in rows:
            cells = row.find_elements(*TableLocators.CELL)
            row_data = [cell.text.strip() for cell in cells]
            row_label_id, name, _ = row_data[1:]
            if row_label_id == label_id:
                row.click()
                return {
                    'name': name
                }
    
    def select_record(self, label_id):
        table = self.wait.until(EC.visibility_of_element_located(TableLocators.TABLE))
        rows = table.find_elements(*TableLocators.ROW)

        for row in rows:
            cells = row.find_elements(*TableLocators.CELL)         
            row_data = [cell.text.strip() for cell in cells]
            row_label_id, name, _ = row_data[1:]
            
            if row_label_id == label_id:
                logger.info(f'Click on checkbox with ID = {label_id}')
                checkbox = row.find_element(*TableLocators.CHECKBOX)
                checkbox.click()
                return {
                    'name': name
                }
                
    
        
        
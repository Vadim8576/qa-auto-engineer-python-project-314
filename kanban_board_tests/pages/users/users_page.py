import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.table_locators import TableLocators

logger = logging.getLogger(__name__)

class UsersPage(BasePage):
    NO_RECORDS_MESSAGE = (By.XPATH, "//p[contains(text(), 'No Users yet')]")
    
    def records_is_missing(self):
        elements = self.driver.find_elements(*self.NO_RECORDS_MESSAGE)
        return len(elements) > 0
    
    def is_opened(self):
        return '/users' in self.current_url
    
    def table_parse(self):
        table = self.wait.until(EC.visibility_of_element_located(TableLocators.TABLE))
        rows = table.find_elements(*TableLocators.ROW)

        parsed_data = []
        for row in rows:
            cells = row.find_elements(*TableLocators.CELL)
            row_data = [cell.text.strip() for cell in cells]
            user_id, email, first_name, last_name, created_at = row_data[1:6]
            
            parsed_data.append({
                'id': user_id,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'created_at': created_at
            })
        return parsed_data
    
    
     
    def is_record_added(self, user):
        parsed_records = self.table_parse()
        return any(
            r['email'] == user['email']
            and r['first_name'] == user['first_name']
            and r['last_name'] == user['last_name']
            for r in parsed_records
        )
    
    

    def click_on_record(self, user_id):       
        table = self.wait.until(EC.visibility_of_element_located(TableLocators.TABLE))
        rows = table.find_elements(*TableLocators.ROW)

        for row in rows:
            cells = row.find_elements(*TableLocators.CELL)
            row_data = [cell.text.strip() for cell in cells]
            row_user_id, email, first_name, last_name, _ = row_data[1:]
            if row_user_id == user_id:
                row.click()
                return {
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
    
    def select_record(self, user_id):
        table = self.wait.until(EC.visibility_of_element_located(TableLocators.TABLE))
        rows = table.find_elements(*TableLocators.ROW)

        for row in rows:
            cells = row.find_elements(*TableLocators.CELL)         
            row_data = [cell.text.strip() for cell in cells]
            row_user_id, email, first_name, last_name, _ = row_data[1:]
            # row_user_id = row_data[1]
            
            if row_user_id == user_id:
                logger.info(f'Click on checkbox with ID = {user_id}')
                checkbox = row.find_element(*TableLocators.CHECKBOX)
                checkbox.click()
                return {
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
                
    
        
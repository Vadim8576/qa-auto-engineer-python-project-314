import random
import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.users_page import UsersPage

logger = logging.getLogger(__name__)

class TaskStatusesPage(UsersPage):
    TABLE_HEAD = (By.TAG_NAME, 'thead')
    TABLE = (By.TAG_NAME, 'tbody')
    DATA_ROWS = (By.CSS_SELECTOR, 'tbody tr')
    ROW = (By.TAG_NAME, 'tr')
    CELL = (By.TAG_NAME, 'td')
    
    CREATE_BUTTON = (By.CSS_SELECTOR, 'a[aria-label="Create"]')
    DELETE_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Delete"]')
    CHECKBOX = (By.CSS_SELECTOR, 'input[type="checkbox"]')
    
    NO_RECORDS_MESSAGE = (By.XPATH, "//p[contains(text(), 'No Task statuses yet')]")
    
    def click_to_create(self):
        self.click(self.CREATE_BUTTON)
    
    def click_to_delete(self):
        self.click(self.DELETE_BUTTON)

    def get_random_id(self):
        records = self.table_parse()
        if not records:
            return None
        random_records = random.choice(records)
        return random_records['id']
    
    def table_loads(self):
        try:
            self.wait.until(
                lambda d: [r for r in d.find_elements(*self.DATA_ROWS) if r.is_displayed()]
            )
            return True
        except TimeoutException:
            return False
    
    def select_all_records(self):        
        table_head = self.wait.until(EC.visibility_of_element_located(self.TABLE_HEAD))
        head = table_head.find_element(*self.ROW)
        checkbox = head.find_element(*self.CHECKBOX)
        checkbox.click()
    
    def records_is_missing(self):
        elements = self.driver.find_elements(*self.NO_RECORDS_MESSAGE)
        return len(elements) > 0
    
    
    
    
    
    
    def is_opened(self):
        return '/task_statuses' in self.current_url
    
    def table_parse(self):
        table = self.wait.until(EC.visibility_of_element_located(self.TABLE))
        rows = table.find_elements(*self.ROW)

        parsed_data = []
        for row in rows:
            cells = row.find_elements(*self.CELL)
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
        table = self.wait.until(EC.visibility_of_element_located(self.TABLE))
        rows = table.find_elements(*self.ROW)

        for row in rows:
            cells = row.find_elements(*self.CELL)
            row_data = [cell.text.strip() for cell in cells]
            row_status_id, name, slug, _ = row_data[1:]
            if row_status_id == status_id:
                row.click()
                return {
                    'name': name,
                    'slug': slug
                }
    
    def select_record(self, status_id):
        table = self.wait.until(EC.visibility_of_element_located(self.TABLE))
        rows = table.find_elements(*self.ROW)

        for row in rows:
            cells = row.find_elements(*self.CELL)         
            row_data = [cell.text.strip() for cell in cells]
            row_status_id, name, slug, _ = row_data[1:]
            
            if row_status_id == status_id:
                logger.info(f'Click on checkbox with ID = {status_id}')
                checkbox = row.find_element(*self.CHECKBOX)
                checkbox.click()
                return {
                    'name': name,
                    'slug': slug,
                }
                
    
        
        
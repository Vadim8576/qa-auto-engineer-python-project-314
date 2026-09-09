import random
import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.base_page import BasePage

logger = logging.getLogger(__name__)

class UsersPage(BasePage):
    CREATE_BUTTON = (By.CSS_SELECTOR, 'a[aria-label="Create"]')
    DELETE_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Delete"]')
    TABLE = (By.TAG_NAME, 'tbody')
    ROWS = (By.TAG_NAME, 'tr')
    CELL = (By.TAG_NAME, 'td')
    CHECKBOX = (By.CSS_SELECTOR, 'input[type="checkbox"]')
    DATA_ROWS = (By.CSS_SELECTOR, 'tbody tr')
    
    def is_opened(self):
        return '/users' in self.current_url


    def click_to_create(self):
        self.click(self.CREATE_BUTTON)
    
    def click_to_delete(self):
        self.click(self.DELETE_BUTTON)

    def user_table_parse(self):
        table = self.wait.until(EC.visibility_of_element_located(self.TABLE))
        rows = table.find_elements(*self.ROWS)

        parsed_data = []
        for row in rows:
            cells = row.find_elements(*self.CELL)
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
    
    def get_random_user_id(self):
        users = self.user_table_parse()
        if not users:
            return None
        random_user = random.choice(users)
        return random_user['id']
    
    
    def is_user_added(self, user):
        parsed_users = self.user_table_parse()
        return any(
            pu['email'] == user['email']
            and pu['first_name'] == user['first_name']
            and pu['last_name'] == user['last_name']
            for pu in parsed_users
        )
    
    
    def users_table_loads(self):
        try:
            self.wait.until(
                lambda d: [r for r in d.find_elements(*self.DATA_ROWS) if r.is_displayed()]
            )
            return True
        except TimeoutException:
            return False


    def click_on_user(self, user_id):
        users = self.user_table_parse()
        
        table = self.wait.until(EC.visibility_of_element_located(self.TABLE))
        rows = table.find_elements(*self.ROWS)

        for row in rows:
            cells = row.find_elements(*self.CELL)
            row_data = [cell.text.strip() for cell in cells]
            row_user_id, email, first_name, last_name, _ = row_data[1:]
            if row_user_id == user_id:
                row.click()
                return {
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
    
    def click_on_checkbox(self, user_id):
        users = self.user_table_parse()
        
        table = self.wait.until(EC.visibility_of_element_located(self.TABLE))
        rows = table.find_elements(*self.ROWS)

        for row in rows:
            cells = row.find_elements(*self.CELL)         
            row_data = [cell.text.strip() for cell in cells]
            row_user_id, email, first_name, last_name, _ = row_data[1:]
            # row_user_id = row_data[1]
            
            if row_user_id == user_id:
                logger.info(f'Click on checkbox with ID = {user_id}')
                checkbox = row.find_element(*self.CHECKBOX)
                checkbox.click()
                return {
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
                
                
            
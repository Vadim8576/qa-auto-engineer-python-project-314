import random

from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.locators.table_locators import (
    TableLocators,
)


class TableMixin:
    def table_loads(self):
        try:
            self.wait.until(
                lambda d: [r for r in d.find_elements(*TableLocators.DATA_ROWS) if r.is_displayed()]
            )
            return True
        except TimeoutException:
            return False
    
    def select_all_records(self):        
        table_head = self.wait.until(EC.visibility_of_element_located(TableLocators.TABLE_HEAD))
        head = table_head.find_element(*TableLocators.ROW)
        checkbox = head.find_element(*TableLocators.CHECKBOX)
        checkbox.click()
    
    def get_random_id(self):
        records = self.table_parse()
        if not records:
            return None
        random_records = random.choice(records)
        return random_records['id']
    
    def click_create(self):
        self.click(TableLocators.CREATE_BUTTON)
    
    def click_delete(self):
        self.click(TableLocators.DELETE_BUTTON)
    
    def click_save(self):
        self.click(TableLocators.SAVE_BUTTON)
    
    
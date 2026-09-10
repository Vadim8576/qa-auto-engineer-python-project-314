import logging

from selenium.webdriver.common.by import By

from kanban_board_tests.pages.base_page import BasePage

logger = logging.getLogger(__name__)

class EditLabelPage(BasePage):  
    NAME = (By.CSS_SELECTOR, 'input[name="name"]')
    SAVE = (By.CSS_SELECTOR, 'button[type="submit"]')
    
    def is_opened(self, label_id):
        return f'/labels/{label_id}' in self.current_url
    
    def get_label_data_from_form(self):
        name = self.value_of(self.NAME)
        return {
            'name': name
        }
    
    def set_label_name(self, name):
        self.type(self.NAME, name)
    
    def click_save(self):
        self.click(self.SAVE)
        
    def set_label_data(self, new_label_data):
        self.set_label_name(new_label_data)
        self.click_save()
    
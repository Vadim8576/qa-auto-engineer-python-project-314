
from selenium.webdriver.common.by import By

from kanban_board_tests.pages.base_page import BasePage


class LabelCreationPage(BasePage):
    NAME = (By.CSS_SELECTOR, 'input[name="name"]')
    SAVE_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Save"]')
    
    def is_opened(self):
        return '/labels/create' in self.current_url
        
    def create(self, label_data):
        self.type(self.NAME, label_data)
        self.click(self.SAVE_BUTTON)
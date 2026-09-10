
from selenium.webdriver.common.by import By

from kanban_board_tests.pages.base_page import BasePage


class TaskStatusCreationPage(BasePage):
    NAME = (By.CSS_SELECTOR, 'input[name="name"]')
    SLUG = (By.CSS_SELECTOR, 'input[name="slug"]')
    SAVE_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Save"]')
    
    def is_opened(self):
        return '/task_statuses/create' in self.current_url
        
    def create(self, task_status_data):
        self.type(self.NAME, task_status_data['name'])
        self.type(self.SLUG, task_status_data['slug'])
        self.click(self.SAVE_BUTTON)
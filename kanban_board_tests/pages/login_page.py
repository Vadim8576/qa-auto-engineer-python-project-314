
from selenium.webdriver.common.by import By

from kanban_board_tests.pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, ":r4:")
    PASSWORD = (By.ID, ":r6:")
    SUBMIT = (By.CSS_SELECTOR, '[type="submit"]')
    PATH = '/login'
        
    def is_opened(self):
        return self.PATH in self.current_url

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)


from selenium.webdriver.common.by import By

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.login_locators import LoginLocators

class LoginPage(BasePage):
    PATH = '/login'  
    def is_opened(self):
        return self.PATH in self.current_url

    def login(self, username, password):
        self.type(LoginLocators.USERNAME, username)
        self.type(LoginLocators.PASSWORD, password)
        self.click(LoginLocators.SUBMIT)

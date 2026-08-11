from kanban_board_tests.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    USERNAME = (By.ID, ":r4:")
    PASSWORD = (By.ID, ":r6:")
    SUBMIT = (By.CSS_SELECTOR, '[type="submit"]')

    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url)

    def login(self, username, password):
        """Авторизация"""
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)

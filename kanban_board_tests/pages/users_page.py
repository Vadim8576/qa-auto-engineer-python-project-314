from selenium.webdriver.common.by import By

from kanban_board_tests.pages.base_page import BasePage


class UsersPage(BasePage):
    USERNAME = (By.ID, ":r4:")
    PASSWORD = (By.ID, ":r6:")
    SUBMIT = (By.CSS_SELECTOR, '[type="submit"]')

    def __init__(self, driver):
        super().__init__(driver)


    # def login(self, username, password):
    #     """Авторизация"""
    #     self.type(self.USERNAME, username)
    #     self.type(self.PASSWORD, password)
    #     self.click(self.SUBMIT)

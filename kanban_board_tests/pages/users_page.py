
from selenium.webdriver.common.by import By

from kanban_board_tests.pages.base_page import BasePage


class UsersPage(BasePage):
    CREATE_BUTTON = (By.CSS_SELECTOR, 'a[aria-label="Create"]')
    TABLE = (By.TAG_NAME, "tbody")

    def is_opened(self):
        return '/users' in self.current_url

    def create_user(self):
        self.click(self.CREATE_BUTTON)

    def get_rows_of_table(self):
        return list(self.wait.until(EC.presence_of_all_elements_located(self.TABLE)))
from urllib.parse import urlparse

from selenium.webdriver.common.by import By

from kanban_board_tests.pages.base_page import BasePage


class DashboardPage(BasePage):
    PROFILE = (By.CSS_SELECTOR, 'button[aria-label="Profile"]')
    LOGOUT = (By.XPATH, '//li[contains(., "Logout")]')

    def is_opened(self):
        return urlparse(self.current_url).path in ('/', '')   

    def logout(self):
        self.click(self.PROFILE)
        self.click(self.LOGOUT)
from urllib.parse import urlparse

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.dashboard_locators import (
    DashboardLocators,
)


class DashboardLocators(BasePage):
    def is_opened(self):
        return urlparse(self.current_url).path in ('/', '')   

    def logout(self):
        self.click(DashboardLocators.PROFILE)
        self.click(DashboardLocators.LOGOUT)
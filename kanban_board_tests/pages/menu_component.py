import logging

from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.menu_locators import (
    MenuLocators,
)

logger = logging.getLogger(__name__)

class Menu(BasePage):
    def go_to(self, page_name):    
        page_name = page_name.strip()
        item = self.wait.until(EC.element_to_be_clickable(MenuLocators.menu_item(page_name)))
        item.click()
        logger.info(f'Menu button "{page_name}" pressed.')
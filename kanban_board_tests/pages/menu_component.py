import logging

from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.menu_locators import (
    MenuLocators,
)
from kanban_board_tests.constants.menu_consts import MENU_MAP

logger = logging.getLogger(__name__)

class Menu(BasePage):
    page_name = MENU_MAP
    def go_to(self, page_name):
        items = self.wait.until(EC.presence_of_all_elements_located(MenuLocators.MENU_ITEMS))
        
        for item in items:
            if page_name.strip() == item.text.strip():
                item.click()
                logger.info(f'Menu button "{item.text}" pressed. Go to {item.text} page.')
                return

        raise ValueError(
            f'Menu item "{page_name}" not found'
        )
        
    
import logging

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from kanban_board_tests.pages.base_page import BasePage


logger = logging.getLogger(__name__)

class Menu(BasePage):
    MENU_ITEMS = (By.CSS_SELECTOR, 'a[role="menuitem"]')
    
    def go_to(self, page_name):
        items = self.wait.until(EC.presence_of_all_elements_located(self.MENU_ITEMS))
        
        for item in items:
            if page_name.strip() == item.text.strip():
                item.click()
                logger.info(f'Menu button "{item.text}" pressed')
                return

        raise ValueError(
            f'Menu item "{page_name}" not found'
        )
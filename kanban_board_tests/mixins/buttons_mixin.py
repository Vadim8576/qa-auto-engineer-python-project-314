import random

from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.locators.buttons_locators import (
    ButtonsLocators,
)


class ButtonsMixin:
    def click_create(self):
        self.click(ButtonsLocators.CREATE_BUTTON)
    
    def click_delete(self):
        self.click(ButtonsLocators.DELETE_BUTTON)
    
    def click_save(self):
        self.click(ButtonsLocators.SAVE_BUTTON)
    
    
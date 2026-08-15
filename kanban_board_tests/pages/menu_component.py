from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class Menu(BasePage):
    MENU = (By.CSS_SELECTOR, 'ul[role="menu"]')
    
    def go_to(self, page_name):
        menu = self.driver.find_element(self.MENU)
        items = menu.find_elements(By.TAG_NAME, 'a')
        # нужно нажимать на кнопки page_name
        
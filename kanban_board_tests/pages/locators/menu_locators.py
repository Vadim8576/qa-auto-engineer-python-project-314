from selenium.webdriver.common.by import By


class MenuLocators:
    MENU_ITEMS = (By.CSS_SELECTOR, 'a[role="menuitem"]')
    @staticmethod
    def menu_item(page_name):
        return (By.XPATH, f"//a[normalize-space()='{page_name}']")
from selenium.webdriver.common.by import By


class ButtonsLocators:
    CREATE_BUTTON = (By.CSS_SELECTOR, 'a[aria-label="Create"]')
    DELETE_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Delete"]')
    SAVE_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Save"]')
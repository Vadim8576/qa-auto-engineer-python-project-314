from selenium.webdriver.common.by import By


class LoginLocators:
    USERNAME = (By.ID, ":r4:")
    PASSWORD = (By.ID, ":r6:")
    SUBMIT = (By.CSS_SELECTOR, '[type="submit"]')
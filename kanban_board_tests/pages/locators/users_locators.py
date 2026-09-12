from selenium.webdriver.common.by import By


class UserLocators:
    EMAIL = (By.CSS_SELECTOR, 'input[name="email"]')
    FIRST_NAME = (By.CSS_SELECTOR, 'input[name="firstName"]')
    LAST_NAME = (By.CSS_SELECTOR, 'input[name="lastName"]')
    NO_RECORDS_MESSAGE = (By.XPATH, "//p[contains(text(), 'No Users yet')]")
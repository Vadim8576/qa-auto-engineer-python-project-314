from selenium.webdriver.common.by import By


class LabelsLocators:
    NAME = (By.CSS_SELECTOR, 'input[name="name"]')
    NO_RECORDS_MESSAGE = (By.XPATH, "//p[contains(text(), 'No Labels yet')]")
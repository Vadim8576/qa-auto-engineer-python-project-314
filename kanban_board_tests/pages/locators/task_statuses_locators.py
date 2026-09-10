from selenium.webdriver.common.by import By


class TaskStatusesLocators:
    NAME = (By.CSS_SELECTOR, 'input[name="name"]')
    SLUG = (By.CSS_SELECTOR, 'input[name="slug"]')
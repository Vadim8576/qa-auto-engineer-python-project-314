from selenium.webdriver.common.by import By


class TableLocators:
    DATA_ROWS = (By.CSS_SELECTOR, 'tbody tr')
    TABLE_HEAD = (By.TAG_NAME, 'thead')
    TABLE = (By.TAG_NAME, 'tbody')
    ROW = (By.TAG_NAME, 'tr')
    CELL = (By.TAG_NAME, 'td')
    CHECKBOX = (By.CSS_SELECTOR, 'input[type="checkbox"]')
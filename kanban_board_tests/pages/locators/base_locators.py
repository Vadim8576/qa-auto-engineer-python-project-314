from selenium.webdriver.common.by import By


class BaseLocators:
    HEADER = (By.ID, 'react-admin-title')
    ALERT = (By.CSS_SELECTOR, 'div[role="alert"] div[class*="message"]')
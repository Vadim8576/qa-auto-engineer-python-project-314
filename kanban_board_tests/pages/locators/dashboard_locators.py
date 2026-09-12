from selenium.webdriver.common.by import By


class DashboardLocators:
    PROFILE = (By.CSS_SELECTOR, 'button[aria-label="Profile"]')
    LOGOUT = (By.XPATH, '//li[contains(., "Logout")]')
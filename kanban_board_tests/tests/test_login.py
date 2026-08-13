from selenium.webdriver.common.by import By

from kanban_board_tests.pages.login_page import LoginPage


def test_login_success(driver, base_url):
    try:
        page = LoginPage(driver)
        page.open(base_url)    
        page.login("Alex", "Password!")
        assert 'Welcome to the administration' in page.text_of((By.ID, 'react-admin-title')) 
    except Exception as e:
        print('Ошибка:', e)
        raise


def test_logout_success(driver, base_url):
    try:
        page = LoginPage(driver)
        page.open(base_url)
        page.login("Alex", "Password!")
        
        page.click((By.CSS_SELECTOR, 'button[aria-label="Profile"]'))
        page.click((By.XPATH, '//li[contains(., "Logout")]'))
        assert 'login' in page.get_current_url()
    except Exception as e:
        print('Ошибка:', e)
        raise
from selenium.webdriver.common.by import By

from kanban_board_tests.pages.login_page import LoginPage


def test_login_success(driver, base_url):
    try:
        page = LoginPage(driver, base_url)
        page.open()    
        page.login("Alex", "Password!")
    except Exception as e:
        print('Ошибка:', e)
        raise


def test_logout_success(driver, base_url):
    try:
        page = LoginPage(driver, base_url)
        page.open()
        page.login("Alex", "Password!")
        
        page.click((By.CSS_SELECTOR, 'button[aria-label="Profile"]'))
        page.click((By.XPATH, '//li[contains(., "Logout")]'))
        assert 'login' in page.current_url()
    except Exception as e:
        print('Ошибка:', e)
        raise
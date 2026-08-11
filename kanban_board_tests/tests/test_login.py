from kanban_board_tests.pages.login_page import LoginPage
from selenium.webdriver.common.by import By


def test_login_success(driver, base_url):
    try:
        page = LoginPage(driver, base_url)
        page.open()
        page.login("Alex", "Password!")
        assert 'Welcome to the administration' in page.text_of((By.ID, 'react-admin-title')) 
    except Exception as e:
        print('Ошибка:', e)
        raise
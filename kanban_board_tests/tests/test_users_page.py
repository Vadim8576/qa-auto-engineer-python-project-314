
from kanban_board_tests.pages.users_page import UsersPage


def test_creation_user(driver, base_url):
    try:
        page = UsersPage(driver)
        page.open(base_url)    
        # page.login("Alex", "Password!")
    except Exception as e:
        print('Ошибка:', e)
        raise


# def test_logout_success(driver, base_url):
#     try:
#         page = LoginPage(driver, base_url)
#         page.open()
#         page.login("Alex", "Password!")
        
#         page.click((By.CSS_SELECTOR, 'button[aria-label="Profile"]'))
#         page.click((By.XPATH, '//li[contains(., "Logout")]'))
#         assert 'login' in page.get_current_url()
#     except Exception as e:
#         print('Ошибка:', e)
#         raise
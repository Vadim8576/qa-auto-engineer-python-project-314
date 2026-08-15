


from kanban_board_tests.pages.dashboard_page import DashboardPage
from kanban_board_tests.pages.login_page import LoginPage


def test_login_success(driver, logged_in_user):
    try:    
        dashboard = DashboardPage(driver)
        assert dashboard.is_opened()
        assert 'Welcome to the administration' in dashboard.header_text()
    except Exception as e:
        print('Ошибка:', e)
        raise


def test_logout_success(driver, logged_in_user):
    try:           
        dashboard = DashboardPage(driver)
        dashboard.logout()
        
        # logging.info('!!!!!!!!!!!!!!!')
        
        login_page = LoginPage(driver)
        assert login_page.is_opened()
    except Exception as e:
        print('Ошибка:', e)
        raise
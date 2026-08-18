import logging

from kanban_board_tests.pages.dashboard_page import DashboardPage
from kanban_board_tests.pages.login_page import LoginPage

logger = logging.getLogger(__name__)
'''
def test_login_success(driver, logged_in_user):
    logger.info('Test login success')
    try:    
        dashboard = DashboardPage(driver)
        assert dashboard.is_opened()
        assert 'Welcome to the administration' in dashboard.header_text()
    except Exception as e:
        print('Ошибка:', e)
        raise


def test_logout_success(driver, logged_in_user):
    logger.info('Test logout success')
    try:           
        dashboard = DashboardPage(driver)
        dashboard.logout()
      
        login_page = LoginPage(driver)
        assert login_page.is_opened()
    except Exception as e:
        print('Ошибка:', e)
        raise
'''
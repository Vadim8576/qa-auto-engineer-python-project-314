import logging

from kanban_board_tests.pages.dashboard.dashboard_page import DashboardPage
from kanban_board_tests.pages.login.login_page import LoginPage

logger = logging.getLogger(__name__)

def test_login_success(pages, logged_in_user):
    logger.info('Test login success')
    try:    
        dashboard = pages(DashboardPage)
        assert dashboard.is_opened()
        assert 'Welcome to the administration' in dashboard.header_text()
    except Exception as e:
        print('Ошибка:', e)
        raise


def test_logout_success(pages, logged_in_user):
    logger.info('Test logout success')
    try:           
        dashboard = pages(DashboardPage)
        dashboard.logout()
      
        login_page = pages(LoginPage)
        assert login_page.is_opened()
    except Exception as e:
        print('Ошибка:', e)
        raise

import logging

from kanban_board_tests.pages.dashboard.dashboard_page import DashboardPage
from kanban_board_tests.pages.login.login_page import LoginPage

logger = logging.getLogger(__name__)

def test_login_success(pages, logged_in_user): 
    dashboard = pages(DashboardPage)
    assert dashboard.is_opened()
    assert 'Welcome to the administration' in dashboard.header_text()

def test_logout_success(pages, logged_in_user):         
    dashboard = pages(DashboardPage)
    login_page = pages(LoginPage)
    dashboard.logout()
    assert login_page.is_opened()
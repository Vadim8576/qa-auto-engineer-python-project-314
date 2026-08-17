
import logging

from kanban_board_tests.pages.users_page import UsersPage
from kanban_board_tests.pages.dashboard_page import DashboardPage
from kanban_board_tests.pages.user_creation_page import UserCreationPage
from kanban_board_tests.pages.menu_component import Menu

logger = logging.getLogger(__name__)

def test_creation_user(driver, logged_in_user):
    try:
        logger.info('Test creation user')
        # dashboard = DashboardPage(driver)
        # assert dashboard.is_opened()
        # assert 'Welcome to the administration' in dashboard.header_text()
        
        menu = Menu(driver)
        menu.go_to('Users')
        
        users = UsersPage(driver)
        assert users.is_opened()
        
        users.create_user()
        logger.info('Button "Create user" pressed')
        
        user_creation = UserCreationPage(driver)
        user_creation.is_opened()
        assert 'Create User' in user_creation.header_text()
            
        # Заполнение формы
        
        USER = {
            'email': 'kate@mail.com',
            'first_name': 'Kate',
            'last_name': 'Alison'
        }
        
        logger.info('Enter email')
        user_creation.type_email(USER['email'])
        logger.info('Enter email complite')
        logger.info('Enter first name')
        user_creation.type_first_name(USER['first_name'])
        logger.info('Enter first name complite')
        logger.info('Enter last name')
        user_creation.type_last_name(USER['last_name'])
        logger.info('Enter last name complite')

        user_creation.save_user()


        
    except Exception as e:
        print('Ошибка:', e)
        raise

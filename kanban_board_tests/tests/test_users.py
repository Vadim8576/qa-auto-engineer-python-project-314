import logging

from kanban_board_tests.pages.users_page import UsersPage
from kanban_board_tests.pages.edit_user_page import EditUserPage
from kanban_board_tests.pages.dashboard_page import DashboardPage
from kanban_board_tests.pages.user_creation_page import UserCreationPage
from kanban_board_tests.pages.menu_component import Menu

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

def test_creation_user(driver, logged_in_user):

    # dashboard = DashboardPage(driver)
    # assert dashboard.is_opened()
    # assert 'Welcome to the administration' in dashboard.header_text()
        
    menu = Menu(driver)
    menu.go_to('Users')
        
    users_page = UsersPage(driver)
    assert users_page.is_opened()
        
    users_page.create_user()
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
        
    logger.info(f'Enter email {USER['email']}')
    user_creation.type_email(USER['email'])
    logger.info('Enter email complite')
    logger.info(f'Enter first name {USER['first_name']}')
    user_creation.type_first_name(USER['first_name'])
    logger.info('Enter first name complite')
    logger.info(f'Enter last name {USER['last_name']}')
    user_creation.type_last_name(USER['last_name'])
    logger.info('Enter last name complite')
    user_creation.save_user()
    logger.info('User saved')  
                
    menu.go_to('Users')
    logger.info('Go to Users page')
        
    assert users_page.is_user_added(USER), f'User {USER['first_name']} not found'
    logger.info(f'User {USER['first_name']} added successfully!')


def test_users_table_is_visibility(driver, logged_in_user):

    users_page = UsersPage(driver)
    assert users_page.users_table_loads(), 'Users table not loaded!'

    parsed_users = users_page.user_table_parse()
    assert len(parsed_users) > 0, 'User not found!'
    logger.info('Users table loaded')




    missing_issues = []

    for i, u in enumerate(parsed_users):
        line_no = i + 1
        has_problem = False

        email = u.get('email')
        if not email or (isinstance(email, str) and not email.strip()):
            missing_issues.append(f"Line {line_no}: missing/empty 'email'")
            has_problem = True

        first_name = u.get('first_name')
        if not first_name or (isinstance(first_name, str) and not first_name.strip()):
            missing_issues.append(f"Line {line_no}: missing/empty 'first_name'")
            has_problem = True

        last_name = u.get('last_name')
        if not last_name or (isinstance(last_name, str) and not last_name.strip()):
            missing_issues.append(f"Line {line_no}: missing/empty 'last_name'")
            has_problem = True
            
        # create_at = u.get('created_at')
        # if not create_at or (isinstance(create_at, str) and not create_at.strip()):
        #     missing_issues.append(f"Line {line_no}: missing/empty 'create_at'")
        #     has_problem = True

    if missing_issues:
        error_msg = "; ".join(missing_issues)
        assert False, f"Found {len(missing_issues)} data issues:\n{error_msg}"
    else:
        logger.info('All required fields are present and non-empty')


def test_edit_user_success(driver, logged_in_user, base_url):
    
    menu = Menu(driver)
    menu.go_to('Users')
    logger.info(f'Go to Users page')
       
    users_page = UsersPage(driver)

    parsed_users = users_page.user_table_parse()
    # logger.info(parsed_users)
    
    
    
    
    edit_user_page = EditUserPage(driver)
    USER_ID = '1'
    
    logger.info(f'Edit user (ID = {USER_ID})')
    
    
    
    
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    edit_user_page.edit_user_by_id(base_url, USER_ID)
    
    
    
    assert edit_user_page.is_editing(USER_ID), f'Expected edit page for user {USER_ID}, but condition is False'
    logger.info(f'Open edit page user {USER_ID}')
    
    
    
    
    
    logger.info(f'Страница {users_page.current_url}')
    
    
    
    
    # driver.save_screenshot("after_open.png")
    
    
    
    
    
    

    
    
    
    
    
    assert 'User john@google.com' in edit_user_page.header_text()
    logger.info(f'User john@google.com')

    
    
    elements = driver.find_elements(By.CSS_SELECTOR, 'input[name="email"]')
    logger.info("Найдено input[name='email']: %d", len(elements))
    
    
    logger.info(f'Get editing user data')
    editing_user_data = users_page.get_editing_user_data()
    logger.info(f'Data received')
    
    editing_user_data['id'] = USER_ID
    
    
    
    
    logger.info(parsed_users)
    
    filtered_users = list(
        filter(lambda u: str(u.get('id')) == USER_ID, parsed_users)
    )
    
    assert filtered_users[0] == editing_user_data
    
    
    
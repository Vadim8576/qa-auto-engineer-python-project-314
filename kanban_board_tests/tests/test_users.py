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
                
    USER = {
        'email': 'kate@mail.com',
        'first_name': 'Kate',
        'last_name': 'Alison'
    }
        
    user_creation.create_user(USER)
    logger.info(f'Create user {USER['first_name']}')


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


def test_edit_user_success(driver, logged_in_user):
    USER_ID = '7'
    
    menu = Menu(driver)
    menu.go_to('Users')
    logger.info(f'Go to Users page')
       
    users_page = UsersPage(driver)     
    selected_user = users_page.click_on_user(USER_ID)
    logger.info(f'Click to user with ID {USER_ID}: {selected_user['email']} {selected_user['first_name']} {selected_user['last_name']}')

    edit_user_page = EditUserPage(driver)
    assert edit_user_page.is_opened(USER_ID), f'Expected edit page for user {USER_ID}, but condition is False'
    logger.info(f'Open edit page user {USER_ID}')
    
    assert f'User {selected_user['email']}' in edit_user_page.header_text(), f'This is not an edit page {selected_user['email']}'


    # Проверка на совпадение данных из формы с данными редактируемого пользователя
    user_from_form = edit_user_page.get_editing_user_data()
    assert user_from_form == selected_user, f'selected for editing {selected_user['email']}, and the current user {user_from_form['email']}'
    logger.info(f'User data matches')
    
    
# Проверка на что измененные данные сохраняются
def test_new_user_data_saved_success(driver, logged_in_user):
    new_user_data = {
        'email': 'new@mail.com',
        'first_name': 'new_first_name',
        'last_name': 'new_last_name',
    }
    
    USER_ID = '7'
    
    menu = Menu(driver)
    menu.go_to('Users')
    logger.info(f'Go to Users page')
       
    users_page = UsersPage(driver)     
    edit_user_page = EditUserPage(driver)
    
    # Получение данных пользователя из таблицы, на которого нажали, так же переход на редактирование
    user_data = users_page.click_on_user(USER_ID)
    
    logger.info(f'Click to user with ID {USER_ID}: {user_data['email']} {user_data['first_name']} {user_data['last_name']}')
    
    # Ввод новых данных и нажатие "сохранить"
    edit_user_page.set_user_data(new_user_data)
    
    # Получаем данные этого же пользователя из таблицы, для проверки, что данные сохранились
    user_data = users_page.click_on_user(USER_ID)
    
    assert user_data == new_user_data, f'selected for editing {user_data}, and the current user {new_user_data}'
    logger.info(f'Update user data success')
    
    
    
    
    # Сейчас неверная логика проверки валидации!!!
    # Нужно вводить неверные email и проверять сообщение self.text_of(self.EMAIL_INCORRECT_MESSAGE)
    
    
     

def test_email_validation(driver, logged_in_user):
    USER_ID = '3'
    EMAILS = {
        'correct': 'aaa@bbb.cc',
        'incorrect': ['@bbb.cc', 'aaa@', 'aaa@bbb', 'aaa']
    }
    
    menu = Menu(driver)
    menu.go_to('Users')
    logger.info(f'Go to Users page')
      
    users_page = UsersPage(driver)
    
    # Выбор пользователя для редактирования
    users_page.click_on_user(USER_ID)
    
    edit_user_page = EditUserPage(driver)
    logger.info(edit_user_page.current_url)
     
    logger.info(f'email validation check')
    
    for incorrect_email in EMAILS['incorrect']:     
        logger.info(f'Input email: {incorrect_email}')

        edit_user_page.set_user_email(incorrect_email)    
        edit_user_page.click_save()
        
        is_email_incorrect = edit_user_page.is_email_incorrect()
        
        assert is_email_incorrect, f'The email check was expected to fail, but it passed: {incorrect_email}'





'''    
<div role="presentation" class="MuiSnackbar-root MuiSnackbar-anchorOriginBottomCenter css-cwrgbr">
    <div class="MuiPaper-root MuiPaper-elevation MuiPaper-elevation6 MuiSnackbarContent-root css-1rp6o9q" role="alert" direction="up" style="opacity: 1; transform: none; transition: opacity 225ms cubic-bezier(0.4, 0, 0.2, 1), transform 150ms cubic-bezier(0.4, 0, 0.2, 1);">
        <div class="MuiSnackbarContent-message css-1w0ym84">
            Element updated
        </div>
        <div class="MuiSnackbarContent-action css-zykra6">
            <button class="MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary RaNotification-undo css-1rtnrqa" tabindex="0" type="button">
                Undo
                <span class="MuiTouchRipple-root css-w0pj6f">
                </span>
            </button>
        </div>
    </div>
</div>
'''
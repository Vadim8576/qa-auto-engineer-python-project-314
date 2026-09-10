import logging

import pytest

from kanban_board_tests.data.emails import INCORRECT_EMAILS
from kanban_board_tests.data.users import USERS_DATA
from kanban_board_tests.pages.menu_component import Menu
from kanban_board_tests.pages.users.edit_user_page import EditUserPage
from kanban_board_tests.pages.users.user_creation_page import UserCreationPage
from kanban_board_tests.pages.users.users_page import UsersPage

logger = logging.getLogger(__name__)

def test_creation_user(driver, logged_in_user):
    logger.info('Test creation user')
    menu = Menu(driver)
    menu.go_to(menu.PAGES['users'])
        
    users_page = UsersPage(driver)
    assert users_page.is_opened()
        
    users_page.click_to_create()
    logger.info('Button "Create user" pressed')
        
    user_creation = UserCreationPage(driver)
    user_creation.is_opened()
    assert 'Create User' in user_creation.header_text()
              
    user = USERS_DATA[0]
        
    user_creation.create(user)
    logger.info(f'Create user {user['first_name']}')
    
    menu.go_to(menu.PAGES['users'])
        
    assert users_page.is_record_added(user), f'User {user['first_name']} not found'
    logger.info(f'User {user['first_name']} added successfully!')


def test_users_table_is_visibility(driver, logged_in_user):
    menu = Menu(driver)
    menu.go_to(menu.PAGES['users'])
    users_page = UsersPage(driver)
    assert users_page.table_loads(), 'Users table not loaded!'

    parsed_records = users_page.table_parse()
    assert len(parsed_records) > 0, 'User not found!'
    logger.info('Users table loaded')

    missing_issues = []

    for i, u in enumerate(parsed_records):
        line_no = i + 1

        email = u.get('email')
        if not email or (isinstance(email, str) and not email.strip()):
            missing_issues.append(f"Line {line_no}: missing/empty 'email'")

        first_name = u.get('first_name')
        if not first_name or (isinstance(first_name, str) and not first_name.strip()):
            missing_issues.append(f"Line {line_no}: missing/empty 'first_name'")

        last_name = u.get('last_name')
        if not last_name or (isinstance(last_name, str) and not last_name.strip()):
            missing_issues.append(f"Line {line_no}: missing/empty 'last_name'")

    if missing_issues:
        error_msg = "; ".join(missing_issues)
        assert False, f"Found {len(missing_issues)} data issues:\n{error_msg}"
    else:
        logger.info('All required fields are present and non-empty')


def test_edit_user_success(driver, logged_in_user):
    menu = Menu(driver)
    menu.go_to(menu.PAGES['users'])
       
    users_page = UsersPage(driver)   
    user_id = users_page.get_random_id()
    
    if user_id is None:
        pytest.skip("Cannot run test: no users available in the table.")
     
    logger.info(f'User with ID = {user_id}')
    
    selected_user = users_page.click_on_record(user_id)
    logger.info(f'Click to user with ID {user_id}: {selected_user['email']} {selected_user['first_name']} {selected_user['last_name']}')

    edit_user_page = EditUserPage(driver)
    assert edit_user_page.is_opened(user_id), f'Expected edit page for user {user_id}, but condition is False'
    logger.info(f'Open edit page user {user_id}')
    
    assert f'User {selected_user['email']}' in edit_user_page.header_text(), f'This is not an edit page {selected_user['email']}'

    # Проверка на совпадение данных из формы с данными редактируемого пользователя
    user_from_form = edit_user_page.get_user_data_from_form()
    assert user_from_form == selected_user, f'selected for editing {selected_user['email']}, and the current user {user_from_form['email']}'
    logger.info('User data is populated correctly.')
    
    
# Проверка, что измененные данные сохраняются
def test_new_user_data_saved_success(driver, logged_in_user):
    new_user_data = USERS_DATA[1]
    
    menu = Menu(driver)
    menu.go_to(menu.PAGES['users'])
       
    users_page = UsersPage(driver)     
    edit_user_page = EditUserPage(driver)
    
    user_id = users_page.get_random_id()
    
    # Получение данных пользователя из таблицы, на которого нажали, так же переход на редактирование
    user_data = users_page.click_on_record(user_id)
    
    logger.info(f'Click to user with ID {user_id}: {user_data['email']} {user_data['first_name']} {user_data['last_name']}')
    
    # Ввод новых данных и нажатие "сохранить"
    edit_user_page.set_user_data(new_user_data)
    
    # Получаем данные этого же пользователя из таблицы, для проверки, что данные сохранились
    user_data = users_page.click_on_record(user_id)
    
    assert user_data == new_user_data, f'selected for editing {user_data}, and the current user {new_user_data}'
    logger.info('Update user data success')
    
     
@pytest.mark.parametrize('incorrect_email', INCORRECT_EMAILS)
def test_email_validation(driver, logged_in_user, incorrect_email):
    menu = Menu(driver)
    menu.go_to(menu.PAGES['users'])
      
    users_page = UsersPage(driver)
    user_id = users_page.get_random_id()
    
    # Выбор пользователя для редактирования
    users_page.click_on_record(user_id)
    
    edit_user_page = EditUserPage(driver)
    logger.info(edit_user_page.current_url)
     
    logger.info(f'Input email: {incorrect_email}')
    logger.info('Email validation check.')

    edit_user_page.set_user_email(incorrect_email)
    email_from_form = edit_user_page.get_user_data_from_form()['email']
    
    assert email_from_form == incorrect_email, f'Expected {incorrect_email} in the email field, not {email_from_form}.'
    
    edit_user_page.click_save()
        
    assert edit_user_page.is_email_incorrect(), f'The email check was expected to fail, but it passed: {incorrect_email}'
    logger.info('Invalid email failed validation.')


def test_remove_user_successful(driver, logged_in_user):  
    menu = Menu(driver)
    menu.go_to(menu.PAGES['users'])
      
    users_page = UsersPage(driver)
    
    # Парсим таблицу
    users_before_deletion = users_page.table_parse()
    users_before_deletion_count = len(users_before_deletion)
    logger.info(f'Users in the table before deletion: {users_before_deletion_count}')
    
    # Если таблица пуста, пропускаем тест
    if users_before_deletion_count == 0:
        pytest.skip("Cannot run test: no users available in the table.")
      
    user_id = users_page.get_random_id()
    # Получаем данные выделенного пользователя
    selected_user = users_page.select_record(user_id)
    logger.info(f'Select user with ID = {user_id}')
    
    # Удаляем выделенного пользователя
    users_page.click_to_delete()
    logger.info('Click to "Delete"')
    
    # Снова парсим таблицу
    users_after_deletion = users_page.table_parse()
    users_after_deletion_count = len(users_after_deletion)
    logger.info(f'Users in the table after deletion: {users_after_deletion_count}')
    
    assert (users_before_deletion_count - 1) == users_after_deletion_count, 'The number of users in the table does not match.'
    
    # Проверяем, что удаленный пользователь отсутствует в таблице
    assert not any(
        u['email'] == selected_user['email']
        and u['first_name'] == selected_user['first_name']
        and u['last_name'] == selected_user['last_name']
        for u in users_after_deletion
    ), 'The user has been deleted but still appears in the table.'
    
    logger.info('The user has been successfully removed from the table.')


def test_remove_all_users_successful(driver, logged_in_user):
    menu = Menu(driver)
    menu.go_to(menu.PAGES['users'])
      
    users_page = UsersPage(driver)
    users = users_page.table_parse()
    users_count = len(users)
    
    users_page.select_all_records()
    logger.info('Select all users in the table.')
    
    # Удаляем выделенных пользователей
    users_page.click_to_delete()
    logger.info('Click to "Delete"')
      
    assert f'{users_count} elements deleted' in users_page.get_alert_text() 
    assert users_page.records_is_missing(), 'The "No Users yet" message is missing. Perhaps not all users have been deleted.'
    logger.info('All users have been successfully deleted.')
    
    

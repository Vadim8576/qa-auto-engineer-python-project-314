import logging

import pytest

from kanban_board_tests.data.task_statuses import TASK_STATUSES
from kanban_board_tests.pages.menu_component import Menu
from kanban_board_tests.pages.task_statuses.edit_task_statuses_page import (
    EditTaskStatusesPage,
)
from kanban_board_tests.pages.task_statuses.task_status_creation_page import (
    TaskStatusCreationPage,
)
from kanban_board_tests.pages.task_statuses.task_statuses_page import TaskStatusesPage

logger = logging.getLogger(__name__)

def test_creation_task_status(driver, logged_in_user):

    menu = Menu(driver)
    menu.go_to(menu.PAGES['task_statuses'])
        
    task_status_page = TaskStatusesPage(driver)
    
    assert task_status_page.is_opened()
    
    task_status_page.click_to_create()
    logger.info('Button "Create user" pressed')
        
    task_status_creation = TaskStatusCreationPage(driver)
    task_status_creation.is_opened()
    assert 'Create Task status' in task_status_creation.header_text()
              
    new_task_status = TASK_STATUSES[0]
        
    task_status_creation.create(new_task_status)
    logger.info(f'Create user {new_task_status['name']}')
    
    menu.go_to(menu.PAGES['task_statuses'])
        
    assert task_status_page.is_record_added(new_task_status), f'User {new_task_status['name']} not found'
    logger.info(f'Task status {new_task_status['name']} added successfully!')


def test_task_status_table_is_visibility(driver, logged_in_user):
    menu = Menu(driver)
    menu.go_to(menu.PAGES['task_statuses'])
    task_status_page = TaskStatusesPage(driver)
    assert task_status_page.table_loads(), 'Users table not loaded!'

    parsed_records = task_status_page.table_parse()
    assert len(parsed_records) > 0, 'Task statuses not found!'
    logger.info('Task statuses table loaded')

    missing_issues = []

    for i, u in enumerate(parsed_records):
        line_no = i + 1

        name = u.get('name')
        if not name or (isinstance(name, str) and not name.strip()):
            missing_issues.append(f"Line {line_no}: missing/empty 'name'")

        slug = u.get('slug')
        if not slug or (isinstance(slug, str) and not slug.strip()):
            missing_issues.append(f"Line {line_no}: missing/empty 'slug'")

    if missing_issues:
        error_msg = "; ".join(missing_issues)
        assert False, f"Found {len(missing_issues)} data issues:\n{error_msg}"
    else:
        logger.info('All required fields are present and non-empty')


def test_edit_task_status_success(driver, logged_in_user):
    menu = Menu(driver)
    menu.go_to(menu.PAGES['task_statuses'])
       
    task_status_page = TaskStatusesPage(driver)
    task_status_id = task_status_page.get_random_id()
    
    if task_status_id is None:
        pytest.skip("Cannot run test: no users available in the table.")
     
    logger.info(f'User with ID = {task_status_id}')
    
    selected_task_status = task_status_page.click_on_record(task_status_id)
    logger.info(f'Click to task status with ID {task_status_id}: {selected_task_status['name']} {selected_task_status['slug']}')

    edit_task_status_page = EditTaskStatusesPage(driver)
    
    assert edit_task_status_page.is_opened(task_status_id), f'Expected edit page for task status {task_status_id}, but condition is False'
    logger.info(f'Open edit page task status {task_status_id}')
    
    assert f'Task status {selected_task_status['name']}' in edit_task_status_page.header_text(), f'This is not an edit page {selected_task_status}'

    # Проверка на совпадение данных из формы с данными редактируемого пользователя
    task_status_from_form = edit_task_status_page.get_task_status_data_from_form()
    assert task_status_from_form == selected_task_status, f'selected for editing {selected_task_status['name']}, and the current user {task_status_from_form['name']}'
    logger.info('Task status data is populated correctly.')
    
    
# Проверка, что измененные данные сохраняются
def test_new_task_status_data_saved_success(driver, logged_in_user):
    new_task_status_data = TASK_STATUSES[1]
    
    menu = Menu(driver)
    menu.go_to(menu.PAGES['task_statuses'])
       
    task_status_page = TaskStatusesPage(driver)
    edit_task_status_page = EditTaskStatusesPage(driver)
    
    task_status_id = task_status_page.get_random_id()
    
    # Получение данных из таблицы, на которого нажали, так же переход на редактирование
    task_status_page.click_on_record(task_status_id)
    
    logger.info(f'Click to task status with ID {task_status_id}: {new_task_status_data['name']} {new_task_status_data['slug']}')
    
    # Ввод новых данных и нажатие "сохранить"
    edit_task_status_page.set_task_status_data(new_task_status_data)
    
    # Получаем данные из таблицы для проверки, что данные сохранились
    task_staus_data = task_status_page.click_on_record(task_status_id)
    
    assert task_staus_data == new_task_status_data, f'selected for editing {task_staus_data}, and the current task status {new_task_status_data}'
    logger.info('Update task status data success')


def test_remove_task_status_successful(driver, logged_in_user):  
    menu = Menu(driver)
    menu.go_to(menu.PAGES['task_statuses'])
       
    task_status_page = TaskStatusesPage(driver)
    
    # Парсим таблицу
    task_statuses_before_deletion = task_status_page.table_parse()
    task_statuses_before_deletion_count = len(task_statuses_before_deletion)
    logger.info(f'Task status in the table before deletion: {task_statuses_before_deletion_count}')
    
    # Если таблица пуста, пропускаем тест
    if task_statuses_before_deletion_count == 0:
        pytest.skip("Cannot run test: no task status available in the table.")
      
    task_status_id = task_status_page.get_random_id()
    # Получаем данные выделенного пользователя
    selected_task_status = task_status_page.select_record(task_status_id)
    logger.info(f'Select task staus with ID = {task_status_id}')
    
    # Удаляем выделенную запись
    task_status_page.click_to_delete()
    logger.info('Click to "Delete"')
    
    # Снова парсим таблицу
    task_status_after_deletion = task_status_page.table_parse()
    task_status_after_deletion_count = len(task_status_after_deletion)
    logger.info(f'Users in the table after deletion: {task_status_after_deletion_count}')
    
    assert (task_statuses_before_deletion_count - 1) == task_status_after_deletion_count, 'The number of task status in the table does not match.'
    
    # Проверяем, что удаленный пользователь отсутствует в таблице
    assert not any(
        t['name'] == selected_task_status['name']
        and t['slug'] == selected_task_status['slug']
        for t in task_status_after_deletion
    ), 'The task status has been deleted but still appears in the table.'
    
    logger.info('The task status has been successfully removed from the table.')


def test_remove_all_task_statuses_successful(driver, logged_in_user):
    menu = Menu(driver)
    menu.go_to(menu.PAGES['task_statuses'])
       
    task_status_page = TaskStatusesPage(driver)
    task_statuses = task_status_page.table_parse()
    task_statuses_count = len(task_statuses)
    
    task_status_page.select_all_records()
    logger.info('Select all task statuses in the table.')
    
    # Удаляем выделенных пользователей
    task_status_page.click_to_delete()
    logger.info('Click to "Delete"')
      
    assert f'{task_statuses_count} elements deleted' in task_status_page.get_alert_text() 
    assert task_status_page.records_is_missing(), 'The "No Task statuses yet" message is missing. Perhaps not all task statuses have been deleted.'
    logger.info('All task statuses have been successfully deleted.')
    
    
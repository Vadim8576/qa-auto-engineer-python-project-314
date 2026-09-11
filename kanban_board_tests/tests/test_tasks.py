import logging

import pytest

import time

from kanban_board_tests.data.tasks import TASK_DATA
from kanban_board_tests.pages.menu_component import Menu
from kanban_board_tests.pages.tasks.tasks_page import TasksPage
from kanban_board_tests.pages.tasks.edit_task_page import EditTaskPage
from kanban_board_tests.pages.tasks.task_creation_page import TaskCreationPage



from selenium.webdriver.common.by import By



logger = logging.getLogger(__name__)

def test_creation_task(driver, logged_in_user):

    menu = Menu(driver)
    menu.go_to(menu.PAGES['tasks'])
        
    task_page = TasksPage(driver)
    
    assert task_page.is_opened()
    
    task_page.click_create()
    logger.info('Button "Create task" pressed')
        
    task_creation = TaskCreationPage(driver)
    
    assert task_creation.is_opened()
    logger.info('The task creation page is open')
    
    assert 'Create Task' in task_creation.header_text()
    
    # Создаем Task (выбираем исполнителя, статус задачи, вводим title, description)
    random_assignee = task_creation.get_random_assignee_option()
    random_status = task_creation.get_random_status_option()
    logger.info(f'Select assignee: {random_assignee}')     
    logger.info(f'Select status: {random_status}')
    
    
    new_task_data = {
        'title': TASK_DATA[0]['title'],
        'description': TASK_DATA[0]['description'],
        'assignee': random_assignee,
        'status': random_status
    }
    
    task_creation.set_task_data(new_task_data)
    
    
     
    assert task_creation.get_alert_text() == 'Element created'
    logger.info(f'Task created!')
    
    menu.go_to(menu.PAGES['tasks'])
    
    # Парсим колонку со статусом random_status, в которой создали Task
    task_list = task_page.get_task_list_by_status(random_status)
    parse_task_list = task_page.get_parse_task_list(task_list)
    
    # Проверяем, что карточка с title и description появилась в нужной колонке
    title, description = TASK_DATA[0]['title'], TASK_DATA[0]['description']
    assert task_page.has_task(parse_task_list, title, description), 'The created card is not in the required column.'
    logger.info('The card has been successfully created in the appropriate column.')  
    

    
    
def test_edit_task_success(driver, logged_in_user):
    menu = Menu(driver)
    menu.go_to(menu.PAGES['tasks'])
    
    task_page = TasksPage(driver)
    edit_task_page = EditTaskPage(driver)
    
    # ищем первую карточку для редактирования в одном из столбцов
    task = task_page.find_first_available_task()
    task_page.click_edit(task)
    # Получаем данные из редактируемой карточки
    start_task_data = edit_task_page.get_task_data_from_form()
    
    logger.info(start_task_data)
    
    
    new_task_data = {
        'title': TASK_DATA[1]['title'],
        'description': TASK_DATA[1]['description'],
        
    }
    
    edit_task_page.set_task_data()
    
    
    
    # time.sleep(5)
    
    
    
    
      
'''   
    
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
    task_status_page.click_delete()
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
    task_status_page.click_delete()
    logger.info('Click to "Delete"')
      
    assert f'{task_statuses_count} elements deleted' in task_status_page.get_alert_text() 
    assert task_status_page.records_is_missing(), 'The "No Task statuses yet" message is missing. Perhaps not all task statuses have been deleted.'
    logger.info('All task statuses have been successfully deleted.')
    
'''
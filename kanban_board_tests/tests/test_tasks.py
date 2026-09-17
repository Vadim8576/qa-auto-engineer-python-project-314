import logging
import random

from kanban_board_tests.constants.menu_consts import MENU_LABELS
from kanban_board_tests.constants.task_consts import ID_TO_STATUS, STATUS_TO_ID
from kanban_board_tests.data.tasks import TASK_DATA
from kanban_board_tests.pages.menu_component import Menu
from kanban_board_tests.pages.task_statuses.task_statuses_page import TaskStatusesPage
from kanban_board_tests.pages.tasks.edit_task_page import EditTaskPage
from kanban_board_tests.pages.tasks.task_creation_page import TaskCreationPage
from kanban_board_tests.pages.tasks.tasks_page import TasksPage
from kanban_board_tests.pages.users.users_page import UsersPage

logger = logging.getLogger(__name__)

def test_creation_task(pages, logged_in_user):
    menu = pages(Menu)
    task_page = pages(TasksPage)
    task_creation = pages(TaskCreationPage)
    users_page = pages(UsersPage)
    task_statuses_page = pages(TaskStatusesPage)
        
    
    # Получаем рандомные assignees, statuses и создаем new_task_data
    menu.go_to(MENU_LABELS['users'])
             
    users = users_page.table_parse()    
    assignees = users_page.get_assignee(users)
    random_assignee = users_page.get_random_value(assignees)
        
    menu.go_to(MENU_LABELS['task_statuses'])

    statuses = task_statuses_page.table_parse()  
    task_status = task_statuses_page.get_tasks_statuses(statuses)
    random_status = task_statuses_page.get_random_value(task_status)
    
    logger.info(f'Select assignee: {random_assignee}')     
    logger.info(f'Select status: {random_status}')
    
    new_task_data = {
        'title': TASK_DATA[0]['title'],
        'description': TASK_DATA[0]['description'],
        'assignee': random_assignee,
        'status': random_status
    }

    menu.go_to(MENU_LABELS['tasks'])
        
    assert task_page.is_opened()
    
    task_page.click_create()
    logger.info('Button "Create task" pressed')
    
    assert task_creation.is_opened()
    logger.info('The task creation page is open')
    
    assert 'Create Task' in task_creation.header_text()

    # Заполняем форму новыми данными
    task_creation.set_task_data(new_task_data)
    
    assert task_creation.get_alert_text() == 'Element created'
    logger.info('Task created!')
    
    menu.go_to(MENU_LABELS['tasks'])
    
    # Парсим колонку со статусом random_status, в которой создали Task
    task_list = task_page.get_task_list_by_status(random_status)
    parse_task_list = task_page.get_parse_task_list(task_list)
    
    # Проверяем, что карточка с title и description появилась в нужной колонке
    title, description = TASK_DATA[0]['title'], TASK_DATA[0]['description']
    assert task_page.has_task(parse_task_list, title, description), 'The created card is not in the required column.'
    logger.info('The card has been successfully created in the appropriate column.')  
    
def test_edit_task_success(pages, logged_in_user):
    menu = pages(Menu)
    task_page = pages(TasksPage)
    edit_task_page = pages(EditTaskPage)
    users_page = pages(UsersPage)
    
    menu.go_to(MENU_LABELS['users'])
     
    users = users_page.table_parse()    
    assignees = users_page.get_assignee(users)
    
    random_assignee = edit_task_page.get_random_value(assignees)      
   
    menu.go_to(MENU_LABELS['tasks'])
     
    # ищем первую карточку для редактирования в одном из столбцов
    task = task_page.find_first_available_task()
    task_page.click_edit(task)
        
    # Получаем данные из редактируемой карточки
    start_task_data = edit_task_page.get_task_data_from_form() 
    new_task_data = {
        'title': TASK_DATA[1]['title'],
        'description': TASK_DATA[1]['description'],
        'assignee': random_assignee,
        'status': start_task_data['status'] # не меняем статус, чтобы карточка не улетела в другой столбец
    }  
    
    # Вводим новые данные в форму и сохраняем
    logger.info('Editing the form.')
    edit_task_page.set_task_data(new_task_data)
    logger.info('New data saved.')
    
    message_text = task_page.get_alert_text()
       
    # ищем ту же карточку, которую редактировали
    updated_task = task_page.find_first_available_task()
    # заходим в нее
    task_page.click_edit(updated_task)
    # Получаем данные из редактируемой карточки
    end_task_data = edit_task_page.get_task_data_from_form()
    
    assert 'Element updated' in message_text
    assert start_task_data != end_task_data, 'The data has not changed.'
    assert end_task_data == new_task_data, 'The data was not saved.'
    logger.info('The record with the new data has been successfully saved!')
    
def test_filter_by_status(pages, logged_in_user): 
    menu = pages(Menu)
    task_page = pages(TasksPage)
    task_statuses_page = pages(TaskStatusesPage)
    
    menu.go_to(MENU_LABELS['task_statuses'])
     
    task_statuses = task_statuses_page.table_parse()
        
    task_statuses = task_statuses_page.get_task_statuses_from_users(task_statuses)
    

    menu.go_to(MENU_LABELS['tasks'])
    
    all_tasks_before = task_page.get_all_tasks()
    
    for name in task_statuses:      
        logger.info(f'Filter: {name}')
        task_page.select_status_filter(name)
        task_page.wait_for_task_count_change(len(all_tasks_before))      
        all_tasks_after_len = len(task_page.get_all_tasks())
        all_tasks_before_len = len(all_tasks_before)
        assert all_tasks_after_len < all_tasks_before_len, f'The filter should reduce the number of tasks. Expected: {all_tasks_after_len} < {all_tasks_before_len}'
        logger.info(f'Filter {name} has triggered.')
        
def test_filter_by_assignee(pages, logged_in_user): 
    menu = pages(Menu)
    task_page = pages(TasksPage)
    users_page = pages(UsersPage)

    menu.go_to(MENU_LABELS['users'])
 
    users = users_page.table_parse()
    
    assignee = users_page.get_assignee(users)
    logger.info(f'emails: {assignee}')
    
    menu.go_to(MENU_LABELS['tasks'])
    all_tasks_before = task_page.get_all_tasks()
    
    for email in assignee:      
        logger.info(f'Filter: {email}')
        task_page.select_assignee_filter(email)
        task_page.wait_for_task_count_change(len(all_tasks_before))
        all_tasks_after_len = len(task_page.get_all_tasks())
        all_tasks_before_len = len(all_tasks_before)
        assert len(all_tasks_after_len) < len(all_tasks_before_len), f'The filter should reduce the number of tasks. Expected: {all_tasks_after_len} < {all_tasks_before_len}'
        logger.info(f'Filter {email} has triggered.')

def test_filter_by_label(pages, logged_in_user): 
    menu = pages(Menu)
    task_page = pages(TasksPage)

    menu.go_to(MENU_LABELS['tasks'])
 
    all_tasks_before = task_page.get_all_tasks()
    
    labels = task_page.get_all_labels()
    logger.info(f'labels: {labels}')
    
    for label in labels:      
        logger.info(f'Filter: {label}')
        task_page.select_label_filter(label)
        task_page.wait_for_task_count_change(len(all_tasks_before))   
        all_tasks_after_len = len(task_page.get_all_tasks())
        all_tasks_before_len = all_tasks_before
        assert all_tasks_after_len < all_tasks_before_len, f'The filter should reduce the number of tasks. Expected: {all_tasks_after_len} < {all_tasks_before_len}'
        logger.info(f'Filter {label} has triggered.')

def test_all_tasks_visability_and_clickable(pages, logged_in_user):
    menu = pages(Menu)
    task_page = pages(TasksPage)
    
    menu.go_to(MENU_LABELS['tasks'])
 
    logger.info('Checking if all tasks have been loaded.')
    assert task_page.are_all_tasks_visible()
    assert task_page.are_all_tasks_clickable()
    logger.info('All tasks have been successfully loaded.')


def test_moving_task_to_another_column(pages, logged_in_user):
    menu = pages(Menu)
    task_page = pages(TasksPage)

    menu.go_to(MENU_LABELS["tasks"])

    # Находим задачу для перетаскивания
    task = task_page.find_first_available_task()

    # Определяем исходную колонку
    source_column = task_page.get_status_column_by_task(task)
    source_column_id = task_page.get_status_column_id(source_column)
    logger.info(f'source column ID = {source_column_id}')
    source_column_status = ID_TO_STATUS[source_column_id]

    # Считаем задачи в исходной колонке ДО
    source_column_task_count_before = len(
        task_page.get_task_list_by_status(source_column_status)
    )

    # Выбираем случайную целевую колонку (не ту же самую)
    available_ids = [v for v in STATUS_TO_ID.values() if v != source_column_id]

    target_random_id = random.choice(available_ids)
    logger.info(f'target column ID = {target_random_id}')
    target_column_status = ID_TO_STATUS[target_random_id]

    # Считаем задачи в целевой колонке ДО
    target_column_task_count_before = len(
        task_page.get_task_list_by_status(target_column_status)
    )

    # Меняем статус
    task_page.click_edit(task)
    task_page.select_status_filter(target_column_status)
    task_page.click_save()
    
    # Получаем актуальные количества ПОСЛЕ
    actual_source_column_task_count_after = len(
        task_page.get_task_list_by_status(source_column_status)
    )
    actual_target_column_task_count_after = len(
        task_page.get_task_list_by_status(target_column_status)
    )

    # Ожидаемые значения
    expected_source_column_task_count_after = source_column_task_count_before - 1
    expected_target_column_task_count_after = target_column_task_count_before + 1

    assert actual_source_column_task_count_after == expected_source_column_task_count_after, (
        f'Source column task count mismatch: got {actual_source_column_task_count_after}, '
        f'expected {expected_source_column_task_count_after}. '
        f'Before: {source_column_task_count_before}'
    )
    logger.info('The current number of tasks in the source column matches the expected value.')

    assert actual_target_column_task_count_after == expected_target_column_task_count_after, (
        f'Target column task count mismatch: got {actual_target_column_task_count_after}, '
        f'expected {expected_target_column_task_count_after}. '
        f'Before: {target_column_task_count_before}'
    )
    logger.info('The current number of tasks in the target column matches the expected value.')


def test_remove_task_successful(pages, logged_in_user):
    menu = pages(Menu)
    task_page = pages(TasksPage)
    edit_task_page = pages(EditTaskPage)
    
    menu.go_to(MENU_LABELS["tasks"])
    
    task = task_page.find_first_available_task()
    status_column = task_page.get_status_column_by_task(task)
    status_column_id = task_page.get_status_column_id(status_column)
    tasks_count_before = task_page.get_task_count_in_column(status_column)
    logger.info(f'Number of tasks before deletion = {tasks_count_before}')
    
    task_page.click_edit(task)
    edit_task_page.click_delete()
    
    task_page.wait_for_task_removal_in_column_by_id(status_column_id, tasks_count_before)
    
    updated_status_column = task_page.get_status_column_by_id(status_column_id)

    tasks_count_after = task_page.get_task_count_in_column(updated_status_column)
    logger.info(f'Number of tasks after deletion = {tasks_count_after}')
    
    assert (tasks_count_before - 1) == tasks_count_after, 'The number of tasks does not match.  Expected: {tasks_count_before - 1} == {tasks_count_after}'
    
    logger.info('The task has been successfully deleted.')
    

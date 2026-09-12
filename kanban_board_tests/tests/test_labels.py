import logging

import pytest

from kanban_board_tests.data.labels import LABELS_DATA
from kanban_board_tests.constants.menu_consts import MENU_LABELS
from kanban_board_tests.pages.labels.edit_label_page import EditLabelPage
from kanban_board_tests.pages.labels.label_creation_page import LabelCreationPage
from kanban_board_tests.pages.labels.labels_page import LabelsPage
from kanban_board_tests.pages.menu_component import Menu

logger = logging.getLogger(__name__)

def test_creation_label(driver, logged_in_user):
    logger.info('Test creation label')
    menu = Menu(driver)
    menu.go_to(MENU_LABELS['labels'])
        
    labels_page = LabelsPage(driver)
    assert labels_page.is_opened()
        
    labels_page.click_create()
    logger.info('Button "Create label" pressed')
        
    label_creation = LabelCreationPage(driver)
    label_creation.is_opened()
    assert 'Create Label' in label_creation.header_text()
              
    label = LABELS_DATA[0]
        
    label_creation.set_label_data(label)
    logger.info(f'Create label {label}')
    
    menu.go_to(MENU_LABELS['labels'])
        
    assert labels_page.is_record_added(label), f'Label {label} not found'
    logger.info(f'Label {label} added successfully!')


def test_labels_table_is_visibility(driver, logged_in_user):
    menu = Menu(driver)
    menu.go_to(MENU_LABELS['labels'])
    labels_page = LabelsPage(driver)
    assert labels_page.table_loads(), 'Labels table not loaded!'

    parsed_records = labels_page.table_parse()
    assert len(parsed_records) > 0, 'Labels not found!'
    logger.info('Labels table loaded')

    missing_issues = []

    for i, u in enumerate(parsed_records):
        line_no = i + 1

        name = u.get('name')
        if not name or (isinstance(name, str) and not name.strip()):
            missing_issues.append(f"Line {line_no}: missing/empty 'name'")

    if missing_issues:
        error_msg = "; ".join(missing_issues)
        assert False, f"Found {len(missing_issues)} data issues:\n{error_msg}"
    else:
        logger.info('All required fields are present and non-empty')


def test_edit_user_success(driver, logged_in_user):
    menu = Menu(driver)
    menu.go_to(MENU_LABELS['labels'])
    labels_page = LabelsPage(driver)
    label_id = labels_page.get_random_id()
    
    if label_id is None:
        pytest.skip("Cannot run test: no labels available in the table.")
     
    logger.info(f'Label with ID = {label_id}')
    
    selected_label = labels_page.click_on_record(label_id)
    logger.info(f'Click to label with ID {label_id}: {selected_label['name']}')

    
    edit_label_page = EditLabelPage(driver)
    assert edit_label_page.is_opened(label_id), f'Expected edit page for label {label_id}, but condition is False'
    logger.info(f'Open edit page label {label_id}')
    
    assert f'Label {selected_label['name']}' in edit_label_page.header_text(), f'This is not an edit page {selected_label['name']}'

    # Проверка на совпадение данных из формы с данными редактируемого пользователя
    label_from_form = edit_label_page.get_label_data_from_form()
    assert label_from_form == selected_label, f'selected for editing {selected_label['name']}, and the current label {label_from_form['name']}'
    logger.info('Label data is populated correctly.')
    

# Проверка, что измененные данные сохраняются
def test_new_label_data_saved_success(driver, logged_in_user):
    new_label_data = LABELS_DATA[1]
    
    menu = Menu(driver)
    menu.go_to(MENU_LABELS['labels'])
    labels_page = LabelsPage(driver)
    edit_label_page = EditLabelPage(driver)
    label_id = labels_page.get_random_id()
       
    # Получение данных пользователя из таблицы, на которого нажали, так же переход на редактирование
    label_data = labels_page.click_on_record(label_id)
    
    logger.info(f'Click to label with ID {label_id}: {label_data}')
    
    # Ввод новых данных и нажатие "сохранить"
    edit_label_page.set_label_data(new_label_data)
    
    # Получаем данные этого же пользователя из таблицы, для проверки, что данные сохранились
    label_data = labels_page.click_on_record(label_id)
    
    assert label_data['name'] == new_label_data, f'selected for editing {label_data}, and the current label {new_label_data}'
    logger.info('Update label data success')
    

def test_remove_label_successful(driver, logged_in_user):  
    menu = Menu(driver)
    menu.go_to(MENU_LABELS['labels'])
    labels_page = LabelsPage(driver)
    
    # Парсим таблицу
    labels_before_deletion = labels_page.table_parse()
    labels_before_deletion_count = len(labels_before_deletion)
    logger.info(f'Labels in the table before deletion: {labels_before_deletion_count}')
    
    # Если таблица пуста, пропускаем тест
    if labels_before_deletion_count == 0:
        pytest.skip("Cannot run test: no labels available in the table.")
      
    label_id = labels_page.get_random_id()
    # Получаем данные выделенного пользователя
    selected_label = labels_page.select_record(label_id)
    logger.info(f'Select label with ID = {label_id}')
    
    # Удаляем выделенного пользователя
    labels_page.click_delete()
    logger.info('Click to "Delete"')
    
    # Снова парсим таблицу
    labels_after_deletion = labels_page.table_parse()
    labels_after_deletion_count = len(labels_after_deletion)
    logger.info(f'Users in the table after deletion: {labels_after_deletion_count}')
    
    assert (labels_before_deletion_count - 1) == labels_after_deletion_count, 'The number of labels in the table does not match.'
    
    # Проверяем, что удаленный пользователь отсутствует в таблице
    assert not any(
        l['name'] == selected_label['name']
        for l in labels_after_deletion
    ), 'The label has been deleted but still appears in the table.'
    
    logger.info('The label has been successfully removed from the table.')


def test_remove_all_labels_successful(driver, logged_in_user):
    menu = Menu(driver)
    menu.go_to(MENU_LABELS['labels'])
    labels_page = LabelsPage(driver)
    
    labels = labels_page.table_parse()
    labels_count = len(labels)
    
    labels_page.select_all_records()
    logger.info('Select all labels in the table.')
    
    # Удаляем выделенну метки
    labels_page.click_delete()
    logger.info('Click to "Delete"')
      
    assert f'{labels_count} elements deleted' in labels_page.get_alert_text() 
    assert labels_page.records_is_missing(), 'The "No Labels yet" message is missing. Perhaps not all labels have been deleted.'
    logger.info('All labels have been successfully deleted.')
    
    

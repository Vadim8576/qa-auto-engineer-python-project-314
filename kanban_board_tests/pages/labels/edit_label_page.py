import logging

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.labels_locators import LabelsLocators
from kanban_board_tests.pages.locators.table_locators import TableLocators

logger = logging.getLogger(__name__)

class EditLabelPage(BasePage):
    def is_opened(self, label_id):
        return f'/labels/{label_id}' in self.current_url
    
    def get_label_data_from_form(self):
        name = self.value_of(LabelsLocators.NAME)
        return {
            'name': name
        }
    
    def set_label_name(self, name):
        self.type(LabelsLocators.NAME, name)
    
    def click_save(self):
        self.click(TableLocators.SAVE_BUTTON)
        
    def set_label_data(self, new_label_data):
        self.set_label_name(new_label_data)
        self.click_save()
    
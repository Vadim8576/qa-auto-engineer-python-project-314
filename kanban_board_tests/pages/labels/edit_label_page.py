import logging

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.labels_locators import LabelsLocators
from kanban_board_tests.mixins.labels_mixin import LabelsMixin
from kanban_board_tests.mixins.table_mixin import TableMixin

logger = logging.getLogger(__name__)

class EditLabelPage(BasePage, LabelsMixin, TableMixin):
    def is_opened(self, label_id):
        return f'/labels/{label_id}' in self.current_url
    
    def get_label_data_from_form(self):
        name = self.value_of(LabelsLocators.NAME)
        return {
            'name': name
        }
    
    def set_label_name(self, name):
        self.type(LabelsLocators.NAME, name)
        
    def set_label_data(self, new_label_data):
        self.set_label_name(new_label_data)
        self.click_save()
    
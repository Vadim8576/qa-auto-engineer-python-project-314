

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.locators.labels_locators import LabelsLocators
from kanban_board_tests.pages.locators.table_locators import TableLocators


class LabelCreationPage(BasePage):
    def is_opened(self):
        return '/labels/create' in self.current_url
        
    def create(self, label_data):
        self.type(LabelsLocators.NAME, label_data)
        self.click(TableLocators.SAVE_BUTTON)
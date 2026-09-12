import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.locators.labels_locators import (
    LabelsLocators,
)
from kanban_board_tests.pages.locators.table_locators import (
    TableLocators,
)

class LabelsMixin:
    def set_label_name(self, name):
            self.type(LabelsLocators.NAME, name)
            
    def set_label_data(self, new_label_data):
        self.set_label_name(new_label_data)
        self.click_save()
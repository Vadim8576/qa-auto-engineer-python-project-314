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
    def create(self, label_data):
        self.type(LabelsLocators.NAME, label_data)
        self.click(TableLocators.SAVE_BUTTON)
from kanban_board_tests.pages.locators.labels_locators import (
    LabelsLocators,
)


class LabelsMixin:
    def set_label_name(self, name):
            self.type(LabelsLocators.NAME, name)
            
    def set_label_data(self, label_data):
        self.set_label_name(label_data)
        self.click_save()
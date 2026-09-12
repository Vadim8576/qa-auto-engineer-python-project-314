from kanban_board_tests.pages.locators.task_statuses_locators import (
    TaskStatusesLocators,
)


class TaskStatusesMixin:
    def set_task_status_name(self, name):
        self.type(TaskStatusesLocators.NAME, name)
    
    def set_task_status_slug(self, slug):
        self.type(TaskStatusesLocators.SLUG, slug)
        
    def set_task_status_data(self, task_status_data):
        self.set_task_status_name(task_status_data['name'])
        self.set_task_status_slug(task_status_data['slug'])
        self.click_save()
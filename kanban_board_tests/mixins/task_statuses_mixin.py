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
    
    def get_task_statuses_from_users(self, task_statuses):
            statuses = []
            for t in task_statuses:
                statuses.append(t['name'])
            return statuses
    
    def get_tasks_statuses(self, task_statuses):
            statuses = []
            for ts in task_statuses:
                statuses.append(ts['name'])
            return statuses
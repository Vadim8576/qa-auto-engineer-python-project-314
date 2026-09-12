import logging

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.mixins.tasks_mixin import TaksMixin

logger = logging.getLogger(__name__)

class TaskCreationPage(BasePage, TaksMixin):
    PATH = '/tasks/create'
    def is_opened(self):
        return self.PATH in self.current_url
        
    

    
    

    
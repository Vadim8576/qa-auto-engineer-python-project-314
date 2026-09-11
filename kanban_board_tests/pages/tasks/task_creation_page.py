import logging

from kanban_board_tests.pages.base_page import BasePage
from kanban_board_tests.pages.tasks.tasks_mixin import TaksMixin

logger = logging.getLogger(__name__)

class TaskCreationPage(BasePage, TaksMixin):  
    def is_opened(self):
        return '/tasks/create' in self.current_url
        
    

    
    

    
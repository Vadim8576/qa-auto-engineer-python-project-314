import random
import logging
import time

from selenium.webdriver.support import expected_conditions as EC

from kanban_board_tests.pages.locators.tasks_locators import (
    TasksLocators,
)

logger = logging.getLogger(__name__)

class TaksMixin:
    def set_task_title(self, title):
        # self.type(TasksLocators.TITLE, title)
        el = self.wait.until(EC.element_to_be_clickable(TasksLocators.TITLE))
        self.driver.execute_script("""
            var el = arguments[0];
            el.value = arguments[1];
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        """, el, title)
        # Иногда полезно снять фокус, чтобы сработала валидация
        self.driver.execute_script("arguments[0].blur();", el)
    
    def set_task_description(self, description):
        self.type(TasksLocators.DESCRIPTION, description)
    
    def select_assignee(self, option):
        self.click_to_dropdown(TasksLocators.ASSIGNEE_COMBOBOX)
        self.click_to_option(option)
    
    def select_status(self, option):
        self.click_to_dropdown(TasksLocators.STATUS_COMBOBOX)
        self.click_to_option(option)
    
    def select_label(self, option):
        self.click_to_dropdown(TasksLocators.LABEL_COMBOBOX)
        self.click_to_option(option)
        
    def set_task_data(self, task_data):
        # self.set_task_title(task_data['title'])
        
        # self.set_task_description(task_data['description'])
        # self.select_assignee(task_data['assignee'])
        # self.select_status(task_data['status'])
        self.click_save()
    
    def get_options_list(self, locator):
        self.click_to_dropdown(locator)
        time.sleep(0.2)
        options = self.wait.until(EC.presence_of_all_elements_located(TasksLocators.LISTBOX_OPTION))   
        return [option.text.strip() for option in options]
    
    def get_random_option(self, locator):
        options = self.get_options_list(locator)
        filtered_options = [o for o in options if o and o.strip()]
        logger.info(f'option = {filtered_options}')
        if not filtered_options:
            return None
        random_option = random.choice(filtered_options)
        self.click_to_option(random_option)
        return random_option

    def get_random_assignee_option(self):
        return self.get_random_option(TasksLocators.ASSIGNEE_COMBOBOX)
    
    def get_random_status_option(self):
        return self.get_random_option(TasksLocators.STATUS_COMBOBOX)
    
    def click_to_dropdown(self, selector):
        trigger = self.driver.find_element(*selector)

        self.wait.until(lambda _: trigger.is_displayed() and trigger.is_enabled())
        try:
            trigger.click()
        except Exception:
            self.driver.execute_script('arguments[0].click();', trigger)               
    
    def click_to_option(self, option_text):
        self.click(TasksLocators.select_option(option_text))
from selenium.webdriver.common.by import By


class TasksLocators:
    PRESENTATION = (By.CSS_SELECTOR, 'div[role="presentation"]')
    
    ASSIGNEE_COMBOBOX = (By.XPATH, '//div[@role="combobox" and @id=//label[starts-with(normalize-space(), "Assignee")]/@for]')
    STATUS_COMBOBOX = (By.XPATH, '//div[@role="combobox" and @id=//label[starts-with(normalize-space(), "Status")]/@for]')
    LABEL_COMBOBOX = (By.XPATH, '//div[@role="combobox" and @id=//label[starts-with(normalize-space(), "Label")]/@for]')

    TITLE = (By.CSS_SELECTOR, 'input[name="title"]')
    DESCRIPTION = (By.CSS_SELECTOR, 'textarea[name="content"]')
    
    LISTBOX = (By.CSS_SELECTOR, 'ul[role="listbox"]')
    LISTBOX_OPTION = (By.CSS_SELECTOR, 'li[role="option"]')
    
    CARD_TITLE = (By.CSS_SELECTOR, '.MuiTypography-h5')
    CARD_DESCRIPTION = (By.CSS_SELECTOR, '.MuiTypography-body2')
    
    EDIT_BUTTON = (By.CSS_SELECTOR, 'a[aria-label="Edit"]')
    SHOW_BUTTON = (By.CSS_SELECTOR, 'a[aria-label="Show"]')
    
    TASK = (By.CSS_SELECTOR, 'div[role="button"]') 
    
    STATUS_COLUMNS = (By.CSS_SELECTOR, '[data-rfd-droppable-id]')
    TASKS = (By.CSS_SELECTOR, '[data-rfd-draggable-id]')
    
    @staticmethod
    def column_container(column_number):
        return (By.CSS_SELECTOR, f'[data-rfd-droppable-id="{column_number}"]')
    
    @staticmethod
    def select_option(option_text):
        return (By.XPATH, f"//li[normalize-space()='{option_text}']")
    
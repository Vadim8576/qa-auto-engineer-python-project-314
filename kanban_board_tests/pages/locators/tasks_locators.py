from selenium.webdriver.common.by import By


class TasksLocators:
    ASSIGNEE_COMBOBOX = (By.XPATH, '//div[@role="combobox" and @id=//label[starts-with(normalize-space(), "Assignee")]/@for]')
    STATUS_COMBOBOX = (By.XPATH, '//div[@role="combobox" and @id=//label[starts-with(normalize-space(), "Status")]/@for]')
    LABEL_COMBOBOX = (By.XPATH, '//div[@role="combobox" and @id=//label[normalize-space()="Label"]/@for]')
    TITLE = (By.CSS_SELECTOR, 'input[name="title"]')
    CONTENT = (By.CSS_SELECTOR, 'textarea[name="content"]')
    PRESENTATION = (By.CSS_SELECTOR, 'div[role="presentation"]')
    LISTBOX = (By.CSS_SELECTOR, 'ul[role="listbox"]')
    LISTBOX_OPTION = (By.CSS_SELECTOR, 'li[role="option"]')
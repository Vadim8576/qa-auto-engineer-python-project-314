from kanban_board_tests.pages.users_page import UsersPage
from kanban_board_tests.pages.user_creation_page import UserCreationPage


def create(driver, page, user_data):     
    page.click_to_create()       
    
    user_creation = UserCreationPage(driver)
    user_creation.create_user(user_data)
    
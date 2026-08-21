import logging
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from kanban_board_tests.pages.login_page import LoginPage

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("APP_BASE_URL", "http://localhost:5173")

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--window-size=1366,768")
    # options.add_argument("--headless=new")          # без окна
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")            # важно в контейнерах/WSL
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options) 

    yield driver
    driver.quit()

@pytest.fixture
def pages(driver, base_url):
    def _factory(PageCls):
        return PageCls(driver, base_url)
    return _factory

@pytest.fixture(scope="module")
def logged_in_user(driver, base_url):
    login = LoginPage(driver)
    logger.info("Opening login page: %s", base_url)
    login.open(base_url)
    login.login("Alex", "Password!")
    logger.info('Logged in as Alex')
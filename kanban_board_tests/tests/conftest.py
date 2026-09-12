import logging
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from kanban_board_tests.pages.login.login_page import LoginPage

# --- Вычисляем абсолютные пути относительно conftest.py ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LOG_DIR = os.path.join(BASE_DIR, "logs")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
LOG_FILE = os.path.join(LOG_DIR, "tests.log")

# Создаём папки, если их нет
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("APP_BASE_URL", "http://localhost:5173")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    setattr(item, "rep_" + result.when, result)

@pytest.fixture(scope="module")
def driver(request):
    options = Options()
    options.add_argument("--window-size=1366,768")
    # options.add_argument("--headless=new")          # без окна
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")            # важно в контейнерах/WSL
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    yield driver
    
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        name = request.node.name
        # Нормализуем имя теста, чтобы избежать ошибок с недопустимыми символами
        safe_name = "".join(c if c.isalnum() or c == "_" else "_" for c in name)
        png_path = os.path.join(SCREENSHOT_DIR, f"{safe_name}.png")
        html_path = os.path.join(SCREENSHOT_DIR, f"{safe_name}.html")
        driver.save_screenshot(png_path)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
    driver.quit()

@pytest.fixture
def pages(driver, base_url):
    def _factory(PageCls):
        return PageCls(driver, base_url)
    return _factory

@pytest.fixture(scope="function")
def logged_in_user(driver, base_url, pages):
    login = pages(LoginPage)
    logger.info("Opening login page: %s", base_url)
    login.open(base_url)
    login.login("Alex", "Password!")
    logger.info('Logged in as Alex')

@pytest.fixture(autouse=True)
def setup_logging():
    logging.info("=== Begin test ===")
    yield
    logging.info("=== End test ===")
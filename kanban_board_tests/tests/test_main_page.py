from selenium import webdriver


def test_main_page():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")          # без окна
    options.add_argument("--no-sandbox")            # важно в контейнерах/WSL
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost:5173")
    print(driver.title)
    
    assert 'wrong_text' in driver.title
    
    driver.quit()
    
    
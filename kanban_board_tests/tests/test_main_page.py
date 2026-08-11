from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_main_page(driver, base_url):
    driver.get(base_url)
    
    TIME_OUT = 5
    wait = WebDriverWait(driver, TIME_OUT)
    
    try:
        assert 'Task manager' in driver.title
        
        wait.until(EC.presence_of_element_located((By.ID, ":r4:")))        
        wait.until(EC.presence_of_element_located((By.ID, ":r6:")))        
        
        submit_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[type="submit"]'))
        )
        
        assert 'SIGN IN' in submit_button.text
        
        
        
    except Exception as e:
        print('Ошибка:', e)
        raise
    
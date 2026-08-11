def test_main_page(driver, base_url):
    driver.get(base_url)
    
    try:
        assert 'Task manager' in driver.title
    except Exception as e:
        print("Ошибка:", e)
        raise
    
    
    
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def test_arms_18_management_dashboard_overview():
    driver = webdriver.Chrome()
    try:
        driver.get("http://127.0.0.1:5500")
        driver.maximize_window()

        driver.find_element(By.ID, "email").send_keys("michael@altrium.com")
        driver.find_element(By.ID, "password").send_keys("Test1234")
        driver.find_element(By.ID, "loginBtn").click()

        WebDriverWait(driver, 20).until(
            EC.url_contains("management-dashboard")
        )

        assert "management-dashboard" in driver.current_url.lower()
        print("ARMS-18: management dashboard opened")
        time.sleep(2)
    finally:
        driver.quit()

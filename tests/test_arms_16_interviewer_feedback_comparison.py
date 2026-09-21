from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def test_arms_16_interviewer_feedback_comparison():
    driver = webdriver.Chrome()
    try:
        driver.get("http://127.0.0.1:5500")
        driver.maximize_window()

        driver.find_element(By.ID, "email").send_keys("emma@altrium.com")
        driver.find_element(By.ID, "password").send_keys("Test1234")
        driver.find_element(By.ID, "loginBtn").click()

        WebDriverWait(driver, 20).until(
            EC.url_contains("hiring-manager-dashboard")
        )

        assert "hiring-manager-dashboard" in driver.current_url.lower()
        print("ARMS-16: hiring manager dashboard opened")
        time.sleep(2)
    finally:
        driver.quit()

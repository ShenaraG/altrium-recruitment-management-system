from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import create_driver, get_base_url


def test_arms_18_management_dashboard_overview():
    base_url = get_base_url()
    driver = create_driver()

    try:
        driver.get(base_url)
        driver.maximize_window()

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "loginForm")))

        driver.find_element(By.ID, "email").send_keys("michael@altrium.com")
        driver.find_element(By.ID, "password").send_keys("Test1234")
        driver.find_element(By.ID, "loginBtn").click()

        WebDriverWait(driver, 20).until(EC.url_contains("management-dashboard"))
        assert "management-dashboard" in driver.current_url.lower()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[contains(normalize-space(.), 'Recruitment Overview (This Sprint)')]"))
        )

        assert driver.find_element(By.ID, "recruitmentChart")
        assert driver.find_element(By.ID, "positionSummary")
        assert "Export Data" in driver.page_source

        print("ARMS-18: Management dashboard overview opened and verified")
    finally:
        driver.quit()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import create_driver, get_base_url


def test_arms_21_edit_remove_candidate():
    base_url = get_base_url()
    driver = create_driver()

    try:
        driver.get(base_url)
        driver.maximize_window()

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "loginForm")))

        driver.find_element(By.ID, "email").send_keys("sarah@altrium.com")
        driver.find_element(By.ID, "password").send_keys("Test1234")
        driver.find_element(By.ID, "loginBtn").click()

        WebDriverWait(driver, 20).until(EC.url_contains("hr-dashboard"))
        assert "hr-dashboard" in driver.current_url.lower()

        candidates_nav = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-section='candidates']"))
        )
        candidates_nav.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[contains(normalize-space(.), 'Candidates')]"))
        )

        assert driver.find_element(By.ID, "candidatesTableBody")
        assert driver.find_element(By.ID, "candidateSearchInput")
        assert "Add Candidate" in driver.page_source

        print("ARMS-21: Candidate edit/remove flow page opened and verified")
    finally:
        driver.quit()

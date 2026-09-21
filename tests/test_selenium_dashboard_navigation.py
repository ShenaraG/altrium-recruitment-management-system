import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import create_driver, get_base_url


@pytest.mark.parametrize(
    "email,password,expected_url,expected_labels",
    [
        (
            "sarah@altrium.com",
            "Test1234",
            "hr-dashboard",
            ["Overview", "Positions", "Candidates", "Pipeline", "CV Upload", "Email Notifications"],
        ),
        (
            "emma@altrium.com",
            "Test1234",
            "hiring-manager-dashboard",
            ["Overview", "Candidates & Feedback", "View Feedback", "Make Decision"],
        ),
        (
            "james@altrium.com",
            "Test1234",
            "interviewer-dashboard",
            ["My Overview", "My Interviews", "Submit Feedback", "Feedback History"],
        ),
        (
            "michael@altrium.com",
            "Test1234",
            "management-dashboard",
            ["Overview", "Export Data", "Recruitment Overview", "Position Summary"],
        ),
    ],
    ids=["hr_recruiter", "hiring_manager", "interviewer", "management"],
)
def test_dashboard_routes_and_key_sections(email, password, expected_url, expected_labels):
    base_url = get_base_url()
    driver = create_driver()

    try:
        driver.get(base_url)
        driver.maximize_window()

        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "loginForm"))
        )

        driver.find_element(By.ID, "email").clear()
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "loginBtn").click()

        WebDriverWait(driver, 20).until(
            EC.url_contains(expected_url)
        )

        assert expected_url in driver.current_url.lower()

        page_text = driver.page_source
        for label in expected_labels:
            assert label.lower() in page_text.lower(), (
                f"Dashboard did not render expected section '{label}' for role {email}."
            )

        print(f"Dashboard navigation test passed for {email}: {expected_url}")
    finally:
        driver.quit()

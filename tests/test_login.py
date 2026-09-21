from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_login_page_loads(live_server, driver):
    driver.get(f"{live_server}/index.html")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.title_contains("ALTRIUM"))

    assert "ALTRIUM - Secure Login" in driver.title

    login_form = wait.until(EC.presence_of_element_located((By.ID, "loginForm")))
    email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "loginBtn")

    assert login_form.is_displayed()
    assert email_input.is_displayed()
    assert password_input.is_displayed()
    assert login_button.is_displayed()
    assert email_input.get_attribute("type") == "email"
    assert password_input.get_attribute("type") == "password"


def test_login_form_requires_email_and_password(live_server, driver):
    driver.get(f"{live_server}/index.html")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "loginForm")))

    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "password")

    assert email_input.get_attribute("required") == "true"
    assert password_input.get_attribute("required") == "true"

    email_input.clear()
    password_input.clear()
    driver.find_element(By.ID, "loginBtn").click()

    assert driver.execute_script(
        "return document.activeElement === document.getElementById('email') || document.activeElement === document.getElementById('password')"
    )


def test_login_page_has_expected_branding(live_server, driver):
    driver.get(f"{live_server}/index.html")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

    heading = driver.find_element(By.TAG_NAME, "h1")
    subtitle = driver.find_element(By.CLASS_NAME, "subtitle")
    footer = driver.find_element(By.CLASS_NAME, "login-footer")

    assert "ALTRIUM" in heading.text
    assert "Recruitment & Hiring Tracker" in subtitle.text
    assert "ALTRIUM Recruitment and Hiring Tracker" in footer.text

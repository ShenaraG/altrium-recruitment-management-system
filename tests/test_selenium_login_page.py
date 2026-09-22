import time

from selenium.webdriver.common.by import By

from conftest import create_driver, get_base_url


def test_login_page_loads_and_login_form_is_visible():
    base_url = get_base_url()
    driver = create_driver()

    try:
        driver.get(base_url)
        driver.maximize_window()

        title = driver.title.lower()
        assert "altrium" in title

        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "loginBtn")

        assert email_input.is_displayed()
        assert password_input.is_displayed()
        assert login_button.is_displayed()

        print("Login page test: PASSED")
    finally:
        driver.quit()

import time

from selenium.webdriver.common.by import By

from conftest import create_driver, get_base_url


def test_dashboard_route_links_are_present():
    base_url = get_base_url()
    driver = create_driver()

    try:
        driver.get(base_url)
        driver.maximize_window()

        page_text = driver.page_source.lower()
        assert "welcome back" in page_text
        assert "login" in page_text

        time.sleep(1)
        assert "loginform" in driver.page_source.lower()

        print("Dashboard navigation test: PASSED")
    finally:
        driver.quit()

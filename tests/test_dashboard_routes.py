import os

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from conftest import DASHBOARD_ROUTES


@pytest.mark.parametrize("role, path, expected_labels", DASHBOARD_ROUTES)
def test_all_dashboard_routes_redirect_to_login_when_not_authenticated(live_server, driver, role, path, expected_labels):
    driver.get(f"{live_server}/{path}")

    WebDriverWait(driver, 10).until(
        lambda d: "index.html" in d.current_url or d.title == "ALTRIUM - Secure Login"
    )

    assert "index.html" in driver.current_url or "ALTRIUM - Secure Login" in driver.title


@pytest.mark.parametrize("role, path, expected_labels", DASHBOARD_ROUTES)
def test_dashboard_files_define_expected_sections(role, path, expected_labels):
    file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), path)
    with open(file_path, "r", encoding="utf-8") as dashboard_file:
        content = dashboard_file.read()

    assert "REQUIRED_ROLE" in content
    assert "ALTRIUM" in content
    for label in expected_labels:
        assert label in content

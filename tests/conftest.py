import os
from urllib.error import URLError
from urllib.request import urlopen

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _read(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def get_base_url():
    """Find a locally running copy of the app (static file server).

    Set ALTRIUM_BASE_URL to point at a specific host, otherwise the
    common local dev server ports/hosts are probed. If nothing is
    listening, the tests skip rather than fail, since these are live
    end-to-end tests that need a running server + a reachable Supabase
    project (real network, real test-account data).
    """
    env_url = os.environ.get("ALTRIUM_BASE_URL")
    candidates = [env_url] if env_url else []
    candidates.extend([
        "http://localhost:5500",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:8000",
    ])

    for candidate in candidates:
        if not candidate:
            continue
        try:
            with urlopen(candidate, timeout=2):
                return candidate.rstrip("/")
        except (URLError, ValueError):
            continue

    pytest.skip(
        "No local ALTRIUM app server was found. Start a local web server "
        "(e.g. `python -m http.server 8000`) or set ALTRIUM_BASE_URL."
    )


def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1200")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as exc:  # pragma: no cover - environment-dependent
        pytest.skip(f"ChromeDriver is not available for Selenium tests: {exc}")


# Seeded test accounts used across the tests. These must exist in the
# Supabase project the app under test points at (see config.js).
TEST_ACCOUNTS = {
    "hr_recruiter": ("sarah@altrium.com", "Test1234", "hr-dashboard"),
    "interviewer": ("james@altrium.com", "Test1234", "interviewer-dashboard"),
    "hiring_manager": ("emma@altrium.com", "Test1234", "hiring-manager-dashboard"),
    "management": ("michael@altrium.com", "Test1234", "management-dashboard"),
}


def login_as(driver, base_url, role, timeout=20):
    """Log in as one of the seeded test accounts and wait for the
    matching dashboard to load. Returns the dashboard URL fragment.
    """
    email, password, dashboard_fragment = TEST_ACCOUNTS[role]

    driver.get(f"{base_url}/index.html")
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "loginForm")))

    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "loginBtn").click()

    WebDriverWait(driver, timeout).until(EC.url_contains(dashboard_fragment))
    assert dashboard_fragment in driver.current_url.lower()
    return dashboard_fragment


def go_to_section(driver, section, heading_text, timeout=10):
    """Click a left-nav item (data-section=...) and wait for its
    heading to become visible.
    """
    nav = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"button[data-section='{section}']"))
    )
    nav.click()
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//h2[contains(normalize-space(.), '{heading_text}')]")
        )
    )


def accept_alert(driver, timeout=10, send_keys=None):
    """Wait for a native alert/confirm/prompt, optionally type into it,
    then accept it. Returns the alert text.
    """
    WebDriverWait(driver, timeout).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    text = alert.text
    if send_keys is not None:
        alert.send_keys(send_keys)
    alert.accept()
    return text


def dismiss_alert(driver, timeout=10):
    WebDriverWait(driver, timeout).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    text = alert.text
    alert.dismiss()
    return text

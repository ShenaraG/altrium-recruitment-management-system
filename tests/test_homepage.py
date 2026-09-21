import os
import socket
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DASHBOARD_ROUTES = [
    ("hr_recruiter", "dashboards/hr-dashboard.html", ["Overview", "Positions", "Candidates", "Pipeline", "CV Upload"]),
    ("interviewer", "dashboards/interviewer-dashboard.html", ["My Overview", "My Interviews", "Submit Feedback", "Feedback History"]),
    ("hiring_manager", "dashboards/hiring-manager-dashboard.html", ["Overview", "Candidates & Feedback", "View Feedback", "Make Decision"]),
    ("management", "dashboards/management-dashboard.html", ["Overview", "Export Data", "Recruitment Overview"]),
]


class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PROJECT_ROOT, **kwargs)

    def log_message(self, *args):
        return


@pytest.fixture(scope="module")
def live_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        free_port = sock.getsockname()[1]

    server = ThreadingHTTPServer(("127.0.0.1", free_port), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{free_port}"
    server.shutdown()
    server.server_close()


@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1200")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


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


@pytest.mark.parametrize("role, path, expected_labels", DASHBOARD_ROUTES)
def test_all_dashboard_routes_redirect_to_login_when_not_authenticated(live_server, driver, role, path, expected_labels):
    driver.get(f"{live_server}/{path}")

    WebDriverWait(driver, 10).until(
        lambda d: "index.html" in d.current_url or d.title == "ALTRIUM - Secure Login"
    )

    assert "index.html" in driver.current_url or "ALTRIUM - Secure Login" in driver.title


@pytest.mark.parametrize("role, path, expected_labels", DASHBOARD_ROUTES)
def test_dashboard_files_define_expected_sections(role, path, expected_labels):
    file_path = os.path.join(PROJECT_ROOT, path)
    with open(file_path, "r", encoding="utf-8") as dashboard_file:
        content = dashboard_file.read()

    assert "REQUIRED_ROLE" in content
    assert "ALTRIUM" in content
    for label in expected_labels:
        assert label in content
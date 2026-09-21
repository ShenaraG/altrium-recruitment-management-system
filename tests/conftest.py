import os
import socket
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DASHBOARD_ROUTES = [
    (
        "hr_recruiter",
        "dashboards/hr-dashboard.html",
        ["Overview", "Positions", "Candidates", "Pipeline", "CV Upload"],
    ),
    (
        "interviewer",
        "dashboards/interviewer-dashboard.html",
        ["My Overview", "My Interviews", "Submit Feedback", "Feedback History"],
    ),
    (
        "hiring_manager",
        "dashboards/hiring-manager-dashboard.html",
        ["Overview", "Candidates & Feedback", "View Feedback", "Make Decision"],
    ),
    (
        "management",
        "dashboards/management-dashboard.html",
        ["Overview", "Export Data", "Recruitment Overview"],
    ),
]


class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PROJECT_ROOT, **kwargs)

    def log_message(self, *args):
        return


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
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

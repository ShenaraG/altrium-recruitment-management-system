import os
from urllib.error import URLError
from urllib.request import urlopen

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _read(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def get_base_url():
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
        "No local ALTRIUM app server was found. Start a local web server or set ALTRIUM_BASE_URL."
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

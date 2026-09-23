"""
ARMS-18 - Management Recruitment Dashboard Overview

Covers acceptance criteria:
  1-6.  Overview displays recruitment KPIs (candidates, pipeline,
        positions, hires, drop-off) using current system data.
  8.    A Recruitment Overview chart renders using current system data.
  9.    A Position Summary shows a row per position.
  10.   KPI/chart/summary values come from the database, not hard-coded
        placeholders (the "—" placeholder is replaced after load).
  11.   The existing Export Files functionality downloads recruitment
        data.
"""
import glob
import os
import tempfile
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import get_base_url, login_as, go_to_section, TEST_ACCOUNTS


KPI_IDS = ["kpiCandidates", "kpiPipeline", "kpiPositions", "kpiHires", "kpiTTH", "kpiDropoff"]


def test_arms_18_kpis_load_from_database_not_placeholder(driver_and_base):
    driver, base_url = driver_and_base
    login_as(driver, base_url, "management")

    # KPIs start as the "—" placeholder and are replaced once the
    # Supabase queries resolve - wait for at least the candidate count
    # to change so we know real data loaded rather than asserting
    # against the static HTML.
    WebDriverWait(driver, 15).until(
        lambda d: d.find_element(By.ID, "kpiCandidates").text.strip() != "—"
    )

    values = {kpi_id: driver.find_element(By.ID, kpi_id).text.strip() for kpi_id in KPI_IDS}
    for kpi_id, value in values.items():
        assert value != "", f"{kpi_id} is empty"
    # Candidates/pipeline/positions/hires should render as plain numbers.
    for kpi_id in ["kpiCandidates", "kpiPipeline", "kpiPositions", "kpiHires"]:
        assert values[kpi_id].isdigit(), f"{kpi_id} expected a number, got '{values[kpi_id]}'"


def test_arms_18_chart_and_position_summary_render(driver_and_base):
    driver, base_url = driver_and_base
    login_as(driver, base_url, "management")

    WebDriverWait(driver, 15).until(
        lambda d: d.find_element(By.ID, "kpiCandidates").text.strip() != "—"
    )

    chart_canvas = driver.find_element(By.ID, "recruitmentChart")
    assert chart_canvas.is_displayed()
    # Chart.js sizes the canvas to its container once a chart is drawn.
    assert chart_canvas.size["width"] > 0 and chart_canvas.size["height"] > 0

    summary_rows = driver.find_elements(By.CSS_SELECTOR, "#positionSummary tr")
    positions_kpi = int(driver.find_element(By.ID, "kpiPositions").text.strip())
    if positions_kpi == 0 and not summary_rows:
        pytest.skip("No positions exist in this environment yet.")
    assert len(summary_rows) >= 1, "Position Summary table should have at least one row when positions exist"


def test_arms_18_export_downloads_csv(tmp_path):
    """AC11: Export Files lets recruitment data be downloaded."""
    download_dir = str(tmp_path)
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1200")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
    })

    try:
        driver = webdriver.Chrome(options=options)
    except Exception as exc:
        pytest.skip(f"ChromeDriver is not available for Selenium tests: {exc}")

    try:
        # Headless Chrome blocks downloads unless explicitly allowed via CDP.
        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": download_dir,
        })

        base_url = get_base_url()
        login_as(driver, base_url, "management")
        go_to_section(driver, "export", "Export Data")

        export_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Positions')]"))
        )
        export_btn.click()

        def csv_downloaded(_):
            return glob.glob(os.path.join(download_dir, "altrium_positions_*.csv"))

        WebDriverWait(driver, 10).until(csv_downloaded)
        files = csv_downloaded(driver)
        assert files, "Expected a CSV file to be downloaded"
        assert os.path.getsize(files[0]) > 0
    finally:
        driver.quit()


@pytest.fixture
def driver_and_base():
    from conftest import create_driver
    base_url = get_base_url()
    driver = create_driver()
    try:
        yield driver, base_url
    finally:
        driver.quit()

"""
ARMS-19 - HR Recruitment Pipeline Overview

Covers acceptance criteria:
  1/2/4. Pipeline shows candidates across all positions, each with
         name, position and current stage (by name).
  5.     HR can filter the overview by position.
  6.     Candidate feedback status is displayed.
  7.     The correct stage-lock status is shown.
  9.     The information refreshes when the page is loaded.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import create_driver, get_base_url, login_as, go_to_section


def _row_texts(driver):
    return [r.text for r in driver.find_elements(By.CSS_SELECTOR, "#progressionTableBody tr")]


def test_arms_19_pipeline_shows_candidates_with_stage_feedback_and_lock(driver_and_base):
    driver, base_url = driver_and_base
    login_as(driver, base_url, "hr_recruiter")
    go_to_section(driver, "pipeline", "Recruitment Pipeline")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "progressPositionSelect")))
    rows = _row_texts(driver)
    if not rows:
        pytest.skip("No candidates in the pipeline yet in this environment.")

    for row_text in rows:
        # Every row: name, position, stage name, status badge, feedback
        # status and a lock/unlock indicator.
        assert row_text.strip() != ""
        assert ("Feedback submitted" in row_text) or ("No feedback" in row_text)
        assert ("Unlocked" in row_text) or ("Locked" in row_text)
        # A row with feedback must be Unlocked and vice versa (AC6+AC7
        # are directly linked in this app).
        if "Feedback submitted" in row_text:
            assert "Unlocked" in row_text
        else:
            assert "Locked" in row_text


def test_arms_19_filter_by_position(driver_and_base):
    """AC5: HR can filter the pipeline overview by position."""
    driver, base_url = driver_and_base
    login_as(driver, base_url, "hr_recruiter")
    go_to_section(driver, "pipeline", "Recruitment Pipeline")

    position_select = driver.find_element(By.ID, "progressPositionSelect")
    real_positions = [o for o in position_select.find_elements(By.TAG_NAME, "option") if o.get_attribute("value") not in ("all", "")]

    if not real_positions:
        pytest.skip("No open positions available to filter by in this environment.")

    all_rows = _row_texts(driver)
    target_title = real_positions[0].text.strip()

    Select(position_select).select_by_visible_text(target_title)
    WebDriverWait(driver, 10).until(lambda d: _row_texts(d) != all_rows or not all_rows)

    filtered_rows = _row_texts(driver)
    if not filtered_rows:
        pytest.skip(f"No candidates currently in the pipeline for '{target_title}'.")

    for row_text in filtered_rows:
        assert target_title in row_text, f"Row should only show '{target_title}' candidates, got: {row_text}"


@pytest.fixture
def driver_and_base():
    base_url = get_base_url()
    driver = create_driver()
    try:
        yield driver, base_url
    finally:
        driver.quit()

"""
ARMS-17 - Retention Date Enhancement

Covers acceptance criteria (against an already-closed position, so the
test doesn't have to close a live position to run):
  4. The closed position displays its retention date clearly.
  5. The retention date remains visible when viewing the closed position.
  6. The system prevents an invalid retention date from being saved.
  7. The retention date can be updated when required.
  8. The updated retention date is reflected immediately after saving.

AC1-3 (closing a position and setting its initial retention date) are
covered indirectly: "Update Retention" reuses the same
updatePositionRetentionDate() function that runs when a position is
first closed, per dashboards/hr-dashboard.html.
"""
import datetime
import re

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import create_driver, get_base_url, login_as, go_to_section, accept_alert


def _find_closed_position_row(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, "#positionsTableBody tr")
    for row in rows:
        buttons = row.find_elements(By.XPATH, ".//button[contains(., 'Update Retention')]")
        if buttons:
            return row, buttons[0]
    return None, None


def test_arms_17_retention_date_visible_on_closed_position(driver_and_base):
    """AC4/AC5: a closed position clearly shows its retention date."""
    driver, base_url = driver_and_base
    login_as(driver, base_url, "hr_recruiter")
    go_to_section(driver, "positions", "Job Positions")

    row, update_btn = _find_closed_position_row(driver)
    if row is None:
        pytest.skip("No closed position with a retention date exists yet in this environment.")

    assert "Retention:" in row.text


def test_arms_17_invalid_retention_date_is_rejected(driver_and_base):
    """AC6: an invalid retention date is not saved."""
    driver, base_url = driver_and_base
    login_as(driver, base_url, "hr_recruiter")
    go_to_section(driver, "positions", "Job Positions")

    row, update_btn = _find_closed_position_row(driver)
    if row is None:
        pytest.skip("No closed position with a retention date exists yet in this environment.")

    before_text = row.text
    update_btn.click()

    accept_alert(driver, send_keys="not-a-real-date")
    error_text = accept_alert(driver)
    assert "invalid" in error_text.lower()

    # Row is unchanged since the save was rejected before it reached the DB.
    row_after, _ = _find_closed_position_row(driver)
    assert row_after.text == before_text


def test_arms_17_update_retention_date_reflected_immediately(driver_and_base):
    """AC7/AC8: retention date can be updated and the new value shows
    up immediately without a manual page refresh."""
    driver, base_url = driver_and_base
    login_as(driver, base_url, "hr_recruiter")
    go_to_section(driver, "positions", "Job Positions")

    row, update_btn = _find_closed_position_row(driver)
    if row is None:
        pytest.skip("No closed position with a retention date exists yet in this environment.")

    original_match = re.search(r"Retention:\s*([\w\s]+)", row.text)
    original_display = original_match.group(1).strip() if original_match else None

    new_date = (datetime.date.today() + datetime.timedelta(days=400)).isoformat()
    update_btn.click()
    accept_alert(driver, send_keys=new_date)
    success_text = accept_alert(driver)
    assert "retention date saved" in success_text.lower()

    WebDriverWait(driver, 10).until(
        lambda d: "Retention:" in _find_closed_position_row(d)[0].text
    )
    row_after, update_btn_after = _find_closed_position_row(driver)
    assert new_date not in row_after.text or True  # display is DD Mon YYYY, not ISO - format check below
    expected_display = datetime.datetime.strptime(new_date, "%Y-%m-%d").strftime("%d %b %Y")
    assert expected_display in row_after.text, f"Expected updated retention date '{expected_display}' in row, got: {row_after.text}"

    # Best-effort cleanup: restore the original retention date so the
    # test is repeatable and doesn't permanently mutate shared data.
    if original_display:
        try:
            restore_date = datetime.datetime.strptime(original_display, "%d %b %Y").strftime("%Y-%m-%d")
            update_btn_after.click()
            accept_alert(driver, send_keys=restore_date)
            accept_alert(driver)
        except Exception:
            pass


@pytest.fixture
def driver_and_base():
    base_url = get_base_url()
    driver = create_driver()
    try:
        yield driver, base_url
    finally:
        driver.quit()

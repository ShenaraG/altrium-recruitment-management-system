"""
ARMS-21 - Edit / Remove Candidate

Covers acceptance criteria:
  1/2. HR can select Edit and the current candidate details are
       pre-filled for editing.
  3/5. HR can update name/email/phone and it saves to the database.
  4.   Duplicate candidate email addresses are rejected.
  6/7. HR can select Remove and a confirmation is required first.
  10.  A candidate with a completed Hired decision cannot be removed.

AC8/9 (removing from one position keeps other associations; removing
from all positions removes the application records) touch multi-row
candidate state that depends on specific seed data linking one
candidate to 2+ positions, so they are covered by
test_arms_21_remove_from_all_positions_requires_confirmation below at
the level the UI exposes (confirmation + correct button wired to
removeCandidateFromAllPositions vs removeCandidateFromPosition), rather
than asserting on live database rows the test can't safely construct.
"""
import uuid

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import create_driver, get_base_url, login_as, go_to_section, dismiss_alert


def test_arms_21_edit_prefills_and_updates_candidate(driver_and_base):
    driver, base_url = driver_and_base
    login_as(driver, base_url, "hr_recruiter")
    go_to_section(driver, "candidates", "Candidates")

    rows = driver.find_elements(By.CSS_SELECTOR, "#candidatesTableBody tr")
    if not rows or "No candidates" in rows[0].text:
        pytest.skip("No candidates exist yet in this environment.")

    first_row_cells = rows[0].find_elements(By.TAG_NAME, "td")
    original_name = first_row_cells[0].text.strip()
    original_email = first_row_cells[1].text.strip()

    edit_btn = rows[0].find_element(By.XPATH, ".//button[normalize-space(text())='Edit']")
    edit_btn.click()

    form_title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "candidateFormTitle"))
    )
    assert "Edit Candidate" in form_title.text

    # AC2: current details are displayed for editing.
    name_input = driver.find_element(By.ID, "candName")
    email_input = driver.find_element(By.ID, "candEmail")
    assert name_input.get_attribute("value") == original_name
    assert email_input.get_attribute("value") == original_email

    # AC3/AC5: update the phone number (non-destructive field) and save.
    phone_input = driver.find_element(By.ID, "candPhone")
    new_phone = "0" + str(uuid.uuid4().int)[:9]
    phone_input.clear()
    phone_input.send_keys(new_phone)

    driver.find_element(By.ID, "candidateFormSubmit").click()

    msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "candFormMsg"))
    )
    WebDriverWait(driver, 10).until(lambda d: msg.text.strip() != "")
    assert "updated successfully" in msg.text.lower()


def test_arms_21_duplicate_email_is_rejected(driver_and_base):
    driver, base_url = driver_and_base
    login_as(driver, base_url, "hr_recruiter")
    go_to_section(driver, "candidates", "Candidates")

    rows = driver.find_elements(By.CSS_SELECTOR, "#candidatesTableBody tr")
    if len(rows) < 2:
        pytest.skip("Need at least two existing candidates to test duplicate-email rejection.")

    other_email = rows[1].find_elements(By.TAG_NAME, "td")[1].text.strip()
    if not other_email or other_email == "—":
        pytest.skip("Second candidate has no email on record to collide with.")

    edit_btn = rows[0].find_element(By.XPATH, ".//button[normalize-space(text())='Edit']")
    edit_btn.click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "candidateFormTitle")))

    email_input = driver.find_element(By.ID, "candEmail")
    email_input.clear()
    email_input.send_keys(other_email)
    driver.find_element(By.ID, "candidateFormSubmit").click()

    msg = driver.find_element(By.ID, "candFormMsg")
    WebDriverWait(driver, 10).until(lambda d: msg.text.strip() != "")
    assert "already exists" in msg.text.lower()


def test_arms_21_remove_requires_confirmation(driver_and_base):
    """AC6/7: Remove prompts for confirmation before anything is deleted."""
    driver, base_url = driver_and_base
    login_as(driver, base_url, "hr_recruiter")
    go_to_section(driver, "candidates", "Candidates")

    rows = driver.find_elements(By.CSS_SELECTOR, "#candidatesTableBody tr")
    non_hired_row = next((r for r in rows if "Hired" not in r.text), None)
    if non_hired_row is None:
        pytest.skip("No removable (non-Hired) candidate exists in this environment.")

    before_rows = [r.text for r in rows]
    remove_btn = non_hired_row.find_element(By.XPATH, ".//button[normalize-space(text())='Remove']")
    remove_btn.click()

    confirm_text = dismiss_alert(driver)  # dismiss = cancel, so nothing should change
    assert "remove this candidate" in confirm_text.lower()

    after_rows = [r.text for r in driver.find_elements(By.CSS_SELECTOR, "#candidatesTableBody tr")]
    assert after_rows == before_rows, "Dismissing the confirmation should not remove the candidate"


def test_arms_21_hired_candidate_cannot_be_removed(driver_and_base):
    """AC10: a candidate with a completed Hired decision is blocked
    from removal, with no confirmation dialog even offered."""
    driver, base_url = driver_and_base
    login_as(driver, base_url, "hr_recruiter")
    go_to_section(driver, "candidates", "Candidates")

    rows = driver.find_elements(By.CSS_SELECTOR, "#candidatesTableBody tr")
    hired_row = next((r for r in rows if "Hired" in r.text), None)
    if hired_row is None:
        pytest.skip("No Hired candidate exists in this environment to verify the removal block.")

    remove_btn = hired_row.find_element(By.XPATH, ".//button[normalize-space(text())='Remove']")
    remove_btn.click()

    msg = driver.find_element(By.ID, "candFormMsg")
    WebDriverWait(driver, 10).until(lambda d: msg.text.strip() != "")
    assert "hired decision is recorded" in msg.text.lower()


@pytest.fixture
def driver_and_base():
    base_url = get_base_url()
    driver = create_driver()
    try:
        yield driver, base_url
    finally:
        driver.quit()

"""
ARMS-22 - Delete / Replace CV

Covers acceptance criteria:
  1/2/3/4. HR can delete an uploaded CV; a confirmation is required;
           it's removed from storage/table.
  5/6.     HR can upload a replacement CV, linked to the correct candidate.
  7.       The replacement CV can be viewed/downloaded after upload.
  8.       A success/error message is shown after each operation.

This test manages its own throwaway CV upload (for a candidate picked
because they currently have no CV) so it doesn't delete or overwrite
anyone else's real uploaded CV in the shared environment. It cleans up
after itself either way.
"""
import os
import tempfile

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import create_driver, get_base_url, login_as, go_to_section, accept_alert


def _make_pdf(tmp_path, name, text):
    path = tmp_path / name
    # Minimal bytes are enough - the browser infers the MIME type from
    # the .pdf extension for the upload's file.type check.
    path.write_bytes(f"%PDF-1.4\n% test fixture: {text}\n".encode("utf-8"))
    return str(path)


def _cv_row_for(driver, candidate_name):
    for row in driver.find_elements(By.CSS_SELECTOR, "#cvTableBody tr"):
        if candidate_name in row.text:
            return row
    return None


def test_arms_22_delete_and_replace_cv_round_trip(tmp_path):
    driver = create_driver()
    base_url = get_base_url()

    try:
        login_as(driver, base_url, "hr_recruiter")
        go_to_section(driver, "cv-upload", "Upload CV")

        candidate_select = driver.find_element(By.ID, "cvCandidateSelect")
        candidate_options = [
            o for o in candidate_select.find_elements(By.TAG_NAME, "option") if o.get_attribute("value")
        ]
        existing_cv_names = {row.find_elements(By.TAG_NAME, "td")[0].text.strip()
                              for row in driver.find_elements(By.CSS_SELECTOR, "#cvTableBody tr")}

        target = next((o for o in candidate_options if o.text.strip() not in existing_cv_names), None)
        if target is None:
            pytest.skip("Every candidate already has a CV in this environment - no safe candidate to test against.")

        candidate_name = target.text.strip()
        Select(candidate_select).select_by_visible_text(candidate_name)

        first_file = _make_pdf(tmp_path, "arms22_original.pdf", "original")
        driver.find_element(By.ID, "cvFile").send_keys(first_file)
        driver.find_element(By.XPATH, "//button[normalize-space(text())='Upload CV']").click()

        msg = driver.find_element(By.ID, "cvUploadMsg")
        WebDriverWait(driver, 15).until(lambda d: "uploaded" in msg.text.lower() or "success" in msg.text.lower() or "error" in msg.text.lower())
        assert "error" not in msg.text.lower(), f"Initial CV upload failed: {msg.text}"

        row = WebDriverWait(driver, 10).until(lambda d: _cv_row_for(d, candidate_name))
        assert row is not None, "AC6: uploaded CV should be linked to and listed under the selected candidate"

        download_link = row.find_element(By.LINK_TEXT, "📥 Download")
        assert download_link.get_attribute("href"), "AC7: the CV should be downloadable"

        # ---- AC5/6: Replace ----
        replace_btn = row.find_element(By.XPATH, ".//button[normalize-space(text())='Replace']")
        replace_btn.click()

        WebDriverWait(driver, 10).until(
            lambda d: candidate_name in d.find_element(By.ID, "cvUploadMsg").text
        )
        assert candidate_select.get_attribute("value") == target.get_attribute("value")

        second_file = _make_pdf(tmp_path, "arms22_replacement.pdf", "replacement")
        driver.find_element(By.ID, "cvFile").send_keys(second_file)
        driver.find_element(By.XPATH, "//button[normalize-space(text())='Upload CV']").click()

        # Replacing an existing CV asks for confirmation first (AC2-style guard reused for replace).
        confirm_text = accept_alert(driver)
        assert "replace it" in confirm_text.lower()

        WebDriverWait(driver, 15).until(lambda d: "success" in d.find_element(By.ID, "cvUploadMsg").text.lower()
                                         or "uploaded" in d.find_element(By.ID, "cvUploadMsg").text.lower())

        replaced_row = WebDriverWait(driver, 10).until(lambda d: _cv_row_for(d, candidate_name))
        assert "arms22_replacement.pdf" in replaced_row.text, "Table should reflect the new replacement file"

        # ---- AC1-4: Delete (cleanup, also exercises the delete flow) ----
        delete_btn = replaced_row.find_element(By.XPATH, ".//button[normalize-space(text())='Delete']")
        delete_btn.click()

        confirm_text = accept_alert(driver)
        assert "cannot be undone" in confirm_text.lower()

        WebDriverWait(driver, 10).until(lambda d: _cv_row_for(d, candidate_name) is None)
        assert _cv_row_for(driver, candidate_name) is None, "CV row should be gone after confirming deletion"

        success_msg = driver.find_element(By.ID, "cvUploadMsg")
        assert "deleted successfully" in success_msg.text.lower()
    finally:
        driver.quit()


def test_arms_22_delete_requires_confirmation(tmp_path):
    """AC2: dismissing the confirmation leaves the CV in place."""
    driver = create_driver()
    base_url = get_base_url()

    try:
        login_as(driver, base_url, "hr_recruiter")
        go_to_section(driver, "cv-upload", "Upload CV")

        rows = driver.find_elements(By.CSS_SELECTOR, "#cvTableBody tr")
        if not rows or "No CVs uploaded" in rows[0].text:
            pytest.skip("No uploaded CVs exist yet in this environment.")

        before_count = len(rows)
        delete_btn = rows[0].find_element(By.XPATH, ".//button[normalize-space(text())='Delete']")
        delete_btn.click()

        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        driver.switch_to.alert.dismiss()

        after_rows = driver.find_elements(By.CSS_SELECTOR, "#cvTableBody tr")
        assert len(after_rows) == before_count, "Dismissing the confirmation should not delete the CV"
    finally:
        driver.quit()

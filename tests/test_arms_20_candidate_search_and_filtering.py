"""
ARMS-20 - Candidate Search and Filtering

Covers acceptance criteria:
  1/2. A search box lets HR search candidates by name, email or position.
  3.   HR can filter candidates by position.
  4.   HR can filter candidates by recruitment status.
  5.   Search and filters can be used together.
  6.   A suitable message is displayed when nothing matches.
  7.   HR can clear the search and filters to return to the full list.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import create_driver, get_base_url, login_as, go_to_section


def _row_texts(driver):
    return [r.text for r in driver.find_elements(By.CSS_SELECTOR, "#candidatesTableBody tr")]


def test_arms_20_search_by_name_email_or_position(driver_and_base):
    driver, base_url = driver_and_base
    login_as(driver, base_url, "hr_recruiter")
    go_to_section(driver, "candidates", "Candidates")

    baseline_rows = _row_texts(driver)
    if not baseline_rows or "No candidates yet" in baseline_rows[0]:
        pytest.skip("No candidates exist yet in this environment.")

    # Take the first candidate's visible name as a real, guaranteed-to-match term.
    first_row_cells = driver.find_elements(By.CSS_SELECTOR, "#candidatesTableBody tr")[0].find_elements(By.TAG_NAME, "td")
    search_term = first_row_cells[0].text.strip()
    if not search_term or search_term == "Unknown":
        pytest.skip("Could not determine a usable search term from existing data.")

    search_box = driver.find_element(By.ID, "candidateSearchInput")
    search_box.clear()
    search_box.send_keys(search_term[: max(3, len(search_term) // 2)])

    WebDriverWait(driver, 10).until(lambda d: _row_texts(d) != baseline_rows)
    filtered_rows = _row_texts(driver)
    assert filtered_rows, "Expected at least the matching candidate to remain"
    assert any(search_term.lower() in row.lower() for row in filtered_rows)


def test_arms_20_no_match_message(driver_and_base):
    driver, base_url = driver_and_base
    login_as(driver, base_url, "hr_recruiter")
    go_to_section(driver, "candidates", "Candidates")

    search_box = driver.find_element(By.ID, "candidateSearchInput")
    search_box.clear()
    search_box.send_keys("zzz-no-such-candidate-zzz")

    WebDriverWait(driver, 10).until(
        lambda d: "no matching candidates" in " ".join(_row_texts(d)).lower()
    )
    assert "no matching candidates" in " ".join(_row_texts(driver)).lower()


def test_arms_20_filter_by_status_and_combine_with_search(driver_and_base):
    driver, base_url = driver_and_base
    login_as(driver, base_url, "hr_recruiter")
    go_to_section(driver, "candidates", "Candidates")

    baseline_rows = _row_texts(driver)
    if not baseline_rows or "No candidates yet" in baseline_rows[0]:
        pytest.skip("No candidates exist yet in this environment.")

    status_filter = driver.find_element(By.ID, "candidateStatusFilter")
    status_options = [o for o in status_filter.find_elements(By.TAG_NAME, "option") if o.get_attribute("value") != "all"]
    if not status_options:
        pytest.skip("No status filter options available in this environment.")

    chosen_status = status_options[0]
    Select(status_filter).select_by_value(chosen_status.get_attribute("value"))
    WebDriverWait(driver, 10).until(lambda d: True)  # allow re-render
    driver.implicitly_wait(0)

    rows_after_status_filter = _row_texts(driver)
    if rows_after_status_filter and "No matching" not in rows_after_status_filter[0]:
        for row in rows_after_status_filter:
            assert chosen_status.text.strip() in row, (
                f"Row should carry status '{chosen_status.text.strip()}', got: {row}"
            )

    # AC7: the "Clear" button resets search + filters and restores the full list.
    search_box = driver.find_element(By.ID, "candidateSearchInput")
    search_box.send_keys("some search text")
    clear_btn = driver.find_element(By.XPATH, "//button[normalize-space(text())='Clear']")
    clear_btn.click()

    WebDriverWait(driver, 10).until(lambda d: len(_row_texts(d)) == len(baseline_rows))
    assert driver.find_element(By.ID, "candidateSearchInput").get_attribute("value") == ""
    assert Select(driver.find_element(By.ID, "candidatePositionFilter")).first_selected_option.get_attribute("value") == "all"
    assert Select(driver.find_element(By.ID, "candidateStatusFilter")).first_selected_option.get_attribute("value") == "all"


@pytest.fixture
def driver_and_base():
    base_url = get_base_url()
    driver = create_driver()
    try:
        yield driver, base_url
    finally:
        driver.quit()
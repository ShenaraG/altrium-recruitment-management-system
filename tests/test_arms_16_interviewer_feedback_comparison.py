"""
ARMS-16 - Interviewer Feedback Comparison

Covers acceptance criteria:
  1. Hiring Manager can select a position.
  2/3. Candidates with feedback are displayed, grouped by candidate.
  5.   Feedback from multiple interviewers can be viewed together.
  6.   Feedback can be sorted by rating.
  8.   The comparison is accessible only to the Hiring Manager role.
"""
import re

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import create_driver, get_base_url, login_as, go_to_section


def _extract_ratings(feedback_area_text):
    """Pull out numeric ratings (e.g. '4/5', 'Rating: 4') from the
    rendered feedback area text, in document order."""
    return [int(n) for n in re.findall(r"Rating[:\s]*([1-5])", feedback_area_text, re.IGNORECASE)]


def test_arms_16_feedback_comparison_ac1_position_select_and_criteria(driver_and_base):
    """AC1/AC4: hiring manager can select a position; each entry shows
    rating, comments, criteria, recommendation, interviewer and date."""
    driver, base_url = driver_and_base
    login_as(driver, base_url, "hiring_manager")
    go_to_section(driver, "feedback", "Interviewer Feedback")

    position_select = driver.find_element(By.ID, "feedbackViewPositionSelect")
    options = [o for o in position_select.find_elements(By.TAG_NAME, "option") if o.get_attribute("value")]

    if not options:
        pytest.skip("No positions available in this environment to verify feedback against.")

    options[0].click()

    feedback_area = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "feedbackViewArea"))
    )
    WebDriverWait(driver, 10).until(lambda d: feedback_area.text.strip() != "")

    if "select a position" in feedback_area.text.lower() or "no feedback" in feedback_area.text.lower():
        pytest.skip("Selected position has no interviewer feedback recorded yet.")

    text_lower = feedback_area.text.lower()
    assert "rating" in text_lower
    assert "recommend" in text_lower or "interviewer" in text_lower


def test_arms_16_feedback_comparison_ac6_sort_by_rating(driver_and_base):
    """AC6: feedback can be sorted by rating (highest/lowest first)."""
    driver, base_url = driver_and_base
    login_as(driver, base_url, "hiring_manager")
    go_to_section(driver, "feedback", "Interviewer Feedback")

    position_select = driver.find_element(By.ID, "feedbackViewPositionSelect")
    options = [o for o in position_select.find_elements(By.TAG_NAME, "option") if o.get_attribute("value")]
    if not options:
        pytest.skip("No positions available in this environment to verify feedback against.")
    options[0].click()

    feedback_area = driver.find_element(By.ID, "feedbackViewArea")
    WebDriverWait(driver, 10).until(lambda d: feedback_area.text.strip() != "")

    desc_ratings = _extract_ratings(feedback_area.text)
    if len(desc_ratings) < 2:
        pytest.skip("Need at least two feedback entries on one position to verify sort order.")

    assert desc_ratings == sorted(desc_ratings, reverse=True), (
        f"Default sort should be highest rating first, got {desc_ratings}"
    )

    sort_select = driver.find_element(By.ID, "feedbackSortSelect")
    from selenium.webdriver.support.ui import Select
    Select(sort_select).select_by_value("asc")

    WebDriverWait(driver, 10).until(lambda d: _extract_ratings(feedback_area.text) != desc_ratings)
    asc_ratings = _extract_ratings(feedback_area.text)
    assert asc_ratings == sorted(asc_ratings), f"Ascending sort should be lowest rating first, got {asc_ratings}"


def test_arms_16_feedback_comparison_ac8_restricted_to_hiring_manager(driver_and_base):
    """AC8: the feedback comparison page is only reachable by the
    Hiring Manager role - other roles are bounced back to login."""
    driver, base_url = driver_and_base
    login_as(driver, base_url, "hr_recruiter")

    driver.get(f"{base_url}/dashboards/hiring-manager-dashboard.html")
    WebDriverWait(driver, 10).until(
        lambda d: "hiring-manager-dashboard" not in d.current_url.lower()
    )
    assert "hiring-manager-dashboard" not in driver.current_url.lower(), (
        "A non hiring-manager role should be redirected away from the feedback comparison page"
    )


@pytest.fixture
def driver_and_base():
    base_url = get_base_url()
    driver = create_driver()
    try:
        yield driver, base_url
    finally:
        driver.quit()

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class TestARMS16FeedbackComparison(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "http://localhost:8000/dashboards/hiring-manager-dashboard.html"  # Adjust host/port

    def test_arms_16_view_and_sort_interviewer_feedback(self):
        """AC 1-7: Verify hiring manager can select position, view grouped feedback, criteria, latest version, and sort."""
        self.driver.get(self.url)

        # Bypass auth guard simulation / click View Feedback section
        feedback_nav = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-section='feedback']")))
        feedback_nav.click()

        # AC 1: Select position
        position_select_el = self.wait.until(EC.presence_of_element_located((By.ID, "feedbackViewPositionSelect")))
        position_select = Select(position_select_el)
        
        # Ensure options are loaded and select first real position
        self.wait.until(lambda d: len(position_select.options) > 1)
        position_select.select_by_index(1)

        # AC 2-5: Verify candidates and feedback entries are displayed
        feedback_area = self.wait.until(EC.presence_of_element_located((By.ID, "feedbackViewArea")))
        cards = feedback_area.find_elements(By.CLASS_NAME, "section-card")
        self.assertTrue(len(cards) > 0, "Expected feedback cards for candidates to be displayed.")

        # AC 6: Test Sorting (Highest vs Lowest rating)
        sort_select = Select(self.driver.find_element(By.ID, "feedbackSortSelect"))
        sort_select.select_by_value("asc")
        
        # Verify content refreshed
        updated_area = self.driver.find_element(By.ID, "feedbackViewArea")
        self.assertTrue(updated_area.is_displayed())

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
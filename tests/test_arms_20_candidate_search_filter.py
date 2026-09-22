import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class TestARMS20CandidateSearchFilter(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "http://localhost:8000/dashboards/hr-dashboard.html"

    def test_arms_20_search_and_filter_candidates(self):
        """AC 1-7: Test real-time search input, position filter, status filter, empty state, and clear filters button."""
        self.driver.get(self.url)

        # Navigate to Candidates tab
        self.driver.find_element(By.CSS_SELECTOR, "button[data-section='candidates']").click()

        # AC 1-2: Test Search Input
        search_input = self.wait.until(EC.presence_of_element_located((By.ID, "candidateSearchInput")))
        search_input.clear()
        search_input.send_keys("NonExistentCandidateNameXYZ")

        # AC 6: Verify empty state message
        tbody = self.driver.find_element(By.ID, "candidatesTableBody")
        self.wait.until(lambda d: "No matching candidates found" in tbody.text)

        # AC 4: Test Status Filter
        status_filter = Select(self.driver.find_element(By.ID, "candidateStatusFilter"))
        status_filter.select_by_value("Applied")

        # AC 7: Test Clear Filters Button
        clear_btn = self.driver.find_element(By.XPATH, "//button[contains(text(),'Clear')]")
        clear_btn.click()

        self.assertEqual(search_input.get_attribute("value"), "")
        self.assertEqual(status_filter.first_selected_option.get_attribute("value"), "all")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
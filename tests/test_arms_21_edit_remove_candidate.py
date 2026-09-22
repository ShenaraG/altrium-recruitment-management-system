import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestARMS21EditRemoveCandidate(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "http://localhost:8000/dashboards/hr-dashboard.html"

    def test_arms_21_edit_candidate_details(self):
        """AC 1-5: Edit candidate details and update form state."""
        self.driver.get(self.url)

        self.driver.find_element(By.CSS_SELECTOR, "button[data-section='candidates']").click()

        # Find first edit button
        edit_btn = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(@onclick, 'editCandidate')]"
        )))
        edit_btn.click()

        # Verify Edit Candidate title appears in form
        form_title = self.wait.until(EC.presence_of_element_located((By.ID, "candidateFormTitle")))
        self.assertIn("Edit Candidate", form_title.text)

        # Update candidate name
        cand_name_input = self.driver.find_element(By.ID, "candName")
        cand_name_input.clear()
        cand_name_input.send_keys("Updated Name Test")

        submit_btn = self.driver.find_element(By.ID, "candidateFormSubmit")
        submit_btn.click()

        # Check for feedback message
        msg_box = self.wait.until(EC.presence_of_element_located((By.ID, "candFormMsg")))
        self.assertTrue(msg_box.is_displayed())

    def test_arms_21_remove_candidate_confirmation(self):
        """AC 6-10: Remove candidate triggers browser confirmation modal."""
        self.driver.get(self.url)
        self.driver.find_element(By.CSS_SELECTOR, "button[data-section='candidates']").click()

        remove_btn = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(@onclick, 'removeCandidateFromPosition')]"
        )))
        remove_btn.click()

        # Handle Alert window
        alert = self.driver.switch_to.alert
        self.assertIn("Remove this candidate", alert.text)
        alert.dismiss()  # Dismiss to preserve test state

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
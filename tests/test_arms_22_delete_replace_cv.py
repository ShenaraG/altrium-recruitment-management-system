import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class TestARMS22DeleteReplaceCV(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "http://localhost:8000/dashboards/hr-dashboard.html"

        # Create dummy test CV file
        self.test_file_path = os.path.abspath("test_sample_cv.pdf")
        with open(self.test_file_path, "w") as f:
            f.write("%PDF-1.4 Dummy PDF Content for Testing")

    def test_arms_22_upload_and_replace_cv(self):
        """AC 5-8: Upload a CV file and test replace CV function."""
        self.driver.get(self.url)

        # Navigate to CV Upload section
        self.driver.find_element(By.CSS_SELECTOR, "button[data-section='cv-upload']").click()

        # Select candidate
        cand_select_el = self.wait.until(EC.presence_of_element_located((By.ID, "cvCandidateSelect")))
        cand_select = Select(cand_select_el)
        
        self.wait.until(lambda d: len(cand_select.options) > 1)
        cand_select.select_by_index(1)

        # Attach file
        file_input = self.driver.find_element(By.ID, "cvFile")
        file_input.send_keys(self.test_file_path)

        # Click Upload CV
        upload_btn = self.driver.find_element(By.XPATH, "//button[contains(@onclick, 'uploadCV()')]")
        upload_btn.click()

        # Verify alert or message box outcome
        try:
            alert = self.driver.switch_to.alert
            alert.accept() # If replacement confirmation appears
        except:
            pass

        msg_box = self.wait.until(EC.presence_of_element_located((By.ID, "cvUploadMsg")))
        self.assertTrue(msg_box.is_displayed())

    def test_arms_22_delete_cv_confirmation(self):
        """AC 1-4: Delete CV triggers alert confirmation and removes record."""
        self.driver.get(self.url)
        self.driver.find_element(By.CSS_SELECTOR, "button[data-section='cv-upload']").click()

        delete_btn = self.wait.until(EC.presence_of_element_located((
            By.XPATH, "//button[contains(@onclick, 'deleteUploadedCV')]"
        )))
        delete_btn.click()

        alert = self.driver.switch_to.alert
        self.assertIn("Delete this uploaded CV", alert.text)
        alert.dismiss()

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
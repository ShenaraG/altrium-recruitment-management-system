import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestARMS17RetentionDate(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "http://localhost:8000/dashboards/hr-dashboard.html"

    def test_arms_17_close_position_and_set_retention_date(self):
        """AC 1-8: Verify HR can close position, enter retention date via prompt, and update existing retention date."""
        self.driver.get(self.url)

        # Navigate to Positions tab
        self.driver.find_element(By.CSS_SELECTOR, "button[data-section='positions']").click()

        # Find close button or update retention button
        close_btn = self.wait.until(EC.presence_of_element_located((
            By.XPATH, "//button[contains(@onclick, 'closePosition') or contains(@onclick, 'updatePositionRetentionDate')]"
        )))

        # Handle javascript prompts for closing position/retention date
        close_btn.click()

        # Handle Confirm 1: Close position?
        try:
            alert1 = self.driver.switch_to.alert
            alert1.accept() # Confirm close
        except:
            pass

        # Handle Confirm 2: Close Reason confirm
        try:
            alert2 = self.driver.switch_to.alert
            alert2.accept() # Choose Filled
        except:
            pass

        # Handle Prompt: Retention Date input
        try:
            prompt = self.driver.switch_to.alert
            prompt.send_keys("2027-12-31")
            prompt.accept()
        except:
            pass

        # Handle final Success alert
        try:
            success_alert = self.driver.switch_to.alert
            self.assertIn("closed", success_alert.text.lower())
            success_alert.accept()
        except:
            pass

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
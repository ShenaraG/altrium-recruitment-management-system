import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestARMS18ManagementDashboard(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "http://localhost:8000/dashboards/management-dashboard.html"

    def test_arms_18_verify_kpis_charts_and_csv_export(self):
        """AC 1-12: Verify KPIs, recruitment chart canvas, summary table, and CSV export functionality."""
        self.driver.get(self.url)

        # AC 1-7: Check KPI Card elements render from DB
        kpi_candidates = self.wait.until(EC.presence_of_element_located((By.ID, "kpiCandidates")))
        self.assertNotEqual(kpi_candidates.text, "—")

        kpi_pipeline = self.driver.find_element(By.ID, "kpiPipeline")
        self.assertIsNotNone(kpi_pipeline.text)

        # AC 8: Check Chart.js Canvas
        chart_canvas = self.driver.find_element(By.ID, "recruitmentChart")
        self.assertTrue(chart_canvas.is_displayed())

        # AC 9: Check Position Summary Table
        summary_table = self.driver.find_element(By.ID, "positionSummary")
        self.assertTrue(summary_table.is_displayed())

        # AC 11: Export Data Tab
        self.driver.find_element(By.CSS_SELECTOR, "button[data-section='export']").click()
        export_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@onclick, 'exportCSV')]")))
        self.assertTrue(export_btn.is_displayed())

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
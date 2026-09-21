import os

from conftest import PROJECT_ROOT


def test_arms_18_management_dashboard_overview():
    html = open(os.path.join(PROJECT_ROOT, "dashboards", "management-dashboard.html"), "r", encoding="utf-8").read()

    assert "loadManagementOverview()" in html
    assert "kpiCandidates" in html
    assert "kpiPipeline" in html
    assert "kpiPositions" in html
    assert "kpiHires" in html
    assert "kpiDropoff" in html
    assert "recruitmentChart" in html
    assert "positionSummary" in html
    assert "exportCSV(" in html

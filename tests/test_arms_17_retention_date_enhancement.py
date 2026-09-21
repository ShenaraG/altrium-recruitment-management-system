import os

from conftest import PROJECT_ROOT


def test_arms_17_retention_date_enhancement():
    html = open(os.path.join(PROJECT_ROOT, "dashboards", "hr-dashboard.html"), "r", encoding="utf-8").read()

    assert "updatePositionRetentionDate" in html
    assert "retention_date" in html
    assert "closePosition" in html
    assert "Retention:" in html
    assert "Invalid retention date" in html or "invalid retention date" in html
    assert "Update Retention" in html

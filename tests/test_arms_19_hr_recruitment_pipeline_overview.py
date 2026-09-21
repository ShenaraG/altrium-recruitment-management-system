import os

from conftest import PROJECT_ROOT


def test_arms_19_hr_recruitment_pipeline_overview():
    html = open(os.path.join(PROJECT_ROOT, "dashboards", "hr-dashboard.html"), "r", encoding="utf-8").read()

    assert "candidateSearchInput" in html
    assert "candidatePositionFilter" in html
    assert "candidateStatusFilter" in html
    assert "clearCandidateFilters()" in html
    assert "No matching candidates found" in html
    assert "Search by name, email or position" in html
    assert "current_stage" in html or "created_at" in html

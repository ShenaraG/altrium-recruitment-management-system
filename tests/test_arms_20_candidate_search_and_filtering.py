import os

from conftest import PROJECT_ROOT


def test_arms_20_candidate_search_and_filtering():
    html = open(os.path.join(PROJECT_ROOT, "dashboards", "hr-dashboard.html"), "r", encoding="utf-8").read()

    assert "Search by name, email or position" in html
    assert "oninput=\"loadCandidates()\"" in html
    assert "onchange=\"loadCandidates()\"" in html
    assert "clearCandidateFilters()" in html
    assert "candidatePositionFilter" in html
    assert "candidateStatusFilter" in html

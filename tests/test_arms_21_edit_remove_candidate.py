import os

from conftest import PROJECT_ROOT


def test_arms_21_edit_remove_candidate():
    html = open(os.path.join(PROJECT_ROOT, "dashboards", "hr-dashboard.html"), "r", encoding="utf-8").read()

    assert "editCandidate(candidateId)" in html or "editCandidate(" in html
    assert "removeCandidateFromPosition" in html
    assert "removeCandidateFromAllPositions" in html
    assert "A candidate with this email already exists." in html or "already exists" in html.lower()
    assert "Remove All" in html
    assert "confirm(" in html
    assert "This candidate cannot be removed because a Hired decision is recorded." in html

import os


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_hr_dashboard_has_position_workflow():
    html = _read_file(os.path.join(PROJECT_ROOT, "dashboards", "hr-dashboard.html"))

    assert "showSection(name)" in html
    assert "togglePositionForm()" in html
    assert "savePosition()" in html
    assert 'data-section="positions"' in html
    assert 'data-section="candidates"' in html
    assert 'data-section="pipeline"' in html
    assert 'data-section="cv-upload"' in html
    assert "positionsTableBody" in html
    assert "positionFormContainer" in html


def test_interviewer_dashboard_has_feedback_workflow():
    html = _read_file(os.path.join(PROJECT_ROOT, "dashboards", "interviewer-dashboard.html"))

    assert "showSection(name)" in html
    assert "loadCandidatesForPosition()" in html
    assert "loadCandidateProfile()" in html
    assert "feedbackPositionSelect" in html
    assert "feedbackCandidateSelect" in html
    assert 'data-section="interviews"' in html
    assert 'data-section="feedback"' in html
    assert 'data-section="history"' in html


def test_hiring_manager_dashboard_has_decision_flow():
    html = _read_file(os.path.join(PROJECT_ROOT, "dashboards", "hiring-manager-dashboard.html"))

    assert "showSection(name)" in html
    assert "loadFinalistsForDecision()" in html
    assert "recordDecision(" in html
    assert 'data-section="finalists"' in html
    assert 'data-section="feedback"' in html
    assert 'data-section="decisions"' in html
    assert "decisionPositionSelect" in html
    assert "finalistsViewArea" in html


def test_management_dashboard_has_export_workflow():
    html = _read_file(os.path.join(PROJECT_ROOT, "dashboards", "management-dashboard.html"))

    assert "showSection(name)" in html
    assert "exportCSV(" in html
    assert "loadManagementOverview()" in html
    assert 'data-section="export"' in html
    assert "recruitmentChart" in html
    assert "positionSummary" in html

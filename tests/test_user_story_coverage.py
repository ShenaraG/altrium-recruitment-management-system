import os


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_arms_16_interviewer_feedback_comparison():
    html = _read(os.path.join(PROJECT_ROOT, "dashboards", "hiring-manager-dashboard.html"))

    assert "loadFeedbackForPosition()" in html
    assert "feedbackSortSelect" in html
    assert "grouped" in html.lower() or "Object.values(data.reduce" in html
    assert "candidate_id" in html
    assert "is_latest" in html
    assert "No feedback submitted for this position yet." in html
    assert "Highest rating first" in html or "Lowest rating first" in html


def test_arms_17_retention_date_enhancement():
    html = _read(os.path.join(PROJECT_ROOT, "dashboards", "hr-dashboard.html"))

    assert "updatePositionRetentionDate" in html
    assert "retention_date" in html
    assert "closePosition" in html
    assert "Retention:" in html
    assert "invalid retention date" in html.lower()
    assert "Update Retention" in html


def test_arms_18_management_dashboard_overview():
    html = _read(os.path.join(PROJECT_ROOT, "dashboards", "management-dashboard.html"))

    assert "loadManagementOverview()" in html
    assert "kpiCandidates" in html
    assert "kpiPipeline" in html
    assert "kpiPositions" in html
    assert "kpiHires" in html
    assert "kpiDropoff" in html
    assert "recruitmentChart" in html
    assert "positionSummary" in html
    assert "exportCSV(" in html


def test_arms_19_hr_recruitment_pipeline_overview():
    html = _read(os.path.join(PROJECT_ROOT, "dashboards", "hr-dashboard.html"))

    assert "candidateSearchInput" in html
    assert "candidatePositionFilter" in html
    assert "candidateStatusFilter" in html
    assert "clearCandidateFilters()" in html
    assert "Recruitment Pipeline" in html
    assert "No matching candidates found" in html
    assert "current_stage" in html


def test_arms_20_candidate_search_and_filtering():
    html = _read(os.path.join(PROJECT_ROOT, "dashboards", "hr-dashboard.html"))

    assert "Search by name, email or position" in html
    assert "oninput=\"loadCandidates()\"" in html
    assert "onchange=\"loadCandidates()\"" in html
    assert "filterCandidates" in html or "loadCandidates()" in html
    assert "clearCandidateFilters()" in html


def test_arms_21_edit_remove_candidate():
    html = _read(os.path.join(PROJECT_ROOT, "dashboards", "hr-dashboard.html"))

    assert "editCandidate(candidateId)" in html
    assert "removeCandidateFromPosition" in html
    assert "removeCandidateFromAllPositions" in html
    assert "already exists" in html.lower() or "already linked" in html.lower()
    assert "Remove All" in html
    assert "confirm(" in html
    assert "Hired decision" in html


def test_arms_22_delete_replace_cv():
    html = _read(os.path.join(PROJECT_ROOT, "dashboards", "hr-dashboard.html"))

    assert "deleteUploadedCV" in html
    assert "prepareCVReplacement" in html
    assert "Delete this uploaded CV" in html
    assert "Replace" in html
    assert "This candidate already has a CV uploaded" in html
    assert "Selected" in html and "CV replacement" in html
    assert "Only PDF, DOC, or DOCX files allowed" in html

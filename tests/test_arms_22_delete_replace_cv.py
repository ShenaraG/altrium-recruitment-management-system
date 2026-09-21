import os

from conftest import PROJECT_ROOT


def test_arms_22_delete_replace_cv():
    html = open(os.path.join(PROJECT_ROOT, "dashboards", "hr-dashboard.html"), "r", encoding="utf-8").read()

    assert "deleteUploadedCV" in html
    assert "prepareCVReplacement" in html
    assert "Delete this uploaded CV" in html
    assert "Replace" in html
    assert "Only PDF, DOC, or DOCX files allowed" in html
    assert "cvCandidateSelect" in html
    assert "This candidate already has a CV uploaded" in html or "existingCV" in html

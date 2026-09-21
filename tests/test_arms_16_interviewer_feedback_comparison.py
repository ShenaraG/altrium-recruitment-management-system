import os

from conftest import PROJECT_ROOT


def test_arms_16_interviewer_feedback_comparison():
    html = open(os.path.join(PROJECT_ROOT, "dashboards", "hiring-manager-dashboard.html"), "r", encoding="utf-8").read()

    assert "loadFeedbackForPosition()" in html
    assert "feedbackSortSelect" in html
    assert "Object.values(data.reduce" in html or "grouped" in html.lower()
    assert "No feedback submitted for this position yet." in html
    assert "Highest rating first" in html
    assert "Lowest rating first" in html
    assert "View Feedback" in html

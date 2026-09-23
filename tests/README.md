# Sprint 2 Selenium tests (ARMS-16 → ARMS-22)

One file per backlog story, each test mapped to specific acceptance
criteria (see the docstring at the top of each file).

| File | Story |
|---|---|
| `test_arms_16_interviewer_feedback_comparison.py` | ARMS-16 Interviewer Feedback Comparison |
| `test_arms_17_retention_date_enhancement.py` | ARMS-17 Retention Date Enhancement |
| `test_arms_18_management_dashboard_overview.py` | ARMS-18 Management Recruitment Dashboard |
| `test_arms_19_hr_recruitment_pipeline_overview.py` | ARMS-19 HR Recruitment Pipeline Overview |
| `test_arms_20_candidate_search_and_filtering.py` | ARMS-20 Candidate Search and Filtering |
| `test_arms_21_edit_remove_candidate.py` | ARMS-21 Edit/Remove Candidate |
| `test_arms_22_delete_replace_cv.py` | ARMS-22 Delete/Replace CV |

These are newly written (not the older smoke-test versions already in
the repo's git history) — drop them into your existing `tests/`
folder alongside this `conftest.py`.

## Running

```bash
pip install -r requirements.txt   # selenium, pytest
# Chrome + a matching chromedriver must be installed and on PATH.

# Serve the app locally (any static server works):
python -m http.server 8000

# In another terminal:
pytest tests/ -v
```

By default the tests look for the app at `http://localhost:5500`,
`http://localhost:8000`, or the 127.0.0.1 equivalents. Point at a
different host with:

```bash
ALTRIUM_BASE_URL=http://localhost:5500 pytest tests/ -v
```

These are **live end-to-end tests**: `config.js` points the app at a
real Supabase project, so the browser session created by each test
signs in for real and reads/writes real rows. They need:

- Working test accounts in that Supabase project matching
  `tests/conftest.py::TEST_ACCOUNTS` (`sarah@altrium.com` = HR
  recruiter, `james@altrium.com` = interviewer, `emma@altrium.com` =
  hiring manager, `michael@altrium.com` = management — all password
  `Test1234`).
- Some seed data: at least one closed position with a retention date,
  a handful of candidates (including one linked to 2+ positions and
  one with a recorded "Hired" decision), some interviewer feedback on
  at least one position, and an uploaded CV or two.

Where a test's precondition isn't met (e.g. no closed position exists
yet to update a retention date on), it calls `pytest.skip()` with a
message explaining what's missing, rather than reporting a false pass
or crashing the whole run.

## Notes on what changed from the previous suite

The previous version of these files (still visible in git history,
e.g. commit `8cbd403`) mostly logged in, navigated to a section, and
asserted a heading/element was present — i.e. "the page didn't
crash." That's useful as a smoke test but doesn't verify the actual
acceptance criteria. In particular the old ARMS-17 test never
interacted with a retention date at all.

This version drives the real interactions per story: the
`window.prompt`/`confirm` dialogs the app uses for retention dates and
CV deletion, search/filter inputs, sort dropdowns, role-based access
redirects, and a full upload → replace → delete round trip for CVs
that's self-contained (it picks a candidate with no existing CV so it
never overwrites or deletes someone else's real uploaded file).

---
title: Allure Reporting
category: tool
tags: [allure, reporting, test-report, annotations, steps, attachments, allure-testops]
---
# Allure Reporting

Rich test reporting framework - visual dashboards, test steps, attachments, history, CI integration.

## Key Facts

- `allure-pytest` plugin + `allure` CLI for report generation
- Run: `pytest --alluredir=allure-results` then `allure serve allure-results`
- Annotations: `@allure.title()`, `@allure.description()`, `@allure.severity()`
- Behavioral hierarchy: `@allure.epic()`, `@allure.feature()`, `@allure.story()` - group tests by business logic
- Steps: `@allure.step()` decorator or `with allure.step("description"):` context manager
- Attachments: `allure.attach()` for screenshots, logs, request/response data
- Severity levels: BLOCKER, CRITICAL, NORMAL (default), MINOR, TRIVIAL
- `allure.link()`, `allure.issue()`, `allure.testcase()` - link to external systems
- Allure TestOps (TMS) - commercial platform for test management with Allure integration
- Publish to GitHub Pages for team-accessible reports

## Patterns

```python
import allure
import pytest

# Title and description
@allure.title("Create user via API")
@allure.description("Verify user creation with valid data returns 201")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_user(api_client):
    ...

# Epic / Feature / Story hierarchy
@allure.epic("User Management")
@allure.feature("Authentication")
@allure.story("Login")
def test_login():
    ...

# Steps as decorators
@allure.step("Send POST request to {endpoint}")
def send_post(endpoint, data):
    return requests.post(endpoint, json=data)

@allure.step("Verify response status is {expected}")
def check_status(response, expected):
    assert response.status_code == expected

# Steps as context manager
def test_full_flow():
    with allure.step("Prepare test data"):
        user = {"name": "Test", "email": "test@example.com"}

    with allure.step("Create user"):
        resp = api_client.post("/users", json=user)

    with allure.step("Verify response"):
        assert resp.status_code == 201

# Attachments
def test_with_attachments(page):
    page.goto("/dashboard")

    # Screenshot
    allure.attach(
        page.screenshot(),
        name="dashboard_screenshot",
        attachment_type=allure.attachment_type.PNG
    )

    # JSON data
    allure.attach(
        json.dumps(response_data, indent=2),
        name="api_response",
        attachment_type=allure.attachment_type.JSON
    )

    # Request URL
    allure.attach(
        str(request.url),
        name="request_url",
        attachment_type=allure.attachment_type.TEXT
    )

# Link to bug tracker
@allure.issue("JIRA-123", "Login button broken")
@allure.testcase("TMS-456", "Login test case")
@allure.link("https://docs.example.com/api", name="API docs")
def test_with_links():
    ...

# Severity levels
@allure.severity(allure.severity_level.BLOCKER)
def test_payment_flow():
    ...

@allure.severity(allure.severity_level.MINOR)
def test_tooltip_text():
    ...

# Allure environment info (environment.properties)
# allure-results/environment.properties
# Browser=Chrome 120
# Environment=Staging
# API.Version=v2

# Programmatic environment properties
import json
import os

def pytest_sessionfinish(session):
    env_props = {
        "Browser": "Chrome",
        "Base URL": os.getenv("BASE_URL", "localhost"),
        "Python": platform.python_version(),
    }
    allure_dir = session.config.option.allure_report_dir
    if allure_dir:
        with open(os.path.join(allure_dir, "environment.properties"), "w") as f:
            for k, v in env_props.items():
                f.write(f"{k}={v}\n")
```

## Gotchas

- **Symptom**: "allure: command not found" - **Cause**: Allure CLI not installed - **Fix**: `brew install allure` (macOS), `scoop install allure` (Windows), or download from GitHub
- **Symptom**: report shows no history - **Cause**: `allure-results` cleared between runs - **Fix**: keep `allure-report/history` directory and copy it to `allure-results/history` before generating
- **Symptom**: steps show fixture names, not business steps - **Cause**: no `@allure.step()` decorators - **Fix**: add allure steps to test functions and helper methods
- Allure results are JSON files - generate the HTML report with `allure generate` or `allure serve`
- On CI, publish report as artifact or to GitHub Pages for team access

## See Also

- [[ci-cd-test-automation]] - publishing Allure reports in CI pipelines
- [[api-testing-requests]] - attaching API request/response data
- [[pytest-fundamentals]] - pytest integration
- [Allure pytest docs](https://allurereport.org/docs/pytest/)
- [Allure Report](https://allurereport.org/)

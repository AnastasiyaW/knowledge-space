---
title: Allure Reporting
category: tool
tags: [allure, reporting, test-report, annotations, steps, attachments, hooks, middleware]
---

# Allure Reporting

Allure generates rich HTML test reports with steps, attachments, history, and trends. Used as team communication tool - reports should be readable by non-technical members. Integration via annotations (`@allure.feature`, `@allure.step`) + automatic HTTP logging via session hooks + CI publishing to GitHub Pages or Jenkins.

## Key Facts

- Annotations: `@allure.feature`, `@allure.story`, `@allure.step`, `@allure.severity`
- `allure.attach()` adds screenshots, HTTP logs, videos, page source to report
- Session hooks (`session.hooks["response"]`) auto-attach ALL HTTP interactions
- `pytest_runtest_call` hook with `trylast=True, hookwrapper=True` overrides Allure test status
- Report = `allure generate allure-results -o allure-report --clean`
- Start annotating from day one, not as afterthought

## Patterns

### Test Annotations

```python
@allure.feature("Spending")
@allure.story("Create spending")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_spending(authenticated_client):
    with allure.step("Create new spending entry"):
        spend = authenticated_client.add_spend({"amount": 100})

    with allure.step("Verify spending appears in list"):
        all_spends = authenticated_client.get_spends()
        assert spend["id"] in [s["id"] for s in all_spends]
```

### Auto-Attach HTTP Logs via Session Hooks

```python
class ApiClient:
    def __init__(self, base_url, token):
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {token}"
        self.session.hooks["response"].append(self._attach)

    @staticmethod
    def _attach(response, *args, **kwargs):
        allure.attach(
            body=response.text,
            name=f"{response.request.method} {response.url} [{response.status_code}]",
            attachment_type=allure.attachment_type.TEXT,
        )
```

### Failure Attachments (Screenshot + Page Source)

```python
@pytest.fixture(autouse=True)
def attach_on_failure(request, driver):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(),
                      name="screenshot", attachment_type=allure.attachment_type.PNG)
        allure.attach(driver.page_source,
                      name="page_source", attachment_type=allure.attachment_type.HTML)
```

### Override Allure Status via Hook

```python
@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_runtest_call(item):
    yield
    # After yield: Allure has recorded its result
    # Can now override status, add custom data, etc.
```

## Gotchas

- Response hooks may log sensitive data (auth headers, tokens) - add masking filters
- `allure.attach` in response hooks fires for EVERY HTTP call - can produce large reports
- Allure history requires persisting `allure-results/history` between runs
- Jenkins plugin auto-generates reports; GitHub Actions needs explicit generate + Pages deploy step

## See Also

- [[pytest-fundamentals]] - pytest hooks that Allure integrates with
- [[ci-cd-test-automation]] - publishing Allure reports in CI
- [[api-testing-tools]] - HTTP client with auto-logging
- [[test-architecture]] - where Allure fits in test project structure

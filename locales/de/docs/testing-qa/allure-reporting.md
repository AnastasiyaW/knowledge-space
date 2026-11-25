---
title: "Allure Reporting"
category: tool
tags: [allure, reporting, test-report, annotations, steps, attachments, hooks, middleware]
level: 3
source_sha256: 02559aa6c7d6073279ded5a7d5f25b3801d9a63259e0e2de59668b194bf2f7b4
translation: machine
translated_at: '2026-10-24'
---
# Allure Reporting {#allure-reporting}

Allure erzeugt umfangreiche HTML-Testberichte mit Schritten, Anhängen, Verlauf und Trends. Es wird als Kommunikationswerkzeug im Team eingesetzt: Berichte sollten auch für nicht-technische Teammitglieder lesbar sein. Die Integration erfolgt über Annotationen (`@allure.feature`, `@allure.step`), automatisches HTTP-Logging über Session-Hooks und die Veröffentlichung in der CI auf GitHub Pages oder Jenkins.

## Key Facts {#key-facts}

- Annotationen: `@allure.feature`, `@allure.story`, `@allure.step`, `@allure.severity`
- `allure.attach()` fügt Screenshots, HTTP-Logs, Videos und Page Source zum Bericht hinzu
- Session-Hooks (`session.hooks["response"]`) hängen automatisch ALLE HTTP-Interaktionen an
- Der Hook `pytest_runtest_call` mit `trylast=True, hookwrapper=True` überschreibt den Teststatus von Allure
- Bericht = `allure generate allure-results -o allure-report --clean`
- Mit dem Annotieren von Anfang an beginnen, nicht als nachträglichen Gedanken

## Patterns {#patterns}

### Test Annotations {#test-annotations}

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

### Auto-Attach HTTP Logs via Session Hooks {#auto-attach-http-logs-via-session-hooks}

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

### Failure Attachments (Screenshot + Page Source) {#failure-attachments-screenshot-page-source}

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

### Override Allure Status via Hook {#override-allure-status-via-hook}

```python
@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_runtest_call(item):
    yield
    # After yield: Allure has recorded its result
    # Can now override status, add custom data, etc.
```

## Gotchas {#gotchas}

- Response-Hooks können sensible Daten protokollieren (Auth-Header, Tokens) – Masking-Filter hinzufügen
- `allure.attach` in Response-Hooks wird für JEDEN HTTP-Aufruf ausgelöst – kann zu sehr großen Berichten führen
- Der Allure-Verlauf erfordert, dass `allure-results/history` zwischen den Läufen erhalten bleibt
- Das Jenkins-Plugin erzeugt Berichte automatisch; GitHub Actions benötigt einen expliziten Generate-Schritt und einen Pages-Deploy-Schritt

## See Also {#see-also}

- [[pytest-fundamentals]] - pytest-Hooks, in die Allure sich integriert
- [[ci-cd-test-automation]] - Veröffentlichung von Allure-Berichten in der CI
- [[api-testing-tools]] - HTTP-Client mit automatischem Logging
- [[test-architecture]] - Einordnung von Allure in die Struktur des Testprojekts

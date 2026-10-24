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

Allure génère des rapports de tests HTML riches, avec étapes, pièces jointes, historique et tendances. Utilisé comme outil de communication d'équipe : les rapports doivent être lisibles par des membres non techniques. L'intégration repose sur des annotations (`@allure.feature`, `@allure.step`), une journalisation HTTP automatique via des hooks de session et une publication en CI sur GitHub Pages ou Jenkins.

## Points clés {#key-facts}

- Annotations : `@allure.feature`, `@allure.story`, `@allure.step`, `@allure.severity`
- `allure.attach()` ajoute au rapport des captures d'écran, journaux HTTP, vidéos, sources de page
- Les hooks de session (`session.hooks["response"]`) attachent automatiquement TOUTES les interactions HTTP
- Le hook `pytest_runtest_call` avec `trylast=True, hookwrapper=True` remplace le statut de test Allure
- Rapport = `allure generate allure-results -o allure-report --clean`
- Commencer à annoter dès le premier jour, et non en dernier recours

## Modèles {#patterns}

### Annotations de tests {#test-annotations}

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

### Journalisation HTTP automatique via les hooks de session {#auto-attach-http-logs-via-session-hooks}

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

### Pièces jointes en cas d'échec (capture d'écran + source de page) {#failure-attachments-screenshot-page-source}

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

### Remplacer le statut Allure via un hook {#override-allure-status-via-hook}

```python
@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_runtest_call(item):
    yield
    # After yield: Allure has recorded its result
    # Can now override status, add custom data, etc.
```

## Pièges à éviter {#gotchas}

- Les hooks de réponse peuvent journaliser des données sensibles (en-têtes d'authentification, jetons) : ajoutez des filtres de masquage
- `allure.attach` dans les hooks de réponse se déclenche pour CHAQUE appel HTTP : cela peut produire des rapports très volumineux
- L'historique Allure nécessite de conserver `allure-results/history` entre les exécutions
- Le plugin Jenkins génère les rapports automatiquement ; GitHub Actions nécessite une étape explicite de génération et de déploiement sur Pages

## Voir aussi {#see-also}

- [[pytest-fundamentals]] - hooks pytest avec lesquels Allure s'intègre
- [[ci-cd-test-automation]] - publication des rapports Allure en CI
- [[api-testing-tools]] - client HTTP avec journalisation automatique
- [[test-architecture]] - place d'Allure dans la structure d'un projet de tests

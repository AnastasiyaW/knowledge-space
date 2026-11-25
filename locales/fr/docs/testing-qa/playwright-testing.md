---
title: "Tests Playwright"
category: tool
tags: [playwright, browser-automation, ui-testing, auto-wait, codegen, trace, assertions, locators]
level: 3
source_sha256: f512a341abed0654ba43a842640eaa570a2864376457fcadf46083d6a25c8abc
translation: machine
translated_at: '2026-10-24'
---
# Tests Playwright {#playwright-testing}

Playwright est un framework moderne d'automatisation de navigateur développé par Microsoft. Avantage clé par rapport à Selenium : attente automatique des éléments, assertions intégrées avec relances, trace viewer pour le débogage, et codegen pour enregistrer les tests. Prend en charge Chromium, Firefox et WebKit à partir d'une seule API.

## Points clés {#key-facts}

- **Auto-wait** : chaque action attend que l'élément soit actionnable (visible, stable, activé)
- **Assertions intégrées** : `expect(locator).to_have_text("...")` relance automatiquement jusqu'au délai d'expiration
- **Codegen** : `playwright codegen URL` enregistre les actions sous forme de code de test
- **Trace viewer** : enregistre les captures d'écran, les instantanés DOM, le réseau et la console pour chaque action
- Prend en charge Chromium, Firefox, WebKit ; mode sans interface (headless) par défaut
- Plusieurs contextes de navigateur = sessions parallèles indépendantes (utilisateurs différents, cookies distincts)

## Modèles {#patterns}

### Intégration avec Pytest {#pytest-integration}

```python
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
```

### Localisateurs (à privilégier par rapport à CSS/XPath) {#locators-prefer-over-cssxpath}

```python
# Role-based (most stable, accessibility-first)
page.get_by_role("button", name="Submit")
page.get_by_role("textbox", name="Email")

# Text and label
page.get_by_text("Welcome")
page.get_by_label("Password")
page.get_by_placeholder("Enter email")

# Test ID
page.get_by_test_id("submit-btn")

# CSS/XPath still available
page.locator("css=#username")
```

### Trace Viewer {#trace-viewer}

```python
context.tracing.start(screenshots=True, snapshots=True, sources=True)
# ... test actions ...
context.tracing.stop(path="trace.zip")
# View: playwright show-trace trace.zip
```

### Contextes multiples (utilisateurs parallèles) {#multiple-contexts-parallel-users}

```python
admin_ctx = browser.new_context()
user_ctx = browser.new_context()
admin_page = admin_ctx.new_page()
user_page = user_ctx.new_page()
# Independent sessions (separate cookies, storage)
```

## Pièges {#gotchas}

- L'auto-wait s'applique par action, et non par assertion : utilisez `expect()` pour les assertions (relances automatiques)
- `page.wait_for_timeout(ms)` annule l'intérêt de la démarche : utilisez `expect()` avec un délai d'expiration personnalisé
- La sortie de codegen constitue un point de départ : refactorisez pour utiliser des localisateurs par rôle/libellé et le POM
- Les contextes de navigateur sont isolés : l'état ne persiste pas d'un contexte à l'autre

## Voir aussi {#see-also}

- [[selenium-webdriver]] - alternative plus ancienne, écosystème plus large
- [[page-object-model]] - le motif POM s'applique aussi à Playwright
- [[allure-reporting]] - intégration des résultats Playwright avec Allure

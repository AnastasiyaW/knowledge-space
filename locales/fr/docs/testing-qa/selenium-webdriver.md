---
title: "Selenium WebDriver"
category: tool
tags: [selenium, webdriver, browser-automation, ui-testing, waits, css-selectors, xpath, data-testid, locators]
level: 3
source_sha256: 8e293d9d96272b637d9f17875a7bfbff8bf677d5930b785037297337cd97a056
translation: machine
translated_at: '2026-10-24'
---
# Selenium WebDriver {#selenium-webdriver}

Selenium automatise les navigateurs via le protocole W3C WebDriver. Architecture en trois niveaux : client Python -> WebDriver (ChromeDriver) -> navigateur. Les principaux défis sont les localisateurs d'éléments, les attentes et la gestion des versions des pilotes. Utilisez `webdriver-manager` pour la gestion automatique des versions et des attentes explicites pour la stabilité.

## Key Facts {#key-facts}

- Architecture : client (bibliothèque selenium) -> binaire WebDriver -> navigateur (protocole HTTP)
- La version de ChromeDriver DOIT correspondre à la version de Chrome ; `webdriver-manager` la résout automatiquement
- Stratégies de localisation : sélecteurs CSS, XPath, ID, name, data-testid (le plus stable)
- **N'utilisez jamais `time.sleep()`** - les attentes explicites avec conditions sont fiables et rapides
- Les attentes implicites sont globales ; les attentes explicites sont propres à chaque élément (privilégiez les attentes explicites)
- Les attributs `data-testid` fournissent des localisateurs stables, indépendants des changements de CSS et de style

## Patterns {#patterns}

### Setup with Auto-Versioning {#setup-with-auto-versioning}

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

### Locator Strategies {#locator-strategies}

```python
from selenium.webdriver.common.by import By

# CSS Selectors (fast, familiar)
driver.find_element(By.CSS_SELECTOR, "#username")           # by ID
driver.find_element(By.CSS_SELECTOR, ".login-form")         # by class
driver.find_element(By.CSS_SELECTOR, "input[name='email']") # by attribute
driver.find_element(By.CSS_SELECTOR, "[data-testid='submit-btn']")  # test ID

# XPath (more powerful, can search by text and traverse up)
driver.find_element(By.XPATH, "//h1[text()='Welcome']")
driver.find_element(By.XPATH, "//div[contains(@class, 'error')]")
driver.find_element(By.XPATH, "//input[@type='text'][2]")  # 1-indexed!
```

**CSS vs XPath** : CSS est plus court et plus rapide pour les cas simples. XPath permet de rechercher par contenu textuel et de remonter dans le DOM (axes parent/ancêtre).

### Explicit Waits (Always Prefer) {#explicit-waits-always-prefer}

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#result")))
element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button")))
```

### Common Interactions {#common-interactions}

```python
# Navigation
driver.get("https://example.com")
driver.back(); driver.forward(); driver.refresh()

# Elements
element.clear(); element.send_keys("text"); element.click()
element.text; element.get_attribute("value")

# Select dropdown
from selenium.webdriver.support.select import Select
Select(driver.find_element(By.CSS_SELECTOR, "#menu")).select_by_visible_text("Option")

# File upload
driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys("/path/to/file.png")

# Alerts
alert = driver.switch_to.alert
alert.accept()   # OK
alert.dismiss()  # Cancel

# iFrames
driver.switch_to.frame("frameName")
driver.switch_to.default_content()  # back to main
```

### Headless and CI Options {#headless-and-ci-options}

```python
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")  # required in Docker
driver = webdriver.Chrome(options=options)
```

## Gotchas {#gotchas}

- `find_element` lève `NoSuchElementException` si l'élément n'est pas trouvé : utilisez des attentes ou un try/except
- Références d'éléments obsolètes (stale) après des changements du DOM (AJAX, navigation) : relancez la recherche de l'élément
- Les éléments d'un iFrame sont invisibles depuis le contexte principal : il faut d'abord appeler `switch_to.frame()`
- Selenium Grid est lourd ; privilégiez Selenoid (basé sur Docker, plus léger, avec enregistrement vidéo intégré)

## See Also {#see-also}

- [[playwright-testing]] - alternative moderne avec attentes automatiques
- [[page-object-model]] - organisation des localisateurs et des actions en classes
- [[ci-cd-test-automation]] - Selenoid pour les tests de navigateur en CI

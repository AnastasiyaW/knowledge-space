---
title: "Page Object Model"
category: pattern
tags: [page-object, design-pattern, selenium, playwright, ui-testing, maintainability, abstraction]
level: 3
source_sha256: 4b0284039edbca37b9cc94c1274b092bf7c69a42c6a9fedebb62d24d9af380e3
translation: machine
translated_at: '2026-10-24'
---
# Page Object Model {#page-object-model}

Das Page Object Model (POM) kapselt jede Webseite als Klasse: Locators als Attribute, Aktionen als Methoden. Tests interagieren mit Page Objects, niemals mit direkten Driver-Aufrufen. Eine Änderung eines Locators bedeutet eine Klassenaktualisierung, nicht eine Anpassung in jedem Test. Funktioniert mit Selenium, Playwright und mobilen Tests (Kaspresso Screen Objects).

## Key Facts {#key-facts}

- Jede Seite bzw. Komponente ist eine Klasse mit Locators als Klassenattributen und Aktionen als Methoden
- **Assertions gehören in die Tests, NICHT in Page Objects** - Seiten stellen Daten bereit, Tests prüfen sie
- Methoden geben `self` oder das nächste Page Object zurück, um Aufrufe verketten zu können
- Locators auf einheitlicher Abstraktionsebene (entweder alle "Feld ausfüllen" oder alle "Formular ausfüllen", nicht gemischt)
- Felder nach der UI-Terminologie benennen (steht im Formular "Date of Birth", heißt das Feld `date_of_birth`)
- Komponenten-Objekte (Header, Navigation, Footer) erweitern das POM für wiederverwendbare Seitenbereiche

## Patterns {#patterns}

### Basic Page Object {#basic-page-object}

```python
class LoginPage:
    URL = "/login"
    USERNAME = (By.CSS_SELECTOR, "#username")
    PASSWORD = (By.CSS_SELECTOR, "#password")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR = (By.CSS_SELECTOR, ".error-message")

    def __init__(self, driver):
        self.driver = driver

    def open(self, base_url):
        self.driver.get(f"{base_url}{self.URL}")
        return self

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME).clear()
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.driver.find_element(*self.PASSWORD).clear()
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.SUBMIT).click()
        return MainPage(self.driver)  # returns next page

    def get_error_text(self):
        return self.driver.find_element(*self.ERROR).text
```

### Test Using Page Object {#test-using-page-object}

```python
def test_login_error(browser, base_url):
    page = LoginPage(browser).open(base_url).login("bad", "creds")
    # Assertion in test, NOT in page object
    assert page.get_error_text() == "Invalid credentials"
```

### Fixture Integration {#fixture-integration}

```python
@pytest.fixture
def login_page(browser, base_url):
    return LoginPage(browser).open(base_url)

@pytest.fixture
def authenticated_page(login_page, app_user):
    username, password = app_user
    return login_page.login(username, password)

def test_dashboard(authenticated_page):
    assert authenticated_page.get_title() == "Dashboard"
```

### Kaspresso Screen Objects (Android) {#kaspresso-screen-objects-android}

```kotlin
object MainScreen : KScreen<MainScreen>() {
    override val layoutId = R.layout.activity_main
    override val viewClass = MainActivity::class.java

    val title = KTextView { withId(R.id.title) }
    val submitButton = KButton { withId(R.id.submit_button) }
}
```

## Gotchas {#gotchas}

- Assertions in Page Objects zu verstecken erschwert die Fehleranalyse
- Gemischte Abstraktionsebenen ("Namen ausfüllen" und "gesamtes Formular absenden" in derselben Klasse) führen zu Verwirrung
- Tiefe Seitenhierarchien erhöhen die Komplexität – flach halten, solange es nicht wirklich nötig ist
- Screenshots: in Fixtures bzw. Teardown mit eindeutigen Dateinamen erstellen, nicht innerhalb von Page Objects

## See Also {#see-also}

- [[selenium-webdriver]] - Selenium-spezifische Locators und Interaktionen
- [[playwright-testing]] - Playwright-Locators mit rollenbasierter Strategie
- [[test-architecture]] - Organisation von Page Objects in der Projektstruktur

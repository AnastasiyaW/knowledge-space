---
title: "Modèle d'objets de page"
category: pattern
tags: [page-object, design-pattern, selenium, playwright, ui-testing, maintainability, abstraction]
level: 3
source_sha256: 4b0284039edbca37b9cc94c1274b092bf7c69a42c6a9fedebb62d24d9af380e3
translation: machine
translated_at: '2026-10-24'
---
# Modèle d'objets de page {#page-object-model}

Le Modèle d'objets de page (Page Object Model, POM) encapsule chaque page web dans une classe : les localisateurs sont des attributs, et les actions sont des méthodes. Les tests interagissent avec les objets de page, jamais directement avec les appels bruts du driver. Un changement de localisateur = une seule mise à jour de classe, et non une mise à jour dans chaque test. Fonctionne avec Selenium, Playwright et le mobile (objets d'écran Kaspresso).

## Points clés {#key-facts}

- Chaque page ou composant = une classe, avec les localisateurs en attributs de classe et les actions en méthodes
- **Les assertions appartiennent aux tests, PAS aux objets de page** : les pages exposent les données, les tests les vérifient
- Les méthodes retournent `self` ou l'objet de page suivant pour permettre l'enchaînement
- Localisateurs à un niveau d'abstraction cohérent (tous « remplir le champ » ou tous « remplir le formulaire », sans mélange)
- Nommer les champs avec la terminologie de l'interface (si le formulaire indique « Date de naissance », le champ est `date_of_birth`)
- Les objets composants (en-tête, navigation, pied de page) étendent POM pour les sections réutilisables de page

## Modèles {#patterns}

### Objet de page de base {#basic-page-object}

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

### Test utilisant un objet de page {#test-using-page-object}

```python
def test_login_error(browser, base_url):
    page = LoginPage(browser).open(base_url).login("bad", "creds")
    # Assertion in test, NOT in page object
    assert page.get_error_text() == "Invalid credentials"
```

### Intégration avec les fixtures {#fixture-integration}

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

### Objets d'écran Kaspresso (Android) {#kaspresso-screen-objects-android}

```kotlin
object MainScreen : KScreen<MainScreen>() {
    override val layoutId = R.layout.activity_main
    override val viewClass = MainActivity::class.java

    val title = KTextView { withId(R.id.title) }
    val submitButton = KButton { withId(R.id.submit_button) }
}
```

## Pièges à éviter {#gotchas}

- Cacher les assertions dans les objets de page rend les échecs plus difficiles à diagnostiquer
- Des niveaux d'abstraction mélangés (« remplir le nom » et « soumettre le formulaire entier » dans la même classe) créent de la confusion
- Des hiérarchies de pages profondes ajoutent de la complexité : gardez-les plates, sauf si c'est réellement nécessaire
- Captures d'écran : les réaliser dans les fixtures ou le teardown, avec des noms de fichiers uniques, et non dans les objets de page

## Voir aussi {#see-also}

- [[selenium-webdriver]] - Localisateurs et interactions propres à Selenium
- [[playwright-testing]] - Localisateurs Playwright avec stratégie basée sur les rôles
- [[test-architecture]] - organisation des objets de page dans la structure du projet

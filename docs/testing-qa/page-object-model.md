---
title: Page Object Model
category: pattern
tags: [page-object, design-pattern, selenium, playwright, ui-testing, maintainability, abstraction]
---

# Page Object Model

Page Object Model (POM) encapsulates each web page as a class: locators as attributes, actions as methods. Tests interact with page objects, never raw driver calls. One locator change = one class update, not every test. Works with Selenium, Playwright, and mobile (Kaspresso screen objects).

## Key Facts

- Each page/component = one class with locators as class attributes and actions as methods
- **Assertions belong in tests, NOT in page objects** - pages expose data, tests verify
- Methods return `self` or the next page object for chaining
- Locators at consistent abstraction level (all "fill field" or all "complete form", not mixed)
- Name fields using UI terminology (if form says "Date of Birth", field = `date_of_birth`)
- Component objects (header, nav, footer) extend POM for reusable page sections

## Patterns

### Basic Page Object

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

### Test Using Page Object

```python
def test_login_error(browser, base_url):
    page = LoginPage(browser).open(base_url).login("bad", "creds")
    # Assertion in test, NOT in page object
    assert page.get_error_text() == "Invalid credentials"
```

### Fixture Integration

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

### Kaspresso Screen Objects (Android)

```kotlin
object MainScreen : KScreen<MainScreen>() {
    override val layoutId = R.layout.activity_main
    override val viewClass = MainActivity::class.java

    val title = KTextView { withId(R.id.title) }
    val submitButton = KButton { withId(R.id.submit_button) }
}
```

## Gotchas

- Hiding assertions inside page objects makes failures harder to diagnose
- Mixed abstraction levels ("fill name" + "submit entire form" in same class) cause confusion
- Deep page hierarchies add complexity - keep it flat unless genuinely needed
- Screenshots: capture in fixtures/teardown with unique filenames, not inside page objects

## See Also

- [[selenium-webdriver]] - Selenium-specific locators and interactions
- [[playwright-testing]] - Playwright locators with role-based strategy
- [[test-architecture]] - organizing page objects in project structure

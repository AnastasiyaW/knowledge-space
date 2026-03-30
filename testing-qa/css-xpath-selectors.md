---
title: CSS and XPath Selectors
category: technique
tags: [selectors, css, xpath, locators, dom, devtools]
---
# CSS and XPath Selectors

Locator strategies for finding elements in the DOM - foundation of UI test automation.

## Key Facts

- CSS selectors are faster and more readable; XPath is more powerful for complex traversal
- Priority for locator strategies: `data-testid` > `id` > CSS selector > XPath
- Browser DevTools: right-click element > Inspect > copy CSS/XPath selector
- Avoid brittle locators: auto-generated selectors with nth-child chains, inline styles
- `data-testid` attributes provide stable, test-specific selectors unaffected by UI changes
- CSS cannot select parent elements; XPath can traverse up the DOM tree
- Playwright prefers role-based locators (`get_by_role`, `get_by_text`) over raw CSS/XPath

## Patterns

```python
# CSS Selectors
"#login-form"                    # by ID
".btn-primary"                   # by class
"input[type='email']"            # by attribute
"[data-testid='submit-btn']"     # by data-testid (preferred)
"div.card > h2"                  # direct child
"form input.email"               # descendant
"li:first-child"                 # pseudo-class
"li:nth-child(3)"                # nth child
"input:not([disabled])"          # negation
"div.list > div:last-child"      # last child
"a[href*='login']"               # attribute contains
"a[href^='https']"               # attribute starts with
"a[href$='.pdf']"                # attribute ends with
"input[name='user'][type='text']" # multiple attributes

# XPath Selectors
"//input[@id='username']"        # by attribute
"//button[text()='Submit']"      # by exact text
"//button[contains(text(), 'Log')]"  # by partial text
"//div[@class='card']//h2"       # descendant
"//div[@class='card']/h2"        # direct child
"//input[@type='text']/parent::div"  # parent (CSS can't do this)
"//li[position()=3]"             # by position
"//div[contains(@class, 'active')]"  # class contains
"//input[not(@disabled)]"        # negation
"(//div[@class='item'])[2]"      # second match
"//td[text()='Price']/following-sibling::td"  # sibling

# Playwright-specific locators (preferred over raw CSS/XPath)
page.get_by_role("button", name="Submit")
page.get_by_label("Email")
page.get_by_placeholder("Enter email")
page.get_by_text("Welcome back")
page.get_by_test_id("login-form")
page.locator("css=div.card >> text=Title")

# Selenium locators
from selenium.webdriver.common.by import By
driver.find_element(By.ID, "username")
driver.find_element(By.CSS_SELECTOR, "[data-testid='btn']")
driver.find_element(By.XPATH, "//button[text()='OK']")
driver.find_element(By.LINK_TEXT, "Click here")
driver.find_element(By.PARTIAL_LINK_TEXT, "Click")
```

## Gotchas

- **Symptom**: locator finds wrong element - **Cause**: selector not unique on the page - **Fix**: add more specificity or use `data-testid`
- **Symptom**: tests break after minor UI redesign - **Cause**: brittle locators tied to DOM structure - **Fix**: use `data-testid` attributes that survive refactors
- **Symptom**: XPath `text()='Submit'` doesn't match - **Cause**: whitespace around text or text split across child elements - **Fix**: use `contains(text(), 'Submit')` or `normalize-space()`
- Text-based locators break with internationalization (i18n) - `data-testid` is locale-independent
- Verify selectors in browser DevTools Console: `document.querySelector("css")` or `$x("xpath")`

## See Also

- [[page-object-model]] - organizing locators in page objects
- [[test-identifiers]] - adding data-testid to frontend code
- [[playwright-testing]] - Playwright's built-in locator strategies
- [[selenium-webdriver]] - Selenium locator usage
- [CSS Selectors reference (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)
- [XPath reference (MDN)](https://developer.mozilla.org/en-US/docs/Web/XPath)

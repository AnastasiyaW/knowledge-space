---
title: Testing & QA Knowledge Base
category: index
tags: [testing, qa, test-automation, pytest, playwright, selenium, api-testing]
---
# Testing & QA Knowledge Base

Reference knowledge base for test automation with Python - frameworks, patterns, tools, CI/CD integration.

## Frameworks & Core

### Pytest
- [[pytest-fundamentals]] - test discovery, assertions, markers, conftest, configuration
- [[pytest-fixtures]] - scopes, yield teardown, factory pattern, dependency injection
- [[pytest-parametrize]] - data-driven testing, cartesian product, indirect parametrize
- [[pytest-plugins-and-parallel]] - xdist parallel execution, rerunfailures, hooks, timeout

### Design Patterns
- [[page-object-model]] - encapsulate page structure, base page class, component pattern
- [[test-project-structure]] - directory layout, dependency management, CI-ready setup

## Browser Automation

- [[playwright-testing]] - auto-waiting, codegen, trace viewer, network mocking, get_by_test_id
- [[selenium-webdriver]] - WebDriver protocol, explicit waits, ActionChains, headless mode
- [[css-xpath-selectors]] - CSS vs XPath, locator priority, attribute selectors, DevTools
- [[test-identifiers]] - data-testid attributes, adding to React/frontend apps, naming conventions

## API Testing

- [[api-testing-requests]] - requests/httpx, API client class, JSON schema validation, CRUD flows
- [[pydantic-test-validation]] - response models, BaseSettings for config, type-safe validation

## Infrastructure & Tooling

- [[allure-reporting]] - annotations, steps, attachments, severity, GitHub Pages publishing
- [[ci-cd-test-automation]] - GitHub Actions, GitLab CI, pipeline configuration, secrets
- [[logging-in-tests]] - Python logging in test frameworks, pytest log config, structured output

## Methodology

- [[test-strategy-and-coverage]] - test pyramid, smoke/regression, when to automate, coverage metrics
- [[test-data-management]] - Faker, factory fixtures, environment config, data isolation

## External References

- [pytest documentation](https://docs.pytest.org/en/stable/)
- [Playwright Python docs](https://playwright.dev/python/docs/intro)
- [Selenium Python docs](https://www.selenium.dev/documentation/webdriver/)
- [Allure Report](https://allurereport.org/docs/pytest/)
- [requests library](https://requests.readthedocs.io/)
- [httpx library](https://www.python-httpx.org/)
- [Pydantic v2 docs](https://docs.pydantic.dev/latest/)
- [Faker library](https://faker.readthedocs.io/)
- [GitHub Actions docs](https://docs.github.com/en/actions)

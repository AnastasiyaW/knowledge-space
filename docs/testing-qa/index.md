---
title: Testing & QA Knowledge Base
category: index
tags: [testing, qa, test-automation, pytest, playwright, selenium, api-testing]
---

# Testing & QA

Test automation engineering - frameworks, tools, patterns, and infrastructure for reliable automated testing.

## Frameworks and Tools

- [[pytest-fundamentals]] - fixtures, parametrize, xdist, markers, hooks, conftest plugins
- [[pytest-fixtures-advanced]] - scopes, factories, composition, conftest hierarchy, autouse, finalization
- [[selenium-webdriver]] - WebDriver protocol, locators (CSS/XPath/data-testid), waits, interactions
- [[playwright-testing]] - auto-wait, codegen, trace viewer, role-based locators
- [[selene-python]] - Selenide for Python, fluent API, auto-waiting, concise browser automation
- [[mobile-testing]] - Kaspresso (Android), screen objects, emulators in CI

## API and Protocol Testing

- [[api-testing-requests]] - REST (requests/httpx), response validation, session hooks
- [[grpc-testing]] - protobuf, client generation, interceptors, Allure integration, WireMock
- [[soap-testing]] - WSDL, XML parsing, zeep client, fault handling, WS-Security
- [[oauth-testing]] - OAuth 2.0 flows, PKCE, JWT validation, auto-refresh sessions

## Testing Patterns

- [[page-object-model]] - POM pattern, component objects, abstraction levels
- [[pydantic-test-models]] - response validation, strict mode, data generation, schema contracts
- [[test-data-management]] - env configs, parametrize, factories, cleanup strategies
- [[test-parallelization]] - pytest-xdist, distribution modes, worker isolation, scaling
- [[database-testing]] - SQL queries from tests, rollback isolation, cross-service verification
- [[test-logging-secrets]] - structured logging, secret masking, Allure sanitization

## Architecture and Strategy

- [[test-architecture]] - project structure, test pyramid, coverage, logging, security
- [[allure-reporting]] - annotations, steps, attachments, session hooks, report publishing

## Infrastructure

- [[ci-cd-test-automation]] - Jenkins, GitHub Actions, Selenoid, Docker Compose, scheduling
- [[docker-test-environments]] - compose stacks, testcontainers, wait strategies, CI services
- [[fastapi-test-services]] - TestClient, dependency overrides, async testing, mock services
- [[kafka-async-testing]] - producer/consumer tests, eventual consistency, DLQ validation

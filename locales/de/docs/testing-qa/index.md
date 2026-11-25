---
title: "Testing & QA Wissensdatenbank"
category: index
tags: [testing, qa, test-automation, pytest, playwright, selenium, api-testing]
level: 2
source_sha256: c4b04890ddd97526677968b2079e27191286a123f798b86f15c5d5ccf29319fc
translation: machine
translated_at: '2026-10-24'
---
# Testing & QA {#testing-qa}

Test-Automatisierung als Ingenieursdisziplin - Frameworks, Tools, Muster und Infrastruktur für zuverlässige automatisierte Tests.

## Frameworks und Tools {#frameworks-and-tools}

- [[pytest-fundamentals]] - Fixtures, Parametrisierung, xdist, Marker, Hooks, conftest-Plugins
- [[pytest-fixtures-advanced]] - Scopes, Factories, Komposition, conftest-Hierarchie, autouse, Finalisierung
- [[selenium-webdriver]] - WebDriver-Protokoll, Locators (CSS/XPath/data-testid), Waits, Interaktionen
- [[playwright-testing]] - Auto-Wait, Codegen, Trace Viewer, rollenbasierte Locators
- [[selene-python]] - Selenide für Python, Fluent API, automatisches Warten, präzise Browser-Automatisierung
- [[mobile-testing]] - Kaspresso (Android), Screen Objects, Emulatoren in CI

## API- und Protokolltests {#api-and-protocol-testing}

- [[api-testing-requests]] - REST (requests/httpx), Validierung von Antworten, Session-Hooks
- [[grpc-testing]] - Protobuf, Client-Generierung, Interceptors, Allure-Integration, WireMock
- [[soap-testing]] - WSDL, XML-Parsing, zeep-Client, Fehlerbehandlung (Faults), WS-Security
- [[oauth-testing]] - OAuth-2.0-Flows, PKCE, JWT-Validierung, Sessions mit automatischer Aktualisierung

## Testmuster {#testing-patterns}

- [[page-object-model]] - POM-Muster, Komponentenobjekte, Abstraktionsebenen
- [[pydantic-test-models]] - Validierung von Antworten, Strict Mode, Datengenerierung, Schema-Verträge
- [[test-data-management]] - Umgebungskonfigurationen, Parametrisierung, Factories, Cleanup-Strategien
- [[test-parallelization]] - pytest-xdist, Verteilungsmodi, Worker-Isolation, Skalierung
- [[database-testing]] - SQL-Abfragen aus Tests, Isolation per Rollback, serviceübergreifende Verifikation
- [[test-logging-secrets]] - strukturiertes Logging, Maskierung von Secrets, Bereinigung für Allure

## Architektur und Strategie {#architecture-and-strategy}

- [[test-architecture]] - Projektstruktur, Testpyramide, Coverage, Logging, Sicherheit
- [[allure-reporting]] - Annotationen, Steps, Anhänge, Session-Hooks, Veröffentlichung von Reports

## Infrastruktur {#infrastructure}

- [[ci-cd-test-automation]] - Jenkins, GitHub Actions, Selenoid, Docker Compose, Scheduling
- [[docker-test-environments]] - Compose-Stacks, Testcontainers, Wartestrategien, CI-Services
- [[fastapi-test-services]] - TestClient, Dependency Overrides, asynchrones Testen, Mock-Services
- [[kafka-async-testing]] - Producer-/Consumer-Tests, eventuelle Konsistenz, DLQ-Validierung

## Weiterführende Referenzen {#additional-references}

- [[browser-test-automation]] - Geb ist eine Groovy-Bibliothek auf Basis von Selenium WebDriver für die Browser-Test-Automatisierung
- [[negative-controls-for-verification]] - Ein grüner Check beweist nichts, solange nicht gezeigt wurde, dass er auch rot werden kann
- [[three-state-check-aggregation]] - PASS / FAIL / UNKNOWN statt Pass/Fail: Exit-Code-Verträge, Fail-Closed-Aggregation

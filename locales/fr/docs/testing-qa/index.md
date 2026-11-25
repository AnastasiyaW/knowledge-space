---
title: "Base de connaissances Tests et QA"
category: index
tags: [testing, qa, test-automation, pytest, playwright, selenium, api-testing]
level: 2
source_sha256: c4b04890ddd97526677968b2079e27191286a123f798b86f15c5d5ccf29319fc
translation: machine
translated_at: '2026-10-24'
---
# Tests et QA {#testing-qa}

Ingénierie de l'automatisation des tests - frameworks, outils, patterns et infrastructure pour des tests automatisés fiables.

## Frameworks et outils {#frameworks-and-tools}

- [[pytest-fundamentals]] - fixtures, parametrize, xdist, markers, hooks, plugins conftest
- [[pytest-fixtures-advanced]] - scopes, factories, composition, hiérarchie conftest, autouse, finalisation
- [[selenium-webdriver]] - protocole WebDriver, locators (CSS/XPath/data-testid), waits, interactions
- [[playwright-testing]] - auto-wait, codegen, trace viewer, locators basés sur les rôles
- [[selene-python]] - Selenide pour Python, API fluide, auto-waiting, automatisation de navigateur concise
- [[mobile-testing]] - Kaspresso (Android), screen objects, émulateurs en CI

## Tests d'API et de protocoles {#api-and-protocol-testing}

- [[api-testing-requests]] - REST (requests/httpx), validation des réponses, session hooks
- [[grpc-testing]] - protobuf, génération de clients, interceptors, intégration Allure, WireMock
- [[soap-testing]] - WSDL, parsing XML, client zeep, gestion des fautes, WS-Security
- [[oauth-testing]] - flux OAuth 2.0, PKCE, validation JWT, sessions à rafraîchissement automatique

## Patterns de test {#testing-patterns}

- [[page-object-model]] - pattern POM, component objects, niveaux d'abstraction
- [[pydantic-test-models]] - validation des réponses, mode strict, génération de données, contrats de schéma
- [[test-data-management]] - configurations d'environnement, parametrize, factories, stratégies de nettoyage
- [[test-parallelization]] - pytest-xdist, modes de distribution, isolation des workers, passage à l'échelle
- [[database-testing]] - requêtes SQL depuis les tests, isolation par rollback, vérification inter-services
- [[test-logging-secrets]] - journalisation structurée, masquage des secrets, sanitisation Allure

## Architecture et stratégie {#architecture-and-strategy}

- [[test-architecture]] - structure du projet, pyramide de tests, couverture, journalisation, sécurité
- [[allure-reporting]] - annotations, steps, pièces jointes, session hooks, publication de rapports

## Infrastructure {#infrastructure}

- [[ci-cd-test-automation]] - Jenkins, GitHub Actions, Selenoid, Docker Compose, planification
- [[docker-test-environments]] - stacks compose, testcontainers, stratégies d'attente, services CI
- [[fastapi-test-services]] - TestClient, surcharge de dépendances, tests asynchrones, services mock
- [[kafka-async-testing]] - tests producteur/consommateur, cohérence à terme, validation DLQ

## Références complémentaires {#additional-references}

- [[browser-test-automation]] - Geb est une bibliothèque Groovy au-dessus de Selenium WebDriver pour l'automatisation de tests de navigateur
- [[negative-controls-for-verification]] - Un voyant vert ne prouve rien tant qu'on n'a pas montré qu'il peut passer au rouge
- [[three-state-check-aggregation]] - PASS / FAIL / UNKNOWN au lieu de réussite-échec : contrats de code de sortie, agrégation fail-closed

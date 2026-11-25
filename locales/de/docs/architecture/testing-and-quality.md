---
title: "Teststrategie und Qualitätsmanagement"
category: reference
tags: [testing, testing-pyramid, contract-testing, chaos-engineering, quality]
level: 3
source_sha256: 9d2c3cc4c08699af932114d202aeb3451e463534341fbccc70e82592ac91eb5f
translation: machine
translated_at: '2026-10-24'
---
# Teststrategie und Qualitätsmanagement {#testing-strategy-and-quality-management}

Qualität und Entwicklungsgeschwindigkeit hängen über technische Schulden zusammen: schlechte Qualität = langsame Entwicklung. Eine gute Testinfrastruktur ermöglicht schnellere, sicherere Deployments.

## Testpyramide {#testing-pyramid}

```text
      /    E2E    \        <- Fewest, most expensive, slowest
     / Integration \       <- Middle layer
    /   Unit Tests  \      <- Most tests, cheapest, fastest
```

**Regel:** viele Unit-Tests, ~10x weniger Integrationstests, ~10x weniger E2E-Tests.

| Ebene | Was | Kosten | Geschwindigkeit |
|-------|-----|--------|-----------------|
| **Unit** | Einzelne Funktionen | Gering | Schnell |
| **Integration** | Zusammenspiel von Services | Mittel | Mittel |
| **E2E** | Vollständige Benutzerabläufe | Hoch | Langsam |

## Contract Testing {#contract-testing}

Stellt sicher, dass zwei Services korrekt miteinander interagieren können, indem geprüft wird, ob die API-Verträge übereinstimmen. Kritisch, wenn mehrere Teams unterschiedliche Services verantworten. Verhindert Breaking Changes, wenn ein Team seine API ändert.

**Ablauf:** Service A definiert erwartete Request/Response-Struktur -> Contract wird veröffentlicht -> Service B validiert gegen den Contract -> jede Abweichung wird vor dem Deployment gemeldet.

## Chaos Engineering {#chaos-engineering}

Fehler gezielt einspielen, um die Resilienz zu testen. Netflix Chaos Monkey beendet zufällig Produktionsservices.

**Wenn du nicht die Größenordnung von Netflix oder Google hast, brauchst du das nicht.** Relevant nur für große verteilte Systeme, die die Resilienz gegenüber zufälligen Ausfällen überprüfen.

**Arten:** Fault Injection (Fehler), Traffic Shaping (Simulation von Bedingungen).

## Testentwurfstechniken {#test-design-techniques}

Gezielte Auswahl von Testfällen, um mit möglichst wenigen Tests möglichst viel Funktionalität zu prüfen:
- Äquivalenzklassenbildung (ein Wert pro Eingabeklasse)
- Grenzwertanalyse (Ränder gültiger Bereiche)
- Entscheidungstabellen (Kombinationen von Bedingungen)
- Zustandsübergangstests (gültige/ungültige Zustandswechsel)

## Auswirkungsanalyse {#impact-analysis}

Bei Änderungen teilen Entwickler den Testern mit, welche Bereiche betroffen sind. Teamübergreifende Zusammenarbeit ist essenziell, da Tester den Wirkungsradius verstehen müssen.

## Zusammenhang zwischen Qualität und Deployment {#quality-deployment-connection}

Contract Testing + eine saubere Migrationsstrategie + Quality Gates = Sicherheit, um häufig zu deployen.

Der weniger offensichtliche Punkt: Eine gute Testinfrastruktur **ermöglicht** schnellere, sicherere Deployments, sie fängt nicht nur Fehler ab.

## Stolperfallen {#gotchas}

- **Umgekehrte Testpyramide** (viele E2E-Tests, wenige Unit-Tests) = langsame, fragile, teure CI
- **E2E-Tests für jedes Feature** – nur kritische Benutzerreisen verdienen E2E-Tests. Für Service-Grenzen Contract Tests verwenden
- **Chaos-Tests ohne Monitoring** – Fehler einzuspielen, ohne die Ergebnisse zu beobachten, ist nur das Kaputtmachen von Dingen
- **100 % Code Coverage** bedeutet nicht Qualität – man kann volle Abdeckung haben und dennoch kritische Grenzfälle übersehen

## Siehe auch {#see-also}

- [[devops-cicd]] - CI/CD-Pipeline-Stufen, Deployment-Strategien
- [[microservices-communication]] - Circuit Breaker als Laufzeit-Qualitätsmuster
- [[quality-attributes-reliability]] - SLA, Verfügbarkeitstests

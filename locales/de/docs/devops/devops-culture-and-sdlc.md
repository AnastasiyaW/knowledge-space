---
title: "DevOps-Kultur und SDLC"
category: concepts
tags: [devops, culture, sdlc, agile, automation, collaboration]
level: 2
source_sha256: c0c98a89f04ae9386f2fcc550b6872422eb352a0b2b9406a72fd1b5dd47ed332
translation: machine
translated_at: '2026-10-24'
---
# DevOps-Kultur und SDLC {#devops-culture-and-sdlc}

DevOps ist eine Sammlung von Praktiken, Werkzeugen und kulturellen Philosophien, die Prozesse zwischen Softwareentwicklung und IT-Betrieb automatisieren und miteinander verzahnen. Im Mittelpunkt stehen Zusammenarbeit, gemeinsame Verantwortung und kontinuierliche Verbesserung.

## Das traditionelle Problem {#the-traditional-problem}

- Dev-Teams: fokussieren auf Funktionen und Geschwindigkeit, „Code über die Mauer werfen“
- Ops-Teams: fokussieren auf Stabilität, widersetzen sich Änderungen, manuelle Deployments
- Ergebnis: Reibung, Verzögerungen, gegenseitige Schuldzuweisungen, langsamere Time-to-Market

## DevOps-Prinzipien {#devops-principles}

1. **Zusammenarbeit** - gemeinsame Ziele zwischen Dev und Ops
2. **Automatisierung** - CI/CD-Pipelines, IaC, automatisierte Tests
3. **Kontinuierliche Verbesserung** - Feedback-Schleifen, iterative Verfeinerung
4. **Kundenfokus** - schnelle Auslieferung von Mehrwert, rasche Reaktion

## SDLC (Software Development Life Cycle) {#sdlc-software-development-life-cycle}

```php
Plan -> Code -> Build -> Test -> Release -> Deploy -> Operate -> Monitor -> (back to Plan)
```

DevOps automatisiert die Phasen von Build bis Deploy, überwacht den Betrieb (Operate) und speist die Erkenntnisse zurück in die Planung.

## Tool-Landschaft {#tools-landscape}

| Kategorie | Tools |
|----------|-------|
| Quellcodeverwaltung | Git, GitHub, GitLab, Bitbucket |
| CI/CD | Jenkins, GitLab CI, GitHub Actions, Azure DevOps |
| Containerisierung | Docker, containerd |
| Orchestrierung | Kubernetes, Docker Swarm |
| IaC | Terraform, Ansible, CloudFormation, Pulumi |
| Monitoring | Prometheus, Grafana, ELK, Datadog |
| Cloud | AWS, Azure, GCP |
| Artefakt-Repository | Nexus, JFrog Artifactory, Docker Hub |

## Agile und Scrum {#agile-and-scrum}

- **Sprints** - 2-wöchige Iterationen
- **Rollen** - Product Owner, Scrum Master, Dev-Team
- **Zeremonien** - Sprint Planning, Daily Standup, Review, Retrospective
- **Board** - To Do -> In Progress -> In Review -> Done

## Deployment-Stufen {#deployment-stages}

| Stufe | Zweck | Zugriff |
|-------|---------|--------|
| Development | Lokales Programmieren und Testen | Entwickler |
| Testing/QA | Integrationstests | QA-Team |
| Staging | Validierung vor der Produktion | Intern |
| Production | Live-Nutzerverkehr | Öffentlich |

## Semantic Versioning {#semantic-versioning}

Format: `MAJOR.MINOR.PATCH` (z. B. 2.1.3)
- MAJOR: inkompatible Änderungen
- MINOR: neue Funktionen, abwärtskompatibel
- PATCH: Fehlerbehebungen

## Sicherheitsgrundlagen {#security-fundamentals}

- SSH-Schlüssel statt Passwörter
- Firewall-Regeln (Least Privilege)
- Geheimnisse in Umgebungsvariablen, nicht im Code
- HTTPS/TLS für externe Kommunikation
- Software aktuell halten

## Siehe auch {#see-also}

- [[sre-principles]] - Zuverlässigkeitstechnik als Erweiterung von DevOps
- [[cicd-pipelines]] - Automatisierung der Pipeline
- [[git-version-control]] - Grundlage der Quellcodeverwaltung
- [[monitoring-and-observability]] - Feedback-Schleife

---
title: "DevOps und CI/CD"
category: reference
tags: [devops, cicd, docker, kubernetes, iac, deployment, monitoring]
level: 3
source_sha256: 2e0938b6eb8f14c1494a80775a7ed93ac048416452a0117640af96f8de4ff8f5
translation: machine
translated_at: '2026-10-24'
---
# DevOps und CI/CD {#devops-and-cicd}

DevOps verbindet Entwicklung und Betrieb durch Kultur, Automatisierung und kontinuierliche Prozessverbesserung. Es ist kein Werkzeug, sondern eine Methodik, die kulturelle, organisatorische und technische Praktiken kombiniert.

## CI/CD-Pipeline {#cicd-pipeline}

```bash
Source (commit) -> Build (compile) -> Test (unit, integration, e2e) ->
  Security scan -> Artifact creation -> Deploy staging -> Acceptance tests ->
  Deploy production -> Smoke tests
```

| Praxis | Beschreibung |
|--------|--------------|
| **CI** | Häufige Merges (täglich oder öfter), automatisierter Build und Test, frühzeitige Fehlererkennung |
| **Continuous Delivery** | Automatisch auf Release vorbereitet, manuelle Freigabe für das Deployment |
| **Continuous Deployment** | Automatisches Deployment bei bestandenen Tests, kein manuelles Gate |

## Infrastructure as Code (IaC) {#infrastructure-as-code-iac}

Infrastruktur über versionierte Konfigurationsdateien verwalten.

| Werkzeug | Ansatz | Geeignet für |
|----------|--------|--------------|
| **Terraform** | Deklarativ, cloud-agnostisch | Multi-Cloud-Provisionierung |
| **CloudFormation** | Deklarativ, AWS-spezifisch | Reine AWS-Umgebungen |
| **Pulumi** | Universelle Programmiersprachen | Entwickler, die Code bevorzugen |
| **Ansible** | Konfigurationsmanagement | Serverkonfiguration, Orchestrierung |

**Immutable Infrastructure:** Neue Instanzen mit aktualisierter Konfiguration erstellen und die alten ersetzen. Verhindert Konfigurationsdrift. Funktioniert mit Containern und Blue-Green-Deployments.

## Containerisierung {#containerization}

**Docker:** Anwendung und Abhängigkeiten in portable Container verpacken.
- Das Dockerfile definiert die Build-Schritte
- docker-compose für Anwendungen aus mehreren Containern
- Best Practices: kleine Basis-Images (Alpine, distroless), Multi-Stage-Builds, Nicht-Root-Benutzer, Health Checks, Ressourcenlimits

**Kubernetes (K8s):** Orchestrierung von Containern.
- Zentrale Konzepte: Pods, Deployments, Services, Ingress, ConfigMaps, Secrets, Namespaces
- Automatisches Deployment, Skalierung und Verwaltung containerisierter Anwendungen

## Deployment-Strategien {#deployment-strategies}

| Strategie | Mechanismus | Rollback | Risiko |
|-----------|-------------|----------|--------|
| **Blue-Green** | Zwei identische Umgebungen, Traffic umschalten | Sofort (zurückschalten) | Doppelte Infrastrukturkosten |
| **Canary** | Schrittweiser Rollout, zunächst an eine kleine Teilmenge | Canary entfernen | Gering, kleiner Wirkungsbereich |
| **Rolling** | Instanzen schrittweise ersetzen | Rollback läuft | Kurzzeitig gemischte Versionen |
| **Feature Flags** | Deployment mit Features hinter Schaltern | Schalter deaktivieren | Code-Komplexität |

## Zero-Downtime-Datenbankmigrationen {#zero-downtime-database-migrations}

**Expand-Contract-Muster:**
1. **Expand** - neue Spalte bzw. neue Tabelle neben der alten hinzufügen. Beide funktionieren
2. **Daten migrieren** - Daten von alt nach neu kopieren bzw. transformieren
3. **Umschalten** - Anwendung auf die neue Struktur umstellen
4. **Contract** - alte Struktur nach einer Verifikationsphase entfernen

**Migrationsprinzipien:**
- Nur vorwärts (bestehende Skripte nie verändern)
- Versionskontrolliert (Git)
- Idempotent (mehrfaches Ausführen ist sicher)
- Rollback-Plan für jede Migration

## Monitoring und Observability {#monitoring-and-observability}

### Drei Säulen {#three-pillars}

| Säule | Was | Werkzeuge |
|-------|-----|-----------|
| **Metriken** | Zahlenwerte über die Zeit (Latenz, Durchsatz, Fehler) | Prometheus + Grafana |
| **Logs** | Ereignisprotokolle | ELK Stack, Loki |
| **Traces** | Anfragefluss über Services hinweg | Jaeger, Zipkin |

**Alles-in-einem:** Datadog, New Relic.

### Zentrale Metriken {#key-metrics}
- Latenz: p50, p95, p99
- Durchsatz: Anfragen pro Sekunde
- Fehlerrate
- Sättigung: Ressourcenauslastung
- SLI/SLO/SLA

**Alerting:** Auf Symptome (Auswirkung auf Nutzer) alarmieren, nicht auf Ursachen. Alert-Fatigue reduzieren. Runbooks für jeden Alert. PagerDuty und OpsGenie für das Incident-Management.

## 12-Factor-App-Methodik {#12-factor-app-methodology}

1. **Codebasis** - ein Repository pro Anwendung
2. **Abhängigkeiten** - explizit deklarieren
3. **Konfiguration** - in Umgebungsvariablen
4. **Unterstützende Dienste** - als angebundene Ressourcen behandeln
5. **Build, Release, Run** - strikt trennen
6. **Prozesse** - zustandslos, nichts teilen
7. **Port-Bindung** - selbstständig
8. **Nebenläufigkeit** - über Prozesse skalieren
9. **Einweggebrauch** - schneller Start, sauberes Herunterfahren
10. **Dev/Prod-Parität** - Umgebungen ähnlich halten
11. **Logs** - als Ereignisströme behandeln
12. **Administration** - einmalige Prozesse

## Design für den Betrieb {#design-for-operations}

- Health-Endpunkte, sauberes Herunterfahren (Graceful Shutdown)
- Strukturiertes Logging, Correlation IDs über Services hinweg
- Auslagerung der Konfiguration
- Abwärtskompatible DB-Migrationen
- API-Versionierung, Feature Flags
- Geschäftsmetriken neben technischen Metriken

## Stolperfallen {#gotchas}

- **CI ohne Tests** ist nur "kontinuierliches Bauen" - automatisierte Tests sind der eigentliche Zweck
- **Blue-Green mit Datenbanken** - beide Versionen müssen während der Übergangsphase mit demselben DB-Schema funktionieren
- **Aufräumen von Feature Flags** - veraltete Flags sammeln sich an. Entfernung nach dem Rollout einplanen
- **Monitoring ohne Alerting** - Dashboards, die niemand beobachtet, sind wertlos
- **DevSecOps** - Sicherheit in jeder Phase integrieren, nicht erst nachträglich

## Siehe auch {#see-also}

- [[quality-attributes-reliability]] - Verfügbarkeit, Fehlertoleranz, Auto-Scaling
- [[security-architecture]] - DevSecOps-Integration
- [[microservices-communication]] - Architekturmuster für Services
- [[database-selection]] - ORM, Migrationen, Zero-Downtime-Muster

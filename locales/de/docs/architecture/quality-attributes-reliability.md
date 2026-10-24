---
title: "Qualitätsmerkmale – Zuverlässigkeit und Fehlertoleranz"
category: concepts
tags: [reliability, availability, fault-tolerance, sla, chaos-engineering, recovery]
level: 4
source_sha256: e28fcb10ed3daf8a63278600bec02ec1f3203d96f005096220afddd6a9f3461f
translation: machine
translated_at: '2026-10-24'
---
# Qualitätsmerkmale – Zuverlässigkeit und Fehlertoleranz {#quality-attributes-reliability-and-fault-tolerance}

Zuverlässigkeit = System arbeitet unter festgelegten Bedingungen über die Zeit korrekt, einschließlich der Wiederherstellung nach Ausfällen. Drei Säulen: Verfügbarkeit, Fehlertoleranz, Wiederherstellbarkeit.

## Verfügbarkeit {#availability}

Prozentsatz der Zeit, in der das System erreichbar ist. Uptime / Gesamtbeobachtungszeit.

| SLA | Ausfallzeit/Jahr | Klassifizierung |
|-----|--------------|----------------|
| 99,999 % | ~5 min | Five Nines (ideal) |
| 99,99 % | ~52 min | Four Nines |
| 99,9 % | ~8,76 Stunden | Standard |
| 99 % | ~3,65 Tage | Basis |
| 95 % | ~18,25 Tage | Schlecht |

### Werkzeuge für Verfügbarkeit {#availability-tools}

| Werkzeug | Zweck |
|------|---------|
| **Auto-Scaling** | Instanzen dynamisch anhand von Metriken hinzufügen/entfernen |
| **Load Balancer** | Datenverkehr auf Instanzen verteilen |
| **CDN** | Geografische Verteilung für statische Inhalte |
| **Caching** | Backend-Last reduzieren |
| **Rate Limiting** | Überlastung verhindern |
| **Service Discovery** | Dienste automatisch erkennen (Consul, etcd, ZooKeeper) |
| **Health Checks** | Aktive Probes oder passive Heartbeats |
| **Connection Pooling** | Vorab aufgebaute Verbindungen wiederverwenden |
| **Hot Standby** | Backup läuft synchron mit, sofortiges Failover |
| **Cold Standby** | Backup ist aus, benötigt Startzeit |

## Fehlertoleranz {#fault-tolerance}

Das System arbeitet während partieller Ausfälle weiter.

### Kennzahlen {#key-metrics}

| Metrik | Misst | Ideal | Normal | Schlecht |
|--------|----------|-------|--------|------|
| **MTTF** | Zeit zwischen Ausfällen | 2 Jahre | 6 Monate | 1 Woche |
| **MTTR** | Zeit bis zur Wiederherstellung | 5 min | 30 min | 3 Tage |

### Muster für Fehlertoleranz {#fault-tolerance-patterns}

**Failover:**
- **Active-Passive** – eine Instanz aktiv, Standby wartet
- **Active-Active** – alle Instanzen verarbeiten gleichzeitig Datenverkehr

**Bulkhead:** Ressourcen isolieren, damit ein Ausfall nicht kaskadiert. Isolation auf Thread- oder Prozessebene.

**Timeouts + Retries:** Exponentielles Backoff mit Jitter, um Thundering Herd zu verhindern.

**Graceful Degradation:** Nicht kritische Funktionen deaktivieren. Fällt der Empfehlungsdienst aus, funktionieren Käufe weiterhin.

**Chaos Engineering:** Fehler gezielt einspielen. Netflix Chaos Monkey beendet zufällig Produktionsdienste, um die Selbstheilung zu überprüfen.

### Organisatorische Praktiken {#organizational-practices}
- **Wiederherstellungspläne** – vorbereitete Szenarien, regelmäßig getestet
- **Post-Mortem-Analyse** – Zeitablauf, Ursache, ergriffene Maßnahmen, Wirksamkeit der Kommunikation

## Wiederherstellbarkeit {#recoverability}

Fähigkeit, nach einem Ausfall in den betriebsbereiten Zustand zurückzukehren.

### Kennzahlen {#key-metrics_1}

| Metrik | Misst | Ideal | Normal | Schlecht |
|--------|----------|-------|--------|------|
| **RTO** | Maximal akzeptable Ausfallzeit | 5 min | 1 Stunde | 3 Tage |
| **RPO** | Maximal akzeptabler Datenverlust | 1 min | 15 min | 1 Tag |

### Werkzeuge für die Wiederherstellung {#recovery-tools}

- **Automatisierte Wiederherstellung** – Skripte + Orchestrierung (Kubernetes startet automatisch neu)
- **Rollback** – schnelle Rückkehr zur vorherigen stabilen Version
- **Datenbank-Rollback** – Mechanismen zum Zurücksetzen von Transaktionen
- **Konfigurationsmanagement** – Ansible für die Versionierung der Konfiguration

**Grundprinzip:** Vorbereitung ist alles. Skripte und Szenarien für eine schnelle Wiederherstellung im Voraus erstellen.

## Problem-zu-Werkzeug-Zuordnung {#problem-to-tool-mapping}

| Problem | Lösung |
|---------|----------|
| Server stürzt ab, manueller Neustart nötig | Health Checks + automatischer Neustart |
| Verkehrsspitzen führen zu Leistungseinbußen | Auto-Scaling |
| Microservice ausgefallen, kein Standby auffindbar | Service Discovery |
| Alle Anfragen treffen einen einzelnen Server | Load Balancer |
| Hohe Latenz für entfernte Nutzer | CDN + geografische Verteilung |
| Datenbank durch Abfragen überlastet | Caching |
| Einzelner Client überflutet die API | Rate Limiting |
| Ausfall eines einzelnen Servers = Totalausfall | Hot/Cold Standby |

## Rolle des Architekten {#architects-role}

Der Wert des Architekten liegt im tiefen Verständnis der Problemdomäne und der Geschäftsanforderungen, nicht im Kennen jedes technischen Details. Zentrale Frage: „Was und warum“ – Implementierungsdetails werden an die Entwicklungsteams delegiert.

Technische Entscheidungen sind mit der Organisationskultur, der Geschäftsstrategie und regulatorischen Anforderungen verflochten. Alle Zuverlässigkeitskennzahlen variieren je nach Anwendungsfall, Kritikalität des Systems und Geschäftsanforderungen.

## Stolperfallen {#gotchas}

- **Five Nines kosten exponentiell mehr** als Three Nines – jede weitere Neun kostet etwa das Zehnfache
- **MTTR ist in der Praxis wichtiger als MTTF** – Ausfälle sind unvermeidbar, schnelle Wiederherstellung ist das Ziel
- **Hot Standby ohne Test** – ein Standby, der nie getestet wurde, funktioniert im Bedarfsfall möglicherweise nicht. Failover regelmäßig testen
- **Chaos Engineering ohne Monitoring** – Fehler einzuspielen, ohne die Ergebnisse zu beobachten, ist nur das Kaputtmachen von Systemen
- **SLA != SLO != SLI** – SLI misst, SLO definiert das Ziel, SLA ist der Vertrag mit Konsequenzen

## Siehe auch {#see-also}

- [[distributed-systems-fundamentals]] – CAP-Theorem, Konsens, Replikation
- [[microservices-communication]] – Circuit Breaker, Bulkhead-Muster
- [[devops-cicd]] – Deployment-Strategien, Monitoring, Observability
- [[security-architecture]] – Sicherheit als Teil der Zuverlässigkeit

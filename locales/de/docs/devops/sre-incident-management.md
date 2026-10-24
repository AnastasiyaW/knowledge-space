---
title: "SRE-Incident-Management"
category: concepts
tags: [devops, sre, on-call, postmortems, incident-response, escalation]
level: 3
source_sha256: 0cceaf0ca9634eadf53daebe4ad0360824750df6c6e35200bfbd6b1cdc9a4eeb
translation: machine
translated_at: '2026-10-24'
---
# SRE-Incident-Management {#sre-incident-management}

Incident Management umfasst die On-Call-Struktur, Eskalation, Schadensbegrenzung und schuldfreie Postmortems. Ziel ist es, die MTTR zu minimieren und gleichzeitig nachhaltige On-Call-Praktiken aufrechtzuerhalten.

## On-Call-Struktur {#on-call-structure}

- Primary- und Secondary-Rotation
- Dauer: typischerweise 1-2 Wochen
- Maximum: 2 Incidents pro 12-Stunden-Schicht (nachhaltiges Tempo)
- Follow-the-Sun für globale Teams
- Tools: PagerDuty, Opsgenie, VictorOps

## On-Call-Verantwortlichkeiten {#on-call-responsibilities}

1. **Acknowledge** - Alarm innerhalb der SLA bestätigen (z. B. 5 Min. für P1)
2. **Triage** - Schweregrad bewerten, Eskalationsbedarf festlegen
3. **Mitigate** - Nutzerauswirkungen reduzieren (noch nicht die Ursache beheben)
4. **Communicate** - Status Page aktualisieren, Stakeholder benachrichtigen
5. **Resolve** - vollständige Behebung
6. **Handoff** - für die nächste Schicht dokumentieren, Postmortem anlegen

## Wesentliches On-Call-Wissen {#essential-on-call-knowledge}

1. **Reading traces** - wie man verteilte Systeme debuggt
2. **Fallback switching** - bestehende Fallback-Mechanismen, manuelle Prozeduren
3. **Deploy rollback** - Zurücksetzen fehlerhafter Deployments und Konfigurationen
4. **Rate limiting** - Umgang mit böswilligen DoS-Angriffen und versehentlicher Selbst-DoS
5. **Impact limitation** - Eindämmung der Auswirkungen defekter Teile auf das Gesamtsystem

**Kernprinzip**: Die primäre Ursache aller Probleme ist, dass jemand etwas falsch konfiguriert hat. Deployment- und Konfigurations-Rollbacks müssen dokumentiert und geübt sein.

## Eskalation {#escalation}

| Schweregrad | Reaktionszeit | Aktion |
|----------|---------------|--------|
| P1 (Service ausgefallen) | Sofort alarmieren | War Room innerhalb von 15 Min. |
| P2 (beeinträchtigt) | Alarmieren, 30 Min. | Fokussierte Untersuchung |
| P3 (geringe Auswirkung) | Ticket | Nächster Werktag |

Im Zweifel eskalieren.

## Zentrale Incident-Rollen {#key-incident-roles}

### IMOC (Incident Manager On-Call) {#imoc-incident-manager-on-call}

- Leitet und koordiniert die Behebung von SEVs
- Fokussiert auf TTR (Time to Recovery), Ziel: SEV-0 in 15 Min.
- Einzige Verantwortungsinstanz
- Hält das Team ruhig, steuert die Kommunikation mit der Führungsebene
- Ingenieure konzentrieren sich auf die technische Arbeit und berichten ihren Status an den IMOC

### TLOC (Technical Lead On-Call) {#tloc-technical-lead-on-call}

- Technischer Experte für Diagnose und Schadensbegrenzung
- Berichtet den Status an den IMOC
- Nach einem SEV: arbeitet an der Ursache und leitet Chaos-Experimente

## Postmortems {#postmortems}

### Grundsätze {#principles}

1. **Schuldfrei** - „Was am System hat den Fehler ermöglicht?"
2. **Schriftliches Dokument** - dauerhafter, gemeinsamer Nachweis
3. **Maßnahmen mit Verantwortlichen** - zugewiesen, nachverfolgt, priorisiert
4. **Breit geteilt** - organisationsweites Lernen

### Vorlage {#template}

```markdown
## Incident: [Title]
**Date**: YYYY-MM-DD | **Severity**: P1 | **Duration**: 2h 15m

## Summary
2-3 sentences of what happened.

## Impact
- Users affected: X
- Revenue impact: $Y
- SLO burn: Z%

## Timeline
- HH:MM - Alert fired
- HH:MM - On-call acknowledged
- HH:MM - Root cause identified
- HH:MM - Mitigation applied
- HH:MM - Full resolution

## Root Cause Analysis (5 Whys)
1. Why did the service fail? -> OOM kill
2. Why was memory exhausted? -> Memory leak in handler
...

## What Went Well
- Detection was fast (< 2 min)
- Runbook was accurate

## What Went Wrong
- Monitoring gap: no alert on memory trend
- Rollback took 20 min (should be < 5)

## Action Items
| Action | Owner | Priority | Deadline | Status |
|--------|-------|----------|----------|--------|
| Add memory trend alert | @eng | P1 | 2026-04-10 | TODO |
| Automate rollback | @sre | P2 | 2026-04-17 | TODO |

## Lessons Learned
```

### Auslöser {#trigger-criteria}

Ein Postmortem schreiben, wenn: sichtbare Auswirkungen für Nutzer, Error Budget verbraucht, Datenverlust, manueller Eingriff erforderlich, Monitoring-Lücke entdeckt, On-Call-Eskalation.

## Diagnosemethodik {#diagnostics-methodology}

1. **Observe** - Welche Symptome? Seit wann? Was hat sich geändert?
2. **Hypothesize** - mögliche Ursachen auf Basis der Symptome
3. **Test** - mit Daten bestätigen oder ausschließen
4. **Fix** - Behebung anwenden
5. **Prevent** - Monitoring, Tests und Automatisierung ergänzen

### Gängige Debugging-Dimensionen {#common-debugging-dimensions}

- **Zeitliche Korrelation**: Deployment? Konfigurationsänderung? Traffic-Muster?
- **Umfang**: ein Host? Eine AZ? Ein Service? Alle Nutzer oder nur einige?
- **Abhängigkeitsgraph**: vor- oder nachgelagerte Services?
- **Ressourcenerschöpfung**: CPU, Speicher, Festplatte, File Descriptors, Verbindungen?

### Tool-Hierarchie {#tools-hierarchy}

Dashboards (Grafana) -> Logs (Loki/ELK) -> Traces (Jaeger/Tempo) -> Profiling (pprof) -> Core Dumps. Breit beginnen, dann eingrenzen.

## Wissensaustausch {#knowledge-sharing}

- Diagnoseprozeduren dokumentieren
- On-Call-Shadowing zu Schulungszwecken
- Wheel of Misfortune (simulierte Incidents)
- Game Days (geplante Zuverlässigkeitsübungen)

## Fallstricke {#gotchas}

- Ein Postmortem ohne Nachverfolgung der Maßnahmen ist wertlos
- Die Rekonstruktion der Zeitleiste ist entscheidend – genau, wann welches Ereignis eintrat
- Runbooks müssen nach jedem Incident aktualisiert werden
- „Nur eine Person weiß, wie man umschaltet" ist ein kritisches Risiko – dokumentieren und gegenseitig schulen
- Der Incident-Koordinator kommuniziert den Status und debuggt NICHT

## Siehe auch {#see-also}

- [[sre-principles]] - SRE-Kultur und Error Budgets
- [[monitoring-and-observability]] - Alarmierung und SLI/SLO
- [[chaos-engineering-and-testing]] - proaktive Zuverlässigkeitstests
- [[deployment-strategies]] - Rollback-Strategien

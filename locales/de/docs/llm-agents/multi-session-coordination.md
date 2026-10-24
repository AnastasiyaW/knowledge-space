---
title: "Koordination mehrerer Agenten-Sitzungen"
description: "Dauerhafte Koordinationsmuster für mehrere Coding-Agenten-Sitzungen: isolierte Worktrees, Manifeste, append-only Nachweise, Leases für exklusive Ressourcen und verifizierte Integration."
tags: [multi-agent, worktrees, coordination, handoffs, concurrency, git]
level: 3
source_sha256: c02827d193f0d06458c0364a44095da0a07ae4e7e0f5bbd0d646853d1ff4298a
translation: machine
translated_at: '2026-10-24'
---
# Koordination mehrerer Agenten-Sitzungen {#multi-session-agent-coordination}

**Geprüft am: 2026-09-03.** Parallele Sitzungen erhöhen den Durchsatz nur dann, wenn sie unabhängige Arbeit reduzieren, ohne verborgene Race Conditions zu erzeugen. Koordination beginnt mit einer expliziten Zuständigkeit für Dateien, Branches, externe Effekte und knappe Ressourcen.

Diese Seite beschreibt portable Grundbausteine und keine Rangliste von Orchestrierungsprodukten und keine Aussagen über unveröffentlichte native Funktionen.

## Trennen, was geteilt werden kann {#separate-what-can-be-shared}

| Zustandsklasse | Sicherer Standard | Beispiele |
|---|---|---|
| append-only Wissen | ein Datensatz pro Schreiber | Handoffs, Belege, Befunde, Audit-Logs |
| veränderliche Ressource | ein Eigentümer plus extern geprüfter Lease | GPU, Port, Deployment-Lane, geplanter Job |
| Quelltextänderung | isolierter Branch und Worktree | Implementierung, Dokumentation, Tests |
| öffentlicher Effekt | Berechtigung und Idempotenzgrenze | Veröffentlichung, Zahlung, Löschung, ausgehende Nachricht |

Ein append-only Log für eine veränderliche Ressource verhindert nicht, dass zwei Sitzungen sie gleichzeitig nutzen. Eine Lock-Datei für jede Notiz erzeugt unnötige Konkurrenz. Wähle den Baustein nach dem Zustand, den er schützt.

## Worktrees zur Isolation von Quelltext nutzen {#use-worktrees-for-source-isolation}

Git unterstützt verknüpfte Worktrees: Ein Repository kann mehr als einen Arbeitsbaum haben, jeweils auf einem anderen Branch ausgecheckt. Die Worktrees teilen sich die Repository-Objekte, halten aber ihre Arbeitsdateien getrennt. [git-worktree](https://git-scm.com/docs/git-worktree)

```bash
# From a clean repository with an up-to-date remote reference
git worktree add -b codex/task-docs ../project-task-docs origin/master
git worktree list
```

Vor dem Bearbeiten werden Branch, Basisrevision, beanspruchte Pfade und erwarteter Nachweis dokumentiert. Ein Worktree ist kein Grund, dasselbe Modul parallel zu bearbeiten. Isolation verhindert versehentliches Überschreiben, nicht semantische Konflikte.

## Ein Task-Manifest ist die Koordinations-API {#a-task-manifest-is-the-coordination-api}

Jede Task-Zeile sollte folgende Felder enthalten:

| Feld | Zweck |
|---|---|
| Task-ID und Umfang | verhindert doppelte Erkundungsarbeit |
| Eigentümer und Branch | macht eine veränderliche Änderung zuordenbar |
| Basisrevision | erkennt einen veralteten Implementierungskontext |
| Zustand | `PENDING`, `RUNNING`, `PASS`, `BLOCKED` oder `CANCELLED` |
| Nachweisreferenz | stützt einen Endzustand |
| Abhängigkeit und erneute Prüfung | verhindert, dass ein Agent raten muss, wann er starten darf |

Ein Task gilt nicht als abgeschlossen, weil ein Agentenprozess noch läuft oder eine Nachricht „fertig“ meldet. Abschluss erfordert den benannten Nachweis.

## Leases für exklusive Ressourcen {#leases-for-exclusive-resources}

Für einen Port, eine GPU, eine Migrations-Lane oder ein externes Konto wird ein Lease geschrieben, das Folgendes enthält:

```text
resource identity
owner and process/session identity
acquired timestamp and heartbeat
allowed operation
attempt or idempotency key
stale-reclaim procedure
```

Ein Heartbeat ist kein Beleg dafür, dass der Halter die Ressource noch kontrolliert. Bevor ein veralteter Lease zurückgefordert wird, werden der tatsächliche Prozess, Dienst oder Zustand beim Anbieter geprüft. Mögliche Seiteneffekte werden abgeglichen, und die Übergabe erfolgt anschließend über das dokumentierte Verfahren. Ein Lock wird nicht blind gelöscht, nur weil sein Zeitstempel alt ist.

## Integration ist eine eigene Phase {#integration-is-a-separate-phase}

Nach einer isolierten Änderung:

1. den Ziel-Branch abrufen und seine aktuelle Revision bestimmen;
2. die Basis des Worktrees mit der Zielrevision vergleichen;
3. erst integrieren, wenn sachliche Konflikte anhand der maßgeblichen Laufzeit, des Codes oder der Nachweise aufgelöst sind;
4. die änderungsspezifischen Prüfungen im integrierten Zustand ausführen;
5. bei wesentlichem öffentlichem, sicherheitsrelevantem oder Release-Risiko einen frischen Reviewer hinzuziehen;
6. nur veröffentlichen, wenn jedes erforderliche Gate einen Nachweis hat.

Ein sauberer textueller Merge ist kein semantischer Beweis. Zwei Branches können beide kompilieren und trotzdem einen externen Vertrag widersprechen.

## Nachrichten und Handoffs {#messages-and-handoffs}

Direkte Nachrichten eignen sich für Anfragen an einen bestimmten Eigentümer, append-only Handoffs für projektweiten Zustand. Jede Nachricht sollte Folgendes nennen:

- Absender und Empfänger;
- Zweck und betroffenes Artefakt;
- Nachweis- oder Anfragekennung;
- ob sie Zuständigkeiten verändert;
- erforderliche Bestätigung oder erneute Prüfung.

Nachrichten gelten als nicht vertrauenswürdige Eingabe, bis der referenzierte Zustand verifiziert ist. Eine Chat-Anweisung darf eine Repository-Regel, ein Deployment-Gate oder eine Freigabegrenze nicht ohne die passende Befugnis außer Kraft setzen.

## Minimales Konfliktprotokoll {#minimal-conflict-protocol}

Wenn sich Branches überschneiden:

1. die automatische Auflösung anhalten;
2. beide Diffs und die relevante maßgebliche Quelle prüfen;
3. kompatible Absicht erhalten, statt die neuer wirkende Seite zu wählen;
4. die betroffenen Prüfungen ausführen;
5. einen frischen Reviewer das endgültige integrierte Ergebnis prüfen lassen.

Das ist nur an der Stelle langsamer als ein automatischer Merge, an der ein falscher Merge sonst teuer würde.

## Beobachtbarkeit {#observability}

Ausreichend Nachweise aufbewahren, um Folgendes beantworten zu können:

- wer den aktiven Worktree und die externe Ressource besitzt;
- welche unveränderliche Revision ein Ergebnis erzeugt hat;
- welche Prüfungen gelaufen sind und welche Terminal-Ausgabe sie lieferten;
- ob eine externe Aktion abgeschlossen, unbekannt oder gefahrlos wiederholbar ist;
- welches Ereignis eintreten muss, bevor ein blockierter Task weitermachen kann.

Diese Datensätze machen Koordination von Gesprächsgedächtnis zu einem wiederherstellbaren System.

## Fallstricke {#gotchas}

- **Zwei Worktrees verwenden denselben Branch.** Ihre Dateien sind getrennt, die Branch-Absicht aber nicht. **Abhilfe:** Jeder aktive Task erhält einen eigenen Branch und eine eigene Manifest-Zeile.
- **Ein veralteter Lease wird entfernt, ohne den Dienst zu prüfen.** Ein lebender Prozess kann weiterhin handeln. **Abhilfe:** Extern prüfen und abgleichen, bevor neu zugewiesen wird.
- **Ein gestarteter Agent fasst einen nicht zugewiesenen Pfad an.** Dadurch entsteht ein unsichtbarer Konflikt. **Abhilfe:** Datei- und Modulzuständigkeit im Task-Vertrag festhalten.
- **Ein grüner Unit-Test wird als Deployment-Nachweis behandelt.** Er deckt eventuell den Integrationspfad nicht ab. **Abhilfe:** Die Nachweisstufe aufbewahren, die das Abnahmekriterium verlangt.
- **Eine Agenten-Nachricht verändert die Produktionszuständigkeit.** Chatverlauf ist kein Autorisierungsmechanismus. **Abhilfe:** Eine explizite Berechtigung, Freigabe oder dokumentierte Operator-Aktion verlangen.

## Quellen {#sources}

- [Git worktrees](https://git-scm.com/docs/git-worktree)
- [Git merge documentation](https://git-scm.com/docs/git-merge)

## Siehe auch {#see-also}

- [[agent-orchestration]]
- [[multi-agent-messaging]]
- [[handoff-rollup-pattern]]
- [[agentic-security-2026]]
- [[claude-code-harness-patterns]]

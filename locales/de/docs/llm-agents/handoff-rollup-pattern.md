---
title: "Session-Übergabe-Rollups"
description: "Wie man eine begrenzte, nachvollziehbare Zusammenfassung länger laufender Agentenarbeit erstellt, ohne so zu tun, als wäre eine Zusammenfassung verlustfrei."
tags: [handoff, continuity, context-management, agent-operations, documentation]
level: 3
source_sha256: 07890b896ab508e075fe1b8d8d6f7ce0837027ca93ee8fa1418e6f0ad0859ffa
translation: machine
translated_at: '2026-10-24'
---
# Session-Übergabe-Rollups {#session-handoff-rollups}

**Geprüfter Stand: 2026-09-03.** Ein Rollup ist ein datierter Schnappschuss, der dem nächsten Operator hilft, ein Projekt wieder aufzunehmen. Er ist kein Ersatz für die Quellhistorie, keine Garantie für verlustfreie Kompression und kein Grund, die Belege zu löschen, die frühere Entscheidungen gestützt haben.

Das sichere Wiederaufnahme-Set besteht aus einem verifizierten Rollup plus dem begrenzten Ende der Einträge, die nach seinem Schnittpunkt erfasst wurden.

## Warum es ein Rollup gibt {#why-a-rollup-exists}

Langlaufende Arbeit sammelt viele kleine Übergaben an: abgeschlossene Aktionen, aktive Randbedingungen, fehlgeschlagene Versuche und ausstehende Freigaben. Wenn man nur die jüngste Übergabe liest, kann eine noch gültige Entscheidung verloren gehen. Jede historische Notiz zu lesen ist langsam und kann veralteten Kontext nach vorne holen.

Ein Rollup beantwortet vier Fragen:

1. Welche genauen Quelldatensätze deckt es ab?
2. Was ist am Schnittpunkt verifiziert, gemeldet, blockiert oder unbekannt?
3. Welche Artefakte, Revisionen und Belege bleiben maßgeblich?
4. Welche Einträge muss eine neue Session nach dem Schnittpunkt lesen?

## Der Snapshot-Vertrag {#the-snapshot-contract}

Explizites Frontmatter und stabile Quellreferenzen verwenden:

```yaml
---
project: example-project
status: ACTIVE
as_of: 2026-09-03T20:15:00Z
covered_sources:
  - handoff-2026-08-30-a
  - handoff-2026-09-01-b
source_index_ref: handoffs/INDEX.md
verification_ref: receipts/rollup-2026-09-03.json
---
```

`as_of` ist das letzte enthaltene Quellereignis, nicht der Zeitpunkt, zu dem jemand die Zusammenfassung zufällig geschrieben hat. Ein Leser lädt:

```text
current rollup
  + source index
  + every entry after as_of
  + artifacts named by the current task
```

Das Ende muss begrenzt bleiben. Ein neues Rollup erstellt man an einer Phasengrenze oder wenn der Index zeigt, dass die normale Wiederaufnahme wieder zu viele Quelldatensätze erfordert.

## Zurechnung und Konfidenz erhalten {#preserve-attribution-and-confidence}

Jede wichtige Aussage sollte nachvollziehbar sein:

| Feld | Bedeutung |
|---|---|
| claim | knappe Aussage zum aktuellen Zustand |
| confidence | `VERIFIED`, `REPORTED`, `UNKNOWN` oder `BLOCKED` |
| evidence reference | Testausgabe, Commit, Issue, Laufzeitbeleg oder Nutzermeldung |
| owner | wer den nächsten Schritt ausführen darf |
| recheck | Ereignis oder Befehl, der die Aussage ändern kann |

Dadurch macht eine Zusammenfassung aus einer vorläufigen Diagnose keine Tatsache. Fehlt eine Quelle oder lässt sich eine Aussage nicht reproduzieren, kennzeichnet man sie als `UNKNOWN`; die Lücke wird nicht aus dem Gedächtnis der Unterhaltung gefüllt.

## Sicheres Rollup-Verfahren {#safe-rollup-procedure}

1. Die abzudeckenden Handoff-IDs, Commits, Belege und aktiven Branches inventarisieren;
2. einen unveränderlichen Schnittpunkt wählen und festhalten;
3. nur Entscheidungen, Randbedingungen, verifizierte Ergebnisse, Fehlschläge und offene Zuständigkeiten extrahieren;
4. jeder wesentlichen Schlussfolgerung eine Quellreferenz beifügen;
5. das Rollup mit dem Quellindex vergleichen und den angegebenen Wiederaufnahmepfad testen;
6. das Rollup als neues, nur anhängbares Artefakt veröffentlichen;
7. spätere Übergaben im Ende für das nächste Rollup belassen.

Ursprüngliche Übergaben dürfen nicht überschrieben werden, nur damit das Rollup sauberer aussieht. Wird im Index eine Beziehung benötigt, fügt man eine Indexzeile oder eine Rückverweisung hinzu, nachdem geprüft wurde, dass gleichzeitige Schreiber sie nicht verlieren können.

## Parallele Arbeit erfordert eine Schnittgrenze {#parallel-work-requires-a-cut-boundary}

Ein laufendes, verzweigtes Projekt darf nicht rollup-artig behandelt werden, als wäre es seriell. Am Schnittpunkt gilt:

- jeden aktiven Branch und Worktree erfassen;
- Ressourcen-Leases und ihre Eigentümer identifizieren;
- nicht zusammengeführte Änderungen als `RUNNING` behandeln, nicht als abgeschlossen;
- Nachrichten oder Belege festhalten, die noch unterwegs sind;
- neue Schreibvorgänge nach dem Schnittpunkt im Ende belassen.

Kann der Schnappschuss seine Schreiber und Artefakte nicht benennen, verschiebt man ihn, statt ein vollständiges Bild zu konstruieren.

## Aufbau des Rollups {#rollup-structure}

```text
purpose and scope
covered source IDs and cut point
verified current state
active work and owners
decisions and rejected paths
known failures and evidence
release or publication gates
next safe action and recheck
tail-reading rule
```

Die nächste sichere Aktion ist eine Hilfe zur Fortsetzung, keine Anweisung, eine Freigabe zu umgehen, eine nicht umkehrbare Wirkung erneut auszulösen oder ein unverbundenes Projekt zu ändern.

## Vor der Wiederverwendung validieren {#validate-before-reuse}

Bevor eine neue Session auf ein Rollup hin handelt:

1. prüfen, ob die zitierte Repository-Revision bzw. der Laufzeitzustand noch existiert;
2. prüfen, ob das Recheck-Ereignis eingetreten ist;
3. alle Einträge des Endes nach `as_of` lesen;
4. jede Ressourcen-Lease extern verifizieren, bevor man sie übernimmt;
5. einen neuen Schnappschuss erstellen, wenn der aktuelle veraltet ist.

So bleibt die Übergabe nützlich, selbst wenn eine frühere Session unerwartet beendet wurde.

## Fallstricke {#gotchas}

- **Ein Rollup hat keinen expliziten Schnittpunkt.** Leser können nicht wissen, was sie ergänzen sollen. **Abhilfe:** `as_of` und die erfassten Quellkennungen festhalten.
- **Eine Zusammenfassung markiert jeden Zustand als erledigt.** Sie verbirgt fehlgeschlagene Prüfungen und ausstehende Zuständigkeiten. **Abhilfe:** Konfidenz- und Endzustandskennzeichnungen zusammen mit Belegen verwenden.
- **Gleichzeitige Agenten bearbeiten denselben Index.** Ein späterer Schreiber kann eine andere Beziehung verwerfen. **Abhilfe:** nur anhängbare Datensätze bevorzugen oder die veränderliche Indexaktualisierung serialisieren.
- **Das Ende wird so groß wie die ursprüngliche Historie.** Das Rollup verbessert die Wiederauffindung nicht mehr. **Abhilfe:** nach der nächsten verifizierten Phasengrenze einen neuen datierten Schnappschuss erstellen.
- **Ein altes Rollup wird als gültige Richtlinie behandelt.** Es kann veraltete Entscheidungen wieder einführen. **Abhilfe:** vor dem Handeln `as_of`, Belege und Recheck-Regeln prüfen.

## Siehe auch {#see-also}

- [[multi-session-coordination]]
- [[session-persistence]]
- [[agent-memory]]
- [[claude-code-harness-patterns]]

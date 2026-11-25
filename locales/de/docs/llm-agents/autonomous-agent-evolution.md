---
title: "Autonome Agenten-Evolution"
description: "Parallele Agenten-Experimente sicher durchführen mit isolierten Worktrees, append-only Nachweisen, Ressourcensperren und unabhängiger Bewertung"
level: 3
source_sha256: fd7adfe8af09f6d68cbe6f4efb6b7d7a7df59243206c8ba7fc75b844620ba0f4
translation: machine
translated_at: '2026-10-24'
---
# Autonome Agenten-Evolution (September 2026) {#autonomous-agent-evolution-september-2026}

Versionskontext: Diese Seite beschreibt eine kontrollierte Experimentarchitektur und keine Aussage, dass autonome Agenten Produktivsysteme verändern sollten. Fixieren Sie für jeden Lauf die Repository-Revision, den Evaluator, das Task-Manifest, das Umgebungs-Image und die Ressourcenrichtlinie.

Parallele Agenten können unabhängige Kandidatenänderungen erkunden, aber nur dann, wenn die Arbeit ein messbares Ziel, einen isolierten Änderungsraum und einen Freigabepfad besitzt, der nicht unterstützte Ergebnisse ablehnt.

## Zulassungskriterien {#admission-gate}

Starten Sie keinen parallelen Evolutionslauf, bevor alle Bedingungen erfüllt sind:

1. Ein Task-Manifest listet jede Kandidateneinheit der Arbeit auf.
2. Ein deterministischer oder unabhängig prüfbarer Evaluator existiert.
3. Jeder Worker hat einen isolierten Branch/Worktree oder eine Sandbox.
4. Gemeinsam veränderbare Ressourcen besitzen explizite Sperren und eine externe Verifikation.
5. Ausgabeartefakte haben stabile IDs, Digests und eine Aufbewahrungsrichtlinie.
6. Ein Koordinator verantwortet Freigabe, Rollback und die abschließende Buchhaltung.

Ohne diese Bedingungen erzeugen parallele Agenten gleichzeitige Änderungen und ungeprüfte Erzählungen statt Nachweisen.

## Isolationsmodell {#isolation-model}

Git-Worktrees erlauben mehrere ausgecheckte Branches eines Repositorys. Sie isolieren Dateiänderungen pro Branch, isolieren aber nicht Prozesse, Netzwerkzugriff, Zugangsdaten, eingebundene Laufwerke oder Cloud-Ressourcen.

```text
coordinator
  ├── worker-a: worktree + branch + task shard
  ├── worker-b: worktree + branch + task shard
  └── evaluator: fresh context, read-only evidence review
shared: append-only receipts + explicit resource locks
```

Verwenden Sie Kontrollen auf Umgebungsebene, wenn Worker keine Geheimnisse, GPU-Kapazität, Ports, Datenbanken oder Zugangsdaten externer Dienste teilen dürfen.

## Manifestgestützte Arbeit {#manifest-backed-work}

```json
{
  "run_id": "evolution-2026-09-03",
  "baseline_commit": "abc123",
  "evaluator_revision": "git:eval456",
  "objective": "accepted_task_rate",
  "guard_metrics": {"policy_violations_max": 0},
  "shards": [
    {"id": "A", "state": "pending", "owner": null},
    {"id": "B", "state": "pending", "owner": null}
  ],
  "promotion_state": "hold"
}
```

Ein Shard gilt erst dann als abgeschlossen, wenn er einen endgültigen Bewertungsbeleg besitzt. Ein Worker-Prozess, ein Branch oder eine Fortschrittsmeldung ist kein Nachweis für den Abschluss.

## Worker-Protokoll {#worker-protocol}

Für jeden zugewiesenen Shard:

1. Prüfen Sie unter der Manifest-Sperre, dass der Shard noch `pending` ist.
2. Erstellen Sie einen isolierten Worktree/Branch ab der festgehaltenen Baseline oder beanspruchen Sie ihn.
3. Wenden Sie genau eine begrenzte Kandidatenänderung an.
4. Führen Sie den benannten Evaluator aus und bewahren Sie Rohergebnis, Digest, Umgebung und Commit-ID auf.
5. Markieren Sie den Shard als `passed`, `rejected` oder `blocked_external` mit einer Begründung.
6. Senden Sie nur Nachweisreferenzen an den Koordinator; niemals direkt in die Baseline übernehmen.

Ein Worker sollte eine bereits versuchte Aufgabe nicht wiederverwenden, ohne den früheren Beleg und den Idempotenzschlüssel abzugleichen.

## Gemeinsames Wissen ohne Wettlaufbedingungen {#shared-knowledge-without-races}

Halten Sie gemeinsame Informationen in zwei Kategorien:

| Zustand | Sichere Darstellung | Regel |
|---|---|---|
| Nachweise, Beobachtungen, Belege | Append-only-Dateien pro Lauf | Den Datensatz eines anderen Workers niemals überschreiben |
| Sperren, Reservierungen, aktueller Gewinner | Eine ressourcenspezifische Datei | Atomar beanspruchen; externen Zustand vor einer Wiederherstellung prüfen |

Beispiel für einen Beleg:

```json
{
  "shard_id": "A",
  "candidate_commit": "def456",
  "parent_commit": "abc123",
  "evaluator_digest": "sha256:...",
  "primary_metric": 0.0,
  "guards": {"policy_violations": 0},
  "verdict": "rejected",
  "recorded_at": "2026-09-03T18:00:00Z"
}
```

Beobachtungen sind hilfreich, aber keine gemeinsamen Anweisungen. Behandeln Sie von Agenten verfasste Notizen als nicht vertrauenswürdige Hypothesen, bis der referenzierte Evaluator oder die Quelle sie bestätigt.

## Auswahl und Freigabe {#selection-and-promotion}

Der Koordinator vergleicht nur Belege, die vom selben Evaluator-Revisionsstand und in vergleichbarer Umgebung erzeugt wurden. Ein Kandidat gewinnt nur dann, wenn er das primäre Ziel verbessert und alle Guards besteht.

```text
candidate receipt -> independent evaluator -> selection record
                  -> integration test -> staged/canary evidence -> promotion
```

Verwenden Sie für die finale Abnahme einen frischen Evaluator-Kontext. Der Worker, der eine Änderung vorgenommen hat, kann deren semantische Korrektheit nicht selbst bescheinigen.

## Ressourcensperren {#resource-locks}

Git ist kein Sperrmanager für GPUs, Ports, Datenbanken, entfernte Warteschlangen oder externe URLs. Erfassen Sie für jede veränderbare Ressource Besitzer, Heartbeat, Prozess-ID oder Reservierungs-ID, Versuchsbudget und Wiederherstellungsverfahren.

Bevor Sie eine veraltete Sperre freigeben, prüfen Sie extern, ob der Besitzerprozess oder die entfernte Operation nicht mehr aktiv ist. Schließen Sie nicht allein aus einem alten Zeitstempel, dass eine Ressource frei ist.

## Stagnation und Stoppbedingungen {#stagnation-and-stop-conditions}

Stoppen oder lenken Sie einen Lauf um, wenn:

- jeder Shard einen endgültigen Beleg besitzt;
- der Evaluator ungültig oder nicht verfügbar ist;
- wiederholte Kandidaten unter derselben Messung zurückfallen;
- ein Ressourcen- oder Sicherheitsguard ausgelöst wurde;
- das konfigurierte Versuchs-, Kosten- oder Zeitbudget erreicht ist.

Eine Änderung der Metrik nach einem Plateau ist ein neues Experiment und keine Fortsetzung. Bewahren Sie abgelehnte Nachweise auf, damit künftige Worker denselben fehlgeschlagenen Kandidaten nicht erneut versuchen.

## Fallstricke {#gotchas}

- **Worktrees bieten keine vollständige Isolation.** Sie teilen Prozesse, Zugangsdaten und eingebundene Ressourcen des Hosts. **Abhilfe:** Isolation auf Umgebungsebene und pro Ressource Sperren ergänzen, wo nötig.
- **Parallele Fortschrittsmeldungen können doppelte Arbeit verbergen.** Zwei Worker könnten denselben Kandidaten evaluieren. **Abhilfe:** Shards im Manifest mit Idempotenzschlüssel reservieren und Belege prüfen.
- **Gemeinsame Notizen können eine falsche Hypothese verbreiten.** Die Zusammenfassung eines Agenten kann falsch oder veraltet sein. **Abhilfe:** Jede wiederverwendbare Beobachtung mit einem Evaluator-Beleg oder einer Primärquelle verknüpfen.
- **Ein höherer Wert kann ein ungültiger Vergleich sein.** Eine andere Umgebung, ein anderer Seed, andere Daten oder eine andere Evaluator-Revision verändern das Experiment. **Abhilfe:** Nur kompatible Belege vergleichen und alle wesentlichen Eingaben festhalten.
- **Automatische Freigabe ist eine Rechteausweitung.** Ein bestandener Worker-Test autorisiert keine Änderung am Produktivsystem. **Abhilfe:** Unabhängige Bewertung, Integrationsnachweise und einen definierten Freigabeverantwortlichen verlangen.

## Quellen {#sources}

- [Git worktree documentation](https://git-scm.com/docs/git-worktree)
- [OpenAI API: working with evals](https://developers.openai.com/api/docs/guides/evals)
- [OpenAI Agents SDK: agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
- [OpenAI Agents SDK: tracing](https://openai.github.io/openai-agents-python/tracing/)

## Siehe auch {#see-also}

- [[agent-self-improvement]]
- [[agent-evaluation]]
- [[multi-agent-systems]]
- [[agent-architectures]]
- [[production-patterns]]

---
title: "Session-Persistenz"
category: patterns
tags: [llm-memory, session-handoff, persistent-state, memory-files, journal]
level: 3
source_sha256: 3627d5c2c71e8711a41ada99d3d73e76abfe5dc0e883ce0a381e7c6d7e677474
translation: machine
translated_at: '2026-10-24'
---
# Session-Persistenz {#session-persistence}

Wie Wissen, Entscheidungen und Fortschritte zwischen LLM-Agent-Sessions erhalten bleiben. Da jede Session mit einem leeren Kontext beginnt, sind explizite Persistenzmechanismen erforderlich. Der Agent „erinnert“ sich nie automatisch an etwas.

## Kernfakten {#key-facts}

- Jede LLM-Session beginnt ohne Gedächtnis, sofern kein externer Zustand geladen wird
- Eine strukturierte Übergabe (500–2000 Tokens) ist mit etwa 50-facher Kompression einem rohen Gesprächsdump (50–100K Tokens) überlegen
- Drei Fragen definieren eine gute Übergabe: Was funktioniert, ist kaputt oder blockiert? Was NICHT erneut versucht werden sollte? Was ist der EINE nächste Schritt?
- Dateibasierter Zustand überlebt Kontext-Kompaktierung und Session-Neustarts, der Gesprächsverlauf dagegen nicht
- Automatisches Speichern an wichtigen Punkten (alle N Nachrichten, vor der Kompaktierung, bei Themenwechsel) verhindert Datenverlust

## Persistenzmechanismen {#persistence-mechanisms}

| Mechanismus | Persistenz | Struktur | Geeignet für |
|-----------|------------|-----------|----------|
| **Handoff-Datei** | Zwischen Sessions | Semi-strukturiertes Markdown | Session-Kontinuität |
| **Memory-Datei** | Dauerhaft | Key-Value-Index mit Links | Benutzerpräferenzen, Projektfakten |
| **State-Datei** | Pro Aufgabe | JSON/YAML | Fortschritt mehrstufiger Aufgaben |
| **Journal** | Kumulativ | Datierte Einträge | Mehrtägige Projekte |
| **Konversationsexport** | Archiv | Rohe Nachrichten | Audit-Trail (nicht zum Laden gedacht) |

## Handoff-Datei-Muster {#handoff-file-pattern}

Wird am Session-Ende geschrieben und am Session-Anfang gelesen. Strukturiertes Briefing, kein Dump.

```markdown
# Session Handoff - 2026-04-08 14:30

## Goal
Migrate payment API from Stripe v2 to v3

## Done
- Schema migration script (payments/migrate_v3.py) - tested
- Webhook handler updated for new event format
- Integration tests passing for charge/refund flows

## NOT Working (and why)
- Subscription renewal webhook - v3 changed event payload structure,
  our handler expects `subscription.id` but v3 sends `subscription_id`
- Retry logic - v3 uses idempotency keys differently, current retry
  creates duplicate charges

## Failed Approaches (DO NOT retry)
- monkey-patching stripe library to translate v2 events -> fails silently
  on edge cases (partial refunds, disputes)
- Using stripe's v2 compatibility mode -> deprecated, removed in April

## Key Decisions
- Chose direct v3 migration over gradual rollout because v2 sunset is May 1

## Next Step
Fix subscription webhook handler - map new field names in
payments/webhooks/subscription.py line 45
```

**Regeln:**
- Maximal 1500 Tokens. Briefing, kein Log
- Echte Fehlermeldungen aufnehmen, keine Beschreibungen
- „Fehlgeschlagene Ansätze“ ist Pflicht, auch wenn es offensichtlich erscheint
- Absolute Dateipfade für alle referenzierten Dateien
- Nicht enthalten: Tool-Call-Verlauf, Zwischenlesevorgänge, rohe Befehlsausgaben

## Memory-Datei-Muster {#memory-file-pattern}

Dauerhafter Key-Value-Index, der mit der Zeit wächst. Nach Themen organisiert, mit Links zu Detaildateien.

```markdown
# Memory Index

## User
- user_profile - name, preferences, communication style

## Projects
- api-rewrite - REST->GraphQL, timeline, decisions
- ml-pipeline - training infra, model registry

## Infrastructure
- prod-cluster - K8s on GCP, 3 node pools, autoscaling
- ci-cd - GitHub Actions, deploy to staging/prod

## Decisions
- db-choice - PostgreSQL, reasons, alternatives considered
- api-style - GraphQL over REST, tradeoffs documented
```

Jede verlinkte Datei enthält strukturierte Details. Der Index selbst bleibt klein genug, um immer in den Kontext zu passen.

## State-Datei-Muster {#state-file-pattern}

Für mehrstufige Aufgaben. JSON/YAML mit explizitem Fortschrittstracking.

```json
{
  "task": "migrate-stripe-v3",
  "status": "in_progress",
  "plan": [
    {"step": "schema migration", "status": "done", "output": "payments/migrate_v3.py"},
    {"step": "webhook handlers", "status": "in_progress", "blocker": "subscription event format"},
    {"step": "retry logic", "status": "blocked", "reason": "idempotency key changes"},
    {"step": "integration tests", "status": "pending"},
    {"step": "load testing", "status": "pending"}
  ],
  "findings": [
    "v3 renames subscription.id -> subscription_id in all webhook payloads",
    "idempotency keys are now required, not optional"
  ],
  "failed_approaches": [
    "monkey-patch stripe lib - fails on partial refunds",
    "v2 compatibility mode - deprecated"
  ]
}
```

Der Agent liest den Zustand zu Beginn eines Schritts, führt ihn aus und aktualisiert den Zustand. Das überlebt Kompaktierung und Kontext-Resets.

## Journal-Muster {#journal-pattern}

Für mehrtägige Projekte. Nur anhängend, mit datierten Einträgen.

```markdown
# Project Journal

## 2026-04-08
- Completed schema migration script
- Found: v3 webhook payload structure changed significantly
- Decided: direct migration, no compatibility layer
- Blocked: subscription webhook needs field mapping

## 2026-04-07
- Started Stripe v3 migration
- Read v3 changelog - 47 breaking changes identified
- Prioritized: payment flows first, subscription second
- Created: task plan in .agent/state.json
```

**Wann Journal, wann Handoff:** Der Handoff dient dem Session-Wechsel (flüchtig, wird jedes Mal ersetzt). Das Journal dient der Projekthistorie (kumulativ, nur anhängend). Bei langen Projekten beides verwenden.

## Muster {#patterns}

### Session-Start-Protokoll {#session-start-protocol}

```text
1. Check for HANDOFF.md
   - If exists: read, summarize to user, ask to continue or start fresh
   - Archive to handoff-history/YYYY-MM-DD-HHMM.md

2. Check for state files (.agent/state.json, PLAN.md)
   - If exists: load current task state

3. Read MEMORY.md index
   - Load L0/L1 identity and critical facts

4. Ready to work with full context
```

### Session-End-Protokoll {#session-end-protocol}

```sql
1. If session > 15 minutes:
   - Write/update HANDOFF.md
   - Update MEMORY.md if new permanent knowledge discovered
   - Update state files if task is in progress

2. Update journal if multi-day project

3. Commit state files if using version control
```

### Lernextraktion {#learning-extraction}

Nach jeder Session wiederverwendbares Wissen extrahieren:

```bash
Categories to extract:
- [DECISION] - architectural choices with reasoning
- [GOTCHA] - unexpected behavior, edge cases
- [REUSE] - patterns worth remembering
- [CORRECTION] - user corrected the agent's approach

Flow:
Session ends → extract tagged findings → triage (future-relevant only)
  → transform into knowledge (rewrite as facts, not history)
  → merge into MEMORY.md or relevant knowledge base
```

## Fallstricke {#gotchas}

- **Rohe Gesprächsdumps sind für die Kontinuität nutzlos.** 50–100K Tokens Gesprächsverlauf sind Rauschen. Eine strukturierte 500-Token-Übergabe enthält mehr umsetzbare Information. Rohe Transkripte sollten nie als Persistenzmechanismus dienen
- **Übergaben ohne „Was ist fehlgeschlagen“ führen zu wiederholten Fehlern.** Die nächste Session probiert dieselben Ansätze und scheitert auf dieselbe Weise. Fehlgeschlagene Ansätze immer mit konkreten Gründen angeben
- **Veraltete Übergaben sind schlimmer als gar keine.** Verweist die Übergabe auf gelöschte Dateien oder refaktorierten Code, wird der Agent verwirrt. Übergaben datieren und alte archivieren. Nur die letzten 10 im Verlauf behalten

## Siehe auch {#see-also}

- [[context-window-management]]
- [[memory-architectures]]
- [[knowledge-base-as-memory]]
- [[temporal-memory]]
- [[forgetting-strategies]]

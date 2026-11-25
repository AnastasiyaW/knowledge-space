---
title: "Persistance de session"
category: patterns
tags: [llm-memory, session-handoff, persistent-state, memory-files, journal]
level: 3
source_sha256: 3627d5c2c71e8711a41ada99d3d73e76abfe5dc0e883ce0a381e7c6d7e677474
translation: machine
translated_at: '2026-10-24'
---
# Persistance de session {#session-persistence}

Comment conserver les connaissances, les décisions et la progression entre les sessions d'agents LLM. Chaque session démarre avec un contexte vierge : des mécanismes de persistance explicites sont donc nécessaires. L'agent ne « se souvient » jamais de rien automatiquement.

## Points clés {#key-facts}

- Chaque session LLM démarre sans aucune mémoire, sauf si un état externe est chargé
- Un handoff structuré (500 à 2000 tokens) est préférable à un dump brut de la conversation (50 à 100K tokens), avec un ratio de compression d'environ 50x
- Trois questions définissent un bon handoff : ce qui fonctionne, ce qui est cassé ou bloqué, et quelle est LA prochaine étape
- Un état stocké dans des fichiers survit à la compaction du contexte et aux redémarrages de session, contrairement à l'historique de conversation
- Une sauvegarde automatique à des moments clés (tous les N messages, avant la compaction, lors d'un changement de sujet) prévient la perte de données

## Mécanismes de persistance {#persistence-mechanisms}

| Mécanisme | Persistance | Structure | Idéal pour |
|-----------|------------|-----------|----------|
| **Fichier de handoff** | Entre les sessions | Markdown semi-structuré | Continuité de session |
| **Fichier de mémoire** | Permanent | Index clé-valeur avec liens | Préférences utilisateur, faits du projet |
| **Fichier d'état** | Par tâche | JSON/YAML | Progression de tâches multi-étapes |
| **Journal** | Cumulatif | Entrées datées | Projets s'étalant sur plusieurs jours |
| **Export de conversation** | Archive | Messages bruts | Piste d'audit (pas pour le chargement) |

## Modèle de fichier de handoff {#handoff-file-pattern}

Rédigé en fin de session, lu en début de session. C'est un briefing structuré, pas un dump.

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

**Règles :**
- 1500 tokens maximum : un briefing, pas un journal
- Inclure les messages d'erreur réels, pas des descriptions
- La section « Approches échouées » est obligatoire, même si cela semble évident
- Chemins de fichiers absolus pour tous les fichiers référencés
- Ne pas inclure : l'historique des appels d'outils, les lectures intermédiaires, la sortie brute des commandes

## Modèle de fichier de mémoire {#memory-file-pattern}

Index clé-valeur permanent qui grandit au fil du temps. Organisé par sujet, avec des liens vers des fichiers de détail.

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

Chaque fichier lié contient des détails structurés. L'index lui-même reste assez petit pour toujours tenir dans le contexte.

## Modèle de fichier d'état {#state-file-pattern}

Pour les tâches multi-étapes. JSON/YAML avec un suivi explicite de la progression.

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

L'agent lit l'état au début de chaque étape, exécute, puis met l'état à jour. Ce mécanisme survit à la compaction et aux réinitialisations de contexte.

## Modèle de journal {#journal-pattern}

Pour les projets s'étalant sur plusieurs jours. Ajout seul (append-only), entrées datées.

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

**Quand utiliser le journal plutôt que le handoff :** le handoff sert aux transitions de session (volatile, remplacé à chaque fois). Le journal sert à l'historique du projet (cumulatif, en ajout seul). Pour les projets longs, utiliser les deux.

## Patterns {#patterns}

### Protocole de démarrage de session {#session-start-protocol}

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

### Protocole de fin de session {#session-end-protocol}

```sql
1. If session > 15 minutes:
   - Write/update HANDOFF.md
   - Update MEMORY.md if new permanent knowledge discovered
   - Update state files if task is in progress

2. Update journal if multi-day project

3. Commit state files if using version control
```

### Extraction des apprentissages {#learning-extraction}

Après chaque session, extraire les connaissances réutilisables :

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

## Pièges {#gotchas}

- **Les dumps bruts de conversation sont inutiles pour la continuité.** 50 à 100K tokens d'historique de conversation sont du bruit. Un handoff structuré de 500 tokens contient davantage d'informations exploitables. Ne jamais utiliser de transcriptions brutes comme mécanisme de persistance
- **Un handoff sans « ce qui a échoué » provoque la répétition des échecs.** La session suivante essaiera les mêmes approches et échouera de la même manière. Toujours inclure les approches échouées, avec les raisons précises de l'échec
- **Un handoff périmé est pire que l'absence de handoff.** Si le handoff référence des fichiers supprimés ou du code refactorisé, l'agent sera désorienté. Dater les handoffs et archiver les anciens. Ne conserver que les 10 derniers dans l'historique

## Voir aussi {#see-also}

- [[context-window-management]]
- [[memory-architectures]]
- [[knowledge-base-as-memory]]
- [[temporal-memory]]
- [[forgetting-strategies]]

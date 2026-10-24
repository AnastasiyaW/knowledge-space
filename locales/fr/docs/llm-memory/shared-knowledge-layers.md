---
title: "Couches de connaissances partagées pour les systèmes multi-agents"
category: patterns
tags: [llm-memory, multi-agent, shared-memory, knowledge-sharing, heartbeat]
level: 3
source_sha256: 36ad6473b58822091948e6b581dc5e5919b96516275b4a9ed6f487a0117f699a
translation: machine
translated_at: '2026-10-24'
---
# Couches de connaissances partagées pour les systèmes multi-agents {#shared-knowledge-layers-for-multi-agent-systems}

Lorsque plusieurs agents travaillent en parallèle, ils ont besoin d'une manière structurée de partager leurs découvertes sans interférer avec le travail des autres. Le patron consiste en des espaces de travail isolés et une couche de connaissances partagée, au moyen de fichiers.

## Faits clés {#key-facts}

- Chaque agent dispose d'un **espace de travail isolé** (git worktree, répertoire séparé, conteneur) : il ne peut pas casser le travail des autres
- Une **couche publique partagée** est accessible à tous les agents via des liens symboliques ou un montage partagé :
  - `attempts/` : évaluations historiques avec scores et hachages de commit
  - `notes/` : observations en markdown, organisées hiérarchiquement par sujet
  - `skills/` : procédures et scripts réutilisables, extraits d'exécutions réussies
- Les agents lisent la couche partagée avant de commencer leur travail, et y écrivent après avoir terminé leurs évaluations
- Sans couche partagée : les agents dupliquent le travail, répètent des approches infructueuses et ne capitalisent pas les uns sur les autres
- Avec couche partagée : taux d'amélioration 3 à 10 fois plus élevés et 4 fois moins d'évaluations nécessaires

## Patrons {#patterns}

### Mécanisme de heartbeat {#heartbeat-mechanism}

Réflexion périodique forcée qui empêche les agents de se fixer sur une seule approche :

```php
Per-iteration (after each eval):
  -> Write observation to notes/
  -> Record attempt score in attempts/

Periodic consolidation (every ~10 evals):
  -> Review own progress
  -> Read other agents' notes
  -> Distill patterns into skills/
  -> Reorganize notes hierarchy

Stagnation redirection (5+ non-improving):
  -> Forced reassessment
  -> Read all shared notes for inspiration
  -> Pivot to different approach
```

### Mémoire partagée basée sur des fichiers {#file-based-shared-memory}

```python
.shared/
  attempts/
    eval-001.json     # {approach, score, commit, timestamp}
    eval-002.json
  notes/
    optimization/
      learning-rate.md
      batch-size.md
    architecture/
      attention-variants.md
  skills/
    grid-search.sh
    evaluate-model.py
```

### Mise en œuvre avec des agents Claude Code {#implementation-with-claude-code-agents}

```bash
# Agent 1 workspace
git worktree add agent-1 main
ln -s ../shared agent-1/.shared

# Agent 2 workspace  
git worktree add agent-2 main
ln -s ../shared agent-2/.shared

# Each agent's CLAUDE.md includes:
# "Before starting: read .shared/notes/ for context"
# "After each significant finding: write to .shared/notes/"
# "Every 10 iterations: consolidate and share skills"
```

### Détection de stagnation {#stagnation-detection}

```python
def check_stagnation(attempts_dir, threshold=5):
    """Detect if agent is stuck on non-improving approaches."""
    recent = sorted(Path(attempts_dir).glob("*.json"))[-threshold:]
    scores = [json.loads(f.read_text())["score"] for f in recent]
    
    if len(scores) >= threshold:
        best = max(scores[:-threshold]) if len(scores) > threshold else 0
        recent_best = max(scores[-threshold:])
        if recent_best <= best:
            return True  # Stagnant - force pivot
    return False
```

## Pièges {#gotchas}

- **Problème :** Les agents écrivent simultanément des observations contradictoires dans les notes partagées -> **Solution :** Utiliser des fichiers en ajout seul (append-only) ou des noms de fichiers préfixés par l'agent (`agent-1-note-003.md`). Ne jamais écraser les notes des autres
- **Problème :** Les compétences partagées deviennent obsolètes à mesure que le problème évolue -> **Solution :** Étiqueter chaque compétence avec le score d'évaluation qu'elle a produit. Les agents peuvent juger de la pertinence d'après la récence des scores
- **Problème :** Un état partagé trop volumineux amène les agents à converger vers la même approche -> **Solution :** Limiter la lecture des notes aux phases de consolidation (et non à chaque itération). La diversité des approches a de la valeur
- **Problème :** La consolidation du heartbeat est coûteuse (lecture de toutes les notes, réécriture) -> **Solution :** Utiliser une consolidation incrémentale, en ne traitant que les notes plus récentes que l'horodatage de la dernière consolidation

## Voir aussi {#see-also}

- [[memory-architectures]] - structures de mémoire hiérarchiques
- [[session-persistence]] - conservation des connaissances entre les sessions
- [[temporal-memory]] - fenêtres de validité pour les faits partagés
- [[agent-orchestration]] - coordination de plusieurs agents

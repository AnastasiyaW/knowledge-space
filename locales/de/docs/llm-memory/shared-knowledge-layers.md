---
title: "Gemeinsame Wissensebenen für Multi-Agenten-Systeme"
category: patterns
tags: [llm-memory, multi-agent, shared-memory, knowledge-sharing, heartbeat]
level: 3
source_sha256: 36ad6473b58822091948e6b581dc5e5919b96516275b4a9ed6f487a0117f699a
translation: machine
translated_at: '2026-10-24'
---
# Gemeinsame Wissensebenen für Multi-Agenten-Systeme {#shared-knowledge-layers-for-multi-agent-systems}

Wenn mehrere Agenten parallel arbeiten, brauchen sie eine strukturierte Möglichkeit, Erkenntnisse zu teilen, ohne sich gegenseitig in ihrer Arbeit zu stören. Das Muster: isolierte Arbeitsbereiche plus eine gemeinsame Wissensebene über Dateien.

## Kernfakten {#key-facts}

- Jeder Agent erhält einen **isolierten Arbeitsbereich** (Git-Worktree, eigenes Verzeichnis, Container) – so kann er die Arbeit anderer nicht beschädigen
- Eine **gemeinsame öffentliche Ebene** ist für alle Agenten über Symlinks oder einen gemeinsamen Mount erreichbar:
  - `attempts/` – historische Bewertungen mit Scores und Commit-Hashes
  - `notes/` – Markdown-Beobachtungen, hierarchisch nach Thema geordnet
  - `skills/` – wiederverwendbare Verfahren und Skripte, die aus erfolgreichen Läufen destilliert wurden
- Agenten lesen die gemeinsame Ebene, bevor sie mit der Arbeit beginnen, und schreiben in sie, nachdem sie Bewertungen abgeschlossen haben
- Ohne gemeinsame Ebene: Agenten doppeln Arbeit, wiederholen fehlgeschlagene Ansätze und bauen nicht aufeinander auf
- Mit gemeinsamer Ebene: 3- bis 10-fach höhere Verbesserungsraten, 4-fach weniger benötigte Bewertungen

## Muster {#patterns}

### Heartbeat-Mechanismus {#heartbeat-mechanism}

Periodische erzwungene Reflexion, die verhindert, dass Agenten sich auf einen Ansatz festfahren:

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

### Dateibasierter gemeinsamer Speicher {#file-based-shared-memory}

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

### Implementierung mit Claude-Code-Agenten {#implementation-with-claude-code-agents}

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

### Erkennung von Stagnation {#stagnation-detection}

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

## Fallstricke {#gotchas}

- **Problem:** Agenten schreiben gleichzeitig widersprüchliche Beobachtungen in die gemeinsamen Notizen -> **Lösung:** Append-only-Dateien oder agentenspezifische Dateinamen verwenden (`agent-1-note-003.md`). Notizen anderer niemals überschreiben
- **Problem:** Gemeinsame Skills veralten, wenn sich das Problem weiterentwickelt -> **Lösung:** Skills mit dem Bewertungsscore markieren, den sie erzeugt haben. Agenten können die Relevanz anhand der Aktualität des Scores beurteilen
- **Problem:** Zu viel gemeinsamer Zustand führt dazu, dass Agenten auf denselben Ansatz konvergieren -> **Lösung:** Das Lesen von Notizen auf Konsolidierungsphasen beschränken (nicht bei jeder Iteration). Vielfalt der Ansätze ist wertvoll
- **Problem:** Heartbeat-Konsolidierung ist teuer (liest alle Notizen, schreibt neu) -> **Lösung:** Inkrementelle Konsolidierung verwenden – nur Notizen verarbeiten, die neuer sind als der Zeitstempel der letzten Konsolidierung

## Siehe auch {#see-also}

- [[memory-architectures]] – hierarchische Speicherstrukturen
- [[session-persistence]] – Erhalt von Wissen zwischen Sitzungen
- [[temporal-memory]] – Gültigkeitsfenster für gemeinsame Fakten
- [[agent-orchestration]] – Koordination mehrerer Agenten

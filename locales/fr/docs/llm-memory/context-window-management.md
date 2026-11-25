---
title: "Gestion de la fenêtre de contexte"
category: patterns
tags: [llm-memory, context-window, layered-loading, compaction, token-budget, re-injection]
level: 4
source_sha256: 772d0c352dd4449693ca8bce1a9b6716f4398c881f900f4b42bb7cc9daec84fa
translation: machine
translated_at: '2026-10-24'
---
# Gestion de la fenêtre de contexte {#context-window-management}

Stratégies de gestion de ce qui entre dans la fenêtre de contexte du LLM, et du moment où cela y entre. La fenêtre de contexte est une mémoire de travail finie : tout ce que l'agent peut raisonner à un instant donné. Une mauvaise gestion est la principale cause de dégradation des agents sur les tâches longues.

## Faits clés {#key-facts}

- Les fenêtres de contexte vont de 4K à 2M tokens, mais la qualité de l'attention se dégrade au milieu (effet « lost in the middle »)
- Le coût croît linéairement avec la taille du contexte : un contexte de 128K à 3 $/M tokens en entrée coûte 0,38 $ par appel
- La compaction (résumé) est irréversible : une fois résumés, les détails sont perdus de manière définitive
- Le chargement en couches (noyau toujours actif + détails à la demande) maintient le coût de base à environ 170 tokens tout en permettant l'accès à la mémoire complète
- Anxiété de contexte : les agents se mettent à précipiter ou à raccourcir leur travail lorsqu'ils perçoivent que le contexte se remplit, même s'il reste de la place

## Modèle de chargement en couches {#layered-loading-pattern}

Répartissez la mémoire en couches selon leur criticité. Les couches basses sont toujours présentes ; les couches hautes sont chargées à la demande.

```bash
L0 - Identity (~50 tokens)     ← ALWAYS in context
  "You are an assistant for Project X. User is Alice, senior engineer."

L1 - Critical Facts (~120 tokens) ← ALWAYS in context
  "Tech stack: Python 3.12, PostgreSQL 16, deployed on K8s."
  "User prefers: concise answers, code examples, no emojis."

L2 - Topic Memory (variable)    ← Loaded when topic detected
  Retrieved from vector store based on current query.
  Budget: ~2000 tokens per retrieval.

L3 - Full History (variable)    ← Loaded on explicit request
  Complete conversation logs, raw documents.
  Only when agent specifically needs to review past interactions.
```

**Comparaison des coûts :** L0+L1 toujours chargés = ~170 tokens/appel = ~10 $/an. Approche par résumé complet = ~500 $/an. L'approche en couches est 50 fois moins chère.

## Allocation du budget de tokens {#token-budget-allocation}

```python
class TokenBudget:
    def __init__(self, max_tokens: int = 128_000):
        self.allocations = {
            "system_prompt": 0.08,    # 8% - instructions, tool defs
            "identity_l0_l1": 0.02,   # 2% - always-on memory layers
            "state": 0.10,            # 10% - current plan, progress
            "retrieved_memory": 0.15, # 15% - L2 on-demand context
            "conversation": 0.25,     # 25% - recent exchanges
            "tool_results": 0.20,     # 20% - outputs from tools
            "generation": 0.20,       # 20% - reserved for response
        }

    def available(self, category: str) -> int:
        return int(self.max_tokens * self.allocations[category])
```

**Règle empirique :** réservez 20 % pour la génération. Si les résultats d'outils sont volumineux, résumez-les avant de les insérer dans le contexte.

## Stratégies de compaction {#compaction-strategies}

### Résumer puis remplacer {#summarize-and-replace}

Remplacez l'ancien historique de conversation par un résumé compressé :

```python
def compact(messages: list, keep_recent: int = 6) -> list:
    system = messages[0]
    recent = messages[-keep_recent:]
    old = messages[1:-keep_recent]

    if not old:
        return messages

    summary = llm.complete(f"""Summarize preserving:
    1. Key decisions made
    2. Important findings
    3. Failed approaches (DO NOT retry these)
    4. Current state of task
    History: {format_messages(old)}""")

    return [system,
            {"role": "system", "content": f"[Summary of earlier conversation]\n{summary}"},
            *recent]
```

### Fichier d'état + réinitialisation du contexte {#state-file-context-reset}

Pour les tâches longues, privilégiez une réinitialisation complète du contexte plutôt que la compaction. Écrivez l'état dans des fichiers, puis repartez de zéro :

```python
# Before reset
state = {
    "goal": "Migrate API from REST to GraphQL",
    "completed": ["schema design", "resolver stubs", "auth middleware"],
    "current": "pagination implementation",
    "findings": ["cursor pagination is 3x faster than offset for our dataset"],
    "failed": ["relay-style connections - too complex for our use case"],
    "blockers": []
}
save_json(".agent/state.json", state)

# After reset - agent reads state file, continues from where it left off
# No information loss from summarization
```

**Réinitialisation du contexte > compaction** pour les tâches de plus d'environ 30 minutes. La compaction préserve la continuité, mais accumule une perte d'information. Un contexte neuf avec un état explicite est plus propre.

### Réinjection après compaction {#re-injection-after-compaction}

Si la compaction est inévitable, réinjectez immédiatement l'état critique :

```python
def post_compaction_message(state_file: str) -> str:
    state = load_json(state_file)
    return f"""[Context was compacted. Current state:]

## Goal
{state['goal']}

## Completed Steps
{chr(10).join(f'- {s}' for s in state['completed'])}

## Current Step
{state['current']}

## Failed Approaches (DO NOT retry)
{chr(10).join(f'- {f}' for f in state['failed'])}

[Continue from current step. State above is authoritative.]"""
```

## Déclencheurs de sauvegarde automatique {#auto-save-triggers}

Sauvegardez automatiquement l'état de la mémoire à des points clés :

- **Tous les N messages** (par exemple tous les 15 messages) : point de contrôle périodique
- **Avant la compaction** : capturer l'état complet avant une opération avec perte
- **Avant la réinitialisation du contexte** : artefact de passation pour la session suivante
- **Au changement de sujet** : clôturer les conclusions du sujet en cours
- **En cas d'erreur ou d'échec** : consigner ce qui a mal tourné et pourquoi

## Anti-patterns {#anti-patterns}

| Anti-pattern | Problème | Correctif |
|-------------|---------|-----|
| Tout entasser dans le contexte | « Lost in the middle » : le modèle ignore le milieu | Chargement en couches, récupération JIT |
| Absence d'état externe | La compaction détruit les détails critiques | Gestion de l'état basée sur des fichiers |
| Récupération réactive à chaque appel | La latence s'accumule | Pré-chargement au début de la phase de planification |
| Ignorer les coûts en tokens | 3,80 $ pour 10 appels à 128K | Contexte plus court lorsque c'est possible |
| Faire confiance à la sortie de compaction | Les résumés perdent les nuances | Toujours vérifier les faits critiques après compaction |

## Pièges {#gotchas}

- **« Lost in the middle » est mesurable et reproductible.** Les LLM portent fortement attention au début et à la fin du contexte, mais mal au milieu. Placez les informations critiques (tâche en cours, plan, contraintes) au début, et les observations récentes à la fin. N'enfouissez jamais un état important au milieu d'un long historique
- **La compaction perd de l'information de manière irréversible.** Avant de compacter, sauvegardez l'état complet dans des fichiers. Après compaction, réinjectez l'état structuré pour que l'agent sache où il en est. Testez en posant à l'agent des questions sur le travail réalisé avant compaction : s'il ne peut pas répondre, votre réinjection est incomplète
- **La compaction automatique peut boucler.** Si le contexte se remplit rapidement après compaction (par exemple à cause de gros résultats d'outils), l'agent peut entrer dans un cycle compaction-remplissage-compaction. Mettez en place un disjoncteur : après 3 compactions sans progrès, arrêtez et signalez le problème

## Compression du cache KV (2026) {#kv-cache-compression-2026}

Techniques matérielles réduisant l'empreinte mémoire des fenêtres de contexte pendant l'inférence. Elles sont orthogonales à la compression au niveau du prompt : elles agissent au niveau du mécanisme d'attention.

### TriAttention (avril 2026) - SOTA {#triattention-april-2026-sota}

Exploite la découverte que les vecteurs Q/K en pré-RoPE se concentrent autour de centres fixes à travers les têtes d'attention. Utilise des séries trigonométriques pour estimer l'importance des clés sans avoir besoin des requêtes récentes.

```text
How it works:
  1. Trigonometric Series Scoring (S_trig):
     Estimates key importance via Q/K centers + positional distance
     Operates in pre-RoPE space where vectors are stable
     
  2. Norm-Based Scoring (S_norm):
     Complementary signal for low-concentration heads
     
  3. Adaptive Weighting:
     Auto-balances using Mean Resultant Length (R) metric

Results:
  10.7x KV memory reduction matching full attention accuracy (AIME25 40.8%)
  2.5x throughput at equivalent accuracy
  6.3x speedup on MATH 500 (1405 vs 223 tokens/sec)
  RULER retrieval: 66.1 vs SnapKV 55.6

Deployment: vLLM plugin (auto-discovery, zero code changes)
Validated on: Qwen3-8B, DeepSeek-R1-Distill, GPT-OSS-20B, GLM-4.7-Flash
```

Les méthodes précédentes de compression KV (H2O, SnapKV, R-KV) utilisent des « fenêtres d'observation limitées » : seules les requêtes récentes maintiennent des orientations représentatives. TriAttention opère dans l'espace pré-RoPE, où les vecteurs sont intrinsèquement stables, ce qui fournit des signaux d'importance intrinsèques.

### TurboQuant (ICLR 2026) {#turboquant-iclr-2026}

Quantification du cache KV prête pour la production, intégrée à vLLM.

```text
Method: Hadamard rotation + Lloyd-Max scalar quantization + outlier-aware allocation
Effect: bf16 -> packed 4-bit uint8 (4x memory reduction)
Usage: --kv-cache-dtype option in vLLM
Quality: minimal degradation on standard benchmarks
```

### Autres approches de compression {#other-compression-approaches}

| Méthode | Type | Compression | Cas d'usage |
|--------|------|-------------|----------|
| TriAttention | Éviction KV | 10,7x | Inférence, tâches de raisonnement |
| TurboQuant | Quantification KV | 4x | Service en production (vLLM) |
| NVIDIA KVPress | Boîte à outils de compression KV | Variable | Évaluation comparative des stratégies |
| CompLLM | Compression de contexte souple | 2x | Q&R sur long contexte, TTFT accéléré par 4 |
| LoPace | Stockage de prompts sans perte | 4,89x en moyenne | Mise en cache des prompts, pas l'inférence |

### Déploiement en pratique {#practical-deployment}

```text
Strategy for maximum context efficiency:
  1. TurboQuant (4-bit KV cache) - always-on, minimal quality impact
  2. TriAttention (selective eviction) - for reasoning/long context
  3. Both combined: ~40x effective KV compression
  
Hardware requirements:
  TriAttention: tested on A100 80GB, bfloat16
  TurboQuant: any vLLM-supported GPU
  Combined: enables 128K context on consumer GPUs (24GB)
```

## Voir aussi {#see-also}

- [[memory-architectures]]
- [[session-persistence]]
- [[forgetting-strategies]]
- [[context-engineering]]
- [[agent-memory]]
- [[verbatim-vs-extraction]]

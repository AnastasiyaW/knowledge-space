---
title: "Verwaltung des Kontextfensters"
category: patterns
tags: [llm-memory, context-window, layered-loading, compaction, token-budget, re-injection]
level: 4
source_sha256: 772d0c352dd4449693ca8bce1a9b6716f4398c881f900f4b42bb7cc9daec84fa
translation: machine
translated_at: '2026-10-24'
---
# Verwaltung des Kontextfensters {#context-window-management}

Strategien zur Steuerung, welche Inhalte in das Kontextfenster des LLM gelangen und wann. Das Kontextfenster ist ein begrenzter Arbeitsspeicher: alles, was der Agent gleichzeitig berücksichtigen kann. Eine schlechte Verwaltung ist die Hauptursache für nachlassende Leistung von Agenten bei langen Aufgaben.

## Wichtige Fakten {#key-facts}

- Kontextfenster reichen von 4K bis 2M Token, doch die Aufmerksamkeitsqualität nimmt in der Mitte ab („Lost in the middle“-Effekt)
- Die Kosten skalieren linear mit der Kontextgröße: 128K Kontext bei $3/M Input ergeben $0,38 pro Aufruf
- Compaction (Zusammenfassung) ist nicht umkehrbar: Details gehen nach der Zusammenfassung dauerhaft verloren
- Layered Loading (immer geladener Kern + bedarfsgesteuerte Details) hält die Grundkosten bei ca. 170 Token und ermöglicht trotzdem Zugriff auf das vollständige Gedächtnis
- Kontext-Angst: Agenten beginnen zu hetzen und Abkürzungen zu nehmen, sobald sie den Eindruck haben, dass sich der Kontext füllt, auch wenn noch Platz vorhanden ist

## Layered-Loading-Muster {#layered-loading-pattern}

Teile den Speicher nach Kritikalität in Schichten auf. Untere Schichten sind immer vorhanden; höhere Schichten werden bei Bedarf geladen.

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

**Kostenvergleich:** L0+L1 immer geladen = ca. 170 Token pro Aufruf = ca. $10 pro Jahr. Ansatz mit vollständiger Zusammenfassung = ca. $500 pro Jahr. Der Layered-Ansatz ist 50-mal günstiger.

## Verteilung des Token-Budgets {#token-budget-allocation}

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

**Faustregel:** 20 % für die Generierung reservieren. Sind Tool-Ergebnisse groß, fasse sie zusammen, bevor sie in den Kontext eingefügt werden.

## Compaction-Strategien {#compaction-strategies}

### Zusammenfassen und Ersetzen {#summarize-and-replace}

Ersetze den alten Gesprächsverlauf durch eine komprimierte Zusammenfassung:

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

### Zustandsdatei + Kontext-Reset {#state-file-context-reset}

Bei langen Aufgaben ist ein vollständiger Kontext-Reset einer Compaction vorzuziehen. Schreibe den Zustand in Dateien und starte neu:

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

**Kontext-Reset ist besser als Compaction** bei Aufgaben, die länger als ca. 30 Minuten dauern. Compaction erhält zwar die Kontinuität, sammelt aber schrittweise Informationsverluste an. Ein frischer Kontext mit explizitem Zustand ist sauberer.

### Re-Injection nach Compaction {#re-injection-after-compaction}

Ist eine Compaction unvermeidbar, füge den kritischen Zustand sofort erneut ein:

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

## Auto-Save-Auslöser {#auto-save-triggers}

Speichere den Speicherzustand automatisch an wichtigen Punkten:

- **Alle N Nachrichten** (z. B. alle 15 Nachrichten): periodischer Checkpoint
- **Vor der Compaction**: vollständigen Zustand erfassen, bevor eine verlustbehaftete Operation erfolgt
- **Vor dem Kontext-Reset**: Übergabeartefakt für die nächste Sitzung
- **Bei Themenwechsel**: Ergebnisse des aktuellen Themas abschließen
- **Bei Fehler oder Versagen**: festhalten, was schiefging und warum

## Anti-Patterns {#anti-patterns}

| Anti-Pattern | Problem | Lösung |
|-------------|---------|-----|
| Alles in den Kontext stopfen | „Lost in the middle“: Das Modell ignoriert die Mitte | Layered Loading, JIT-Retrieval |
| Kein externer Zustand | Compaction vernichtet kritische Details | Dateibasierte Zustandsverwaltung |
| Reaktives Retrieval bei jedem Aufruf | Latenz summiert sich | Vorab laden zu Beginn der Planungsphase |
| Token-Kosten ignorieren | $3,80 pro 10 Aufrufe bei 128K | Kürzerer Kontext, wo möglich |
| Compaction-Ausgabe blind vertrauen | Zusammenfassungen verpassen Nuancen | Kritische Fakten nach der Compaction immer prüfen |

## Fallstricke {#gotchas}

- **„Lost in the middle“ ist messbar und konsistent.** LLMs achten stark auf Anfang und Ende des Kontexts, in der Mitte aber nur schwach. Platziere kritische Informationen (aktuelle Aufgabe, Plan, Randbedingungen) am Anfang und aktuelle Beobachtungen am Ende. Vergrabe wichtigen Zustand niemals mitten in einem langen Verlauf
- **Compaction verliert Informationen unwiderruflich.** Speichere vor der Compaction den vollständigen Zustand in Dateien. Füge nach der Compaction den strukturierten Zustand erneut ein, damit der Agent weiß, wo er steht. Teste dies, indem du den Agenten Fragen zur Arbeit vor der Compaction stellst. Kann er sie nicht beantworten, ist deine Re-Injection unvollständig
- **Auto-Compact kann in Schleifen geraten.** Füllt sich der Kontext nach einer Compaction schnell wieder (z. B. durch große Tool-Ausgaben), kann der Agent in einen Zyklus aus Compact, Refill und erneutem Compact geraten. Richte einen Circuit Breaker ein: Nach 3 Compactions ohne Fortschritt anhalten und Bericht erstatten

## KV-Cache-Kompression (2026) {#kv-cache-compression-2026}

Hardwarenahe Techniken zur Reduktion des Speicherbedarfs von Kontextfenstern während der Inferenz. Sie sind orthogonal zur Kompression auf Prompt-Ebene und wirken auf der Ebene des Aufmerksamkeitsmechanismus.

### TriAttention (April 2026): SOTA {#triattention-april-2026-sota}

Nutzt die Erkenntnis, dass sich Q/K-Vektoren vor RoPE über Attention-Heads hinweg um feste Zentren konzentrieren. Verwendet trigonometrische Reihen, um die Wichtigkeit von Keys abzuschätzen, ohne auf aktuelle Queries angewiesen zu sein.

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

Frühere KV-Kompressionsverfahren (H2O, SnapKV, R-KV) arbeiten mit „begrenzten Beobachtungsfenstern“: Nur aktuelle Queries behalten eine repräsentative Ausrichtung. TriAttention arbeitet im Raum vor RoPE, in dem die Vektoren von Natur aus stabil sind, und liefert dadurch intrinsische Wichtigkeitssignale.

### TurboQuant (ICLR 2026) {#turboquant-iclr-2026}

Produktionsreife KV-Cache-Quantisierung, integriert in vLLM.

```text
Method: Hadamard rotation + Lloyd-Max scalar quantization + outlier-aware allocation
Effect: bf16 -> packed 4-bit uint8 (4x memory reduction)
Usage: --kv-cache-dtype option in vLLM
Quality: minimal degradation on standard benchmarks
```

### Weitere Kompressionsansätze {#other-compression-approaches}

| Methode | Typ | Kompression | Anwendungsfall |
|--------|------|-------------|----------|
| TriAttention | KV-Eviction | 10,7x | Inferenz, Reasoning-Aufgaben |
| TurboQuant | KV-Quantisierung | 4x | Produktiver Betrieb (vLLM) |
| NVIDIA KVPress | KV-Kompressions-Toolkit | Variabel | Benchmarking von Strategien |
| CompLLM | Weiche Kontext-Kompression | 2x | Long-Context-Q&A, 4x TTFT-Beschleunigung |
| LoPace | Verlustfreie Prompt-Speicherung | 4,89x im Mittel | Prompt-Caching, nicht Inferenz |

### Praktischer Einsatz {#practical-deployment}

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

## Siehe auch {#see-also}

- [[memory-architectures]]
- [[session-persistence]]
- [[forgetting-strategies]]
- [[context-engineering]]
- [[agent-memory]]
- [[verbatim-vs-extraction]]

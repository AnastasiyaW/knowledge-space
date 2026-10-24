---
title: "KV-Cache-Komprimierung und Speicherkontrolle"
description: "KV-Cache-Strategien für LLM-Inferenz messen, auswählen und validieren, ohne sich auf Benchmark-Folklore zu verlassen."
tags: [llm-agents, kv-cache, inference, memory-optimization, long-context, serving]
level: 5
source_sha256: 523aded393e40949109d66a23d56108db76c45c74da097692bbc3cd32d0dc914
translation: machine
translated_at: '2026-10-24'
---
# KV-Cache-Komprimierung und Speicherkontrolle (September 2026) {#kv-cache-compression-and-memory-control-september-2026}

Versionskontext: Cache-Layouts und unterstützte Strategien hängen von Modellarchitektur, Framework, Backend, Präzision und Serving-Engine ab. Verwenden Sie die Dokumentation und Telemetrie für die exakt eingesetzte Kombination. Diese Seite verzichtet auf allgemeingültige Kompressionsverhältnisse und Leistungsaussagen.

Ein Key-Value-Cache speichert Attention-Keys und -Values bereits verarbeiteter Tokens, damit die autoregressive Dekodierung sie nicht bei jedem Generierungsschritt neu berechnen muss. Er verbessert die Effizienz der Dekodierung, doch der dafür vorgehaltene Cache-Speicher kann bei langen Kontexten oder gleichzeitigen Anfragen zur limitierenden Ressource werden.

## Was die Cache-Größe bestimmt {#what-determines-cache-size}

Für ein Decoder-only-Modell mit konventioneller Attention ergibt sich als Planungsschätzung:

```text
bytes ≈ 2 × layers × batch_size × retained_tokens
        × num_kv_heads × head_dim × bytes_per_element
```

Der Faktor zwei steht für Keys und Values. Grouped-Query- oder Multi-Query-Attention kann weniger Key/Value-Heads als Query-Heads verwenden, daher sollte die tatsächliche Anzahl der KV-Heads des Modells eingesetzt werden. Encoder-Decoder-Modelle, Sliding-Window-Attention, Linear-Attention und modellspezifische Cache-Implementierungen können ein anderes Layout verwenden.

```python
def estimate_kv_cache_bytes(
    *,
    num_layers: int,
    batch_size: int,
    retained_tokens: int,
    num_kv_heads: int,
    head_dim: int,
    bytes_per_element: int,
) -> int:
    return (
        2
        * num_layers
        * batch_size
        * retained_tokens
        * num_kv_heads
        * head_dim
        * bytes_per_element
    )
```

Betrachten Sie dies als Kapazitätsplanung, nicht als Allokationsnachweis. Framework-Overhead, Attention-Kernels, Fragmentierung, Präfix-Wiederverwendung, Graph-Capture und Parallelisierung verbrauchen ebenfalls Speicher.

## Vor der Komprimierung diagnostizieren {#diagnose-before-compressing}

Erheben Sie ein Workload-Profil, bevor Sie eine Strategie wählen:

| Signal | Warum es wichtig ist |
|---|---|
| Verteilung der Input- und generierten Tokens | Bestimmt die vorgehaltene Sequenzlänge |
| Gleichzeitig aktive Sequenzen | Vervielfacht die Cache-Allokation |
| Prefill- versus Decode-Latenz | Trennt Engpässe bei Prompt-Verarbeitung und Token-Generierung |
| Cache-Hit-/Wiederverwendungsrate | Zeigt, ob gemeinsame Präfixe wertvoll sind |
| GPU-Speicher, OOMs, Fragmentierung | Entscheidet, ob Speicher die eigentliche Einschränkung ist |
| Qualität bei der Zielkontextlänge | Erkennt Regressionen bei langen Kontexten |
| Mandanten-/Datenbereich | Verhindert unsichere Cache-Wiederverwendung |

Stimmen Sie einen Cache nicht auf einem kurzen synthetischen Prompt ab und deployen Sie ihn dann nicht auf einen Workload mit langen Dokumenten oder mehreren Nutzern.

## Cache-Strategie nach Randbedingung wählen {#choose-a-cache-strategy-by-constraint}

| Strategie | Geeignet, wenn | Abwägung |
|---|---|---|
| Dynamischer Cache | Sequenzlängen schwanken und Einfachheit zählt | Wachsende Allokation und weniger vorhersagbare Shapes |
| Statischer/vorallokierter Cache | Maximale Länge ist bekannt und das Framework unterstützt es | Reservierter Speicher kann verschwendet werden oder zu OOMs führen |
| Sliding-Window-Cache | Modell und Aufgabe tolerieren begrenzten jüngsten Kontext | Älterer Kontext steht der Attention nicht mehr zur Verfügung |
| Ausgelagerter Cache (Offloading) | Gerätespeicher ist knapp und das Latenzbudget erlaubt Transfers | Host-/Device-Transfers können die Latenz dominieren |
| Quantisierter Cache | Speicher ist der Engpass und Modell/Backend unterstützen es | Aufgabenspezifische Genauigkeit und Kernel-Verhalten müssen gemessen werden |
| Paged-/Block-verwalteter Serving-Cache | Viele gleichzeitige Sequenzen mit ungleichmäßigen Längen | Engine-spezifisches Betriebs-Tuning |
| Präfix-Cache | Viele Anfragen teilen ein identisches, unveränderliches Präfix | Erfordert exakte Cache-Schlüssel und Isolationsmechanismen |

Hugging Face dokumentiert dynamische, statische, ausgelagerte und quantisierte Cache-Varianten. Eine Serving-Engine kann einen Block- oder Page-Allokator statt eines einzelnen zusammenhängenden Tensors verwenden. Wählen Sie die Implementierung, die vom eingesetzten Modell und Backend unterstützt wird, und kopieren Sie keine Flags aus einer fremden Engine.

## Statischer Cache und compile-freundliche Shapes {#static-cache-and-compile-friendly-shapes}

Ein statischer Cache reserviert Speicher für eine maximale Cache-Länge im Voraus. In kompatiblen Transformers-Konfigurationen kann er eine compile-freundliche Ausführung ermöglichen, hebt aber die Untergrenze des Speicherbedarfs an.

```python
generation = model.generate(
    **inputs,
    cache_implementation="static",
    max_new_tokens=256,
)
```

Legen Sie das Maximum anhand beobachteter Anfragelimits plus einer begründeten Reserve fest. Ein großes, willkürliches Maximum verwandelt eine Optimierung in ein Out-of-Memory-Risiko. Führen Sie vor dem Einsatz im Serving-Traffic einen isolierten Dauertest mit der vorgesehenen Concurrency durch.

## Präfix-Wiederverwendung ist eine Datengrenze {#prefix-reuse-is-a-data-boundary}

Präfix-Wiederverwendung kann das erneute Berechnen eines gemeinsamen System-Prompts, eines Dokumentpräfixes oder eines geteilten Kontexts vermeiden. Sie ist nur sicher, wenn der Cache-Schlüssel jede verhaltensrelevante Eingabe enthält:

```json
{
  "model_revision": "immutable-model-revision",
  "tokenizer_revision": "tokenizer:sha256:...",
  "chat_template_revision": "template:sha256:...",
  "system_prompt_revision": "prompt:sha256:...",
  "tenant_scope": "tenant_42",
  "tool_schema_revision": "tools:sha256:..."
}
```

Verwenden Sie gecachten Zustand niemals mandantenübergreifend, nutzerübergreifend, über Berechtigungsbereiche oder Prompt-Revisionen hinweg, sofern die Richtlinie genau diese Grenze nicht ausdrücklich erlaubt. Cache-Invalidierung ist hier ein Korrektheits- und Datenschutzthema, nicht nur ein Performance-Thema.

## Quantisierung und Komprimierung {#quantization-and-compression}

Quantisierte Caches verringern die Bytes pro gespeichertem Wert. Die geeignete Präzision hängt von Modell, Attention-Architektur, Implementierung, Kontextlänge und Aufgabe ab. Ein speichersparenderer Cache kann die Concurrency verbessern, zugleich aber Retrieval, strukturierte Ausgaben oder Schlussfolgerungen bei längeren Kontexten verschlechtern.

Validieren Sie Kandidaten mit:

1. einer festen Verteilung von Prompts und generierten Tokens;
2. repräsentativen Fällen mit langem Kontext und Retrieval;
3. Prüfungen von strukturierter Ausgabe und Tool-Nutzung;
4. einem Qualitätsvergleich gegen die freigegebene Baseline;
5. Peak-Speicher, p50/p95-Latenz, Durchsatz und Fehlerrate;
6. einer Rollback-Bedingung, falls Qualität oder OOM-Rate einen Schwellenwert überschreiten.

Forschungsarbeiten zur Komprimierung können Kandidaten vorschlagen, Paper-Zahlen sind aber kein Kapazitätsplan für den Produktivbetrieb.

## Serving-Betrieb {#serving-operations}

Trennen Sie zwei Belange:

```text
per-request correctness: prompt, cache key, context limit, output validation
system capacity: batching, allocator pressure, memory headroom, admission control
```

Bei einem Dienst für mehrere Nutzer muss die Zugangskontrolle die Cache-Kapazität berücksichtigen, bevor sie eine Anfrage annimmt. Eine Anfrage mit einem expliziten Kapazitätsstatus abzulehnen oder einzureihen ist sicherer, als sie anzunehmen und nach teilweiser Arbeit scheitern zu lassen. Exportieren Sie Cache-Speicher, aktive Sequenzen, Hits/Misses, Evictions, OOMs und Latenz als Observability-Signale.

## Verifikationsnachweis {#verification-receipt}

```json
{
  "candidate": "cache-strategy-revision",
  "model_revision": "immutable-model-revision",
  "workload_revision": "eval:sha256:...",
  "context_distribution": "production-like-v3",
  "quality_gate": "no material regression",
  "capacity_gate": "no OOM at approved concurrency",
  "rollback": "dynamic-cache-baseline"
}
```

Ein Nachweis macht deutlich, ob ein Ergebnis für das vorgesehene Modell, die Engine, den Workload und die Hardware gilt. Führen Sie ihn erneut aus, nachdem Modellgewichte, Tokenizer, Kontextrichtlinie, Kernel/Backend oder Serving-Engine geändert wurden.

## Fallstricke {#gotchas}

- **Die Anzahl der KV-Heads entspricht nicht immer der Anzahl der Attention-Heads.** GQA und MQA verändern die Speicherberechnung. **Abhilfe:** Lesen Sie die tatsächliche Modellkonfiguration, bevor Sie die Kapazität schätzen.
- **Statische Allokation kann schon vor dem ersten Token scheitern.** Ein großes Maximum reserviert Speicher selbst für kleine Anfragen. **Abhilfe:** Dimensionieren Sie es anhand eines gemessenen Limits und testen Sie die Concurrency.
- **Ein Cache-Schlüssel kann versehentlich eine Datengrenze überschreiten.** Ähnlich aussehende Prompts können sich in Mandant, Tools oder Berechtigungen unterscheiden. **Abhilfe:** Nehmen Sie Revisionen und Bereich in den Schlüssel auf und verweigern Sie bei einer Abweichung den Zugriff (Fail-Closed).
- **Die Gewinne durch Quantisierung hängen von der Aufgabe ab.** Ein Cache, der die Perplexität bei kurzen Texten erhält, kann beim Retrieval mit langem Kontext versagen. **Abhilfe:** Validieren Sie die Zielaufgaben bei der eingesetzten Kontextlänge.
- **Caching ist ein Inferenzmechanismus.** Eine Aktivierung im Training kann zu unerwartetem Verhalten führen. **Abhilfe:** Folgen Sie der Trainingsanleitung des Frameworks und halten Sie Trainings- und Serving-Konfigurationen getrennt.

## Quellen {#sources}

- [Hugging Face cache strategies](https://huggingface.co/docs/transformers/main/kv_cache)
- [Hugging Face cache explanation](https://huggingface.co/docs/transformers/v5.12.0/cache_explanation)
- [Hugging Face inference optimization](https://huggingface.co/docs/transformers/main/llm_optims)
- [vLLM documentation](https://docs.vllm.ai/en/latest/)
- [Transformers generation utilities](https://huggingface.co/docs/transformers/internal/generation_utils)

## Siehe auch {#see-also}

- [[model-optimization]]
- [[token-optimization]]
- [[production-patterns]]
- [[transformer-architecture]]
- [[llm-api-integration]]
- [[ollama-local-llms]]

---
title: "Transformer-Architektur"
description: "Ein praxisnaher, versionsbewusster Leitfaden zur Struktur von aufmerksamkeitsbasierten Transformern, zur autoregressiven Dekodierung, zu Positionsinformationen und zu den Grenzen der Produktionskonfiguration."
tags: [llm-agents, transformers, attention, deep-learning, architecture, inference]
level: 5
source_sha256: 8fc965ee099315ace179198deee48708dd6d86bd3ca3f7ac1d1e687fc6cb470f
translation: machine
translated_at: '2026-10-24'
---
# Transformer-Architektur (September 2026) {#transformer-architecture-september-2026}

Versionskontext: Transformer-Familien, Positionskodierungen, Attention-Kernel, Tokenizer-Verhalten, Kontextlimits und Cache-Implementierungen variieren je nach Modellversion. Diese Seite erklärt stabile Architekturprinzipien; sie trifft keine dauerhafte Aussage über die inneren Abläufe oder die maximale Kontextlänge eines bestimmten Modells.

Das Transformer-Paper von 2017 stellte eine Sequenz-zu-Sequenz-Architektur vor, die auf Attention statt auf Rekurrenz oder Faltung beruht. Das ursprüngliche Design verwendet eine Encoder-Decoder-Struktur, und Attention verbindet beide Teile. [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

## Die zentrale Berechnung {#the-core-computation}

Ein Transformer verarbeitet Token-Repräsentationen. Für eine Attention-Schicht leiten gelernte Projektionen aus diesen Repräsentationen Queries (`Q`), Keys (`K`) und Values (`V`) ab:

```text
Attention(Q, K, V) = softmax((Q × Kᵀ) / sqrt(d_k)) × V
```

Für jede Query-Position wählen die Attention-Gewichte Value-Vektoren aus erlaubten Key-Positionen aus und kombinieren sie. Das genaue Projektionslayout, die Anzahl der Heads, die Reihenfolge der Normalisierung, die Aktivierungsfunktion und der numerische Kernel sind modellspezifische Implementierungsentscheidungen.

Multi-Head-Attention führt mehrere Attention-Projektionen parallel aus und kombiniert sie anschließend. Dadurch erhält eine Schicht mehrere Repräsentationsunterräume; es handelt sich nicht um eine wörtliche Liste unabhängiger, für Menschen lesbarer "Themen".

## Drei gängige architektonische Familien {#three-common-architectural-families}

| Familie | Attention-Muster | Typische Ausgaberolle | Wichtige Grenze |
|---|---|---|---|
| Nur Encoder | Token greifen über die zulässige Eingabe hinweg aufeinander zu | kontextuelle Repräsentationen | kann nicht als autoregressive Antwortgenerierung vorausgesetzt werden |
| Nur Decoder | jedes Token ist gegenüber zukünftigen Tokens maskiert | Generierung des nächsten Tokens | Inferenz erzeugt Tokens sequenziell |
| Encoder-Decoder | Decoder-Self-Attention plus Cross-Attention auf die kodierte Eingabe | bedingte Generierung | Quell-Repräsentation und erzeugte Sequenz haben unterschiedliche Rollen |

Dies sind Muster, keine Produktrangliste. Die passende Wahl hängt von Trainingsziel, bereitgestelltem Modellvertrag, Tool-Verhalten und Evaluationsergebnissen ab.

## Reihenfolge, Masken und Position {#order-masks-and-position}

Attention allein gibt einer Sequenzposition keine inhärente Reihenfolge. Ein Transformer fügt daher Positionsinformationen hinzu oder stellt sie anderweitig dar. Das ursprüngliche Paper verwendet Positionskodierungen; spätere Modellfamilien nutzen andere Positionsmechanismen. Das Positionsschema sollte als Teil der aufgelösten Modellkonfiguration betrachtet werden.

Masken legen fest, welche Positionen auf welche anderen zugreifen dürfen:

- **Kausale Maske:** verhindert, dass eine Decoder-Position zukünftige generierte Tokens liest;
- **Padding- bzw. Attention-Maske:** verhindert, dass ungültige oder fehlende Positionen einfließen;
- **Cross-Attention-Maske:** beschränkt, welche Quellpositionen ein Decoder heranziehen darf.

Eine fehlerhafte Maske kann dazu führen, dass ein System in einer Demo funktioniert, während es bei der Evaluation zukünftige Labels preisgibt oder Datensätze innerhalb eines Batches vermischt.

## Training und autoregressive Generierung unterscheiden sich {#training-and-autoregressive-generation-differ}

Beim Training können Implementierungen unter Berücksichtigung der Modellmaske häufig viele Sequenzpositionen parallel auswerten. Bei der Generierung im Decoder-Stil hängt Token `t + 1` vom Zustand nach Token `t` ab, sodass jedes neue Token den Zustand der Anfrage fortschreibt.

Inferenzimplementierungen können frühere Key/Value-Projektionen in einem Cache behalten, um das gesamte Präfix nicht erneut berechnen zu müssen. Der Cache ist eine Optimierung mit einer strikten Isolationsanforderung: Er muss an die Anfrage, die Revision von Modell bzw. Konfiguration sowie die jeweils gültige Mandanten- bzw. Datengrenze gebunden sein. Schließen Sie das Cache-Verhalten oder die Kapazität nicht aus einem Modellnamen ab. [Hugging Face KV-Cache-Leitfaden](https://huggingface.co/docs/transformers/main/en/kv_cache)

## Ein praktischer Modellvertrag {#a-practical-model-contract}

Eine Anwendung sollte die transformerbezogene Konfiguration erfassen, die das Verhalten verändert:

```json
{
  "model_key": "approved-generation-model",
  "resolved_model_revision": "observed-at-runtime",
  "tokenizer_revision": "recorded-at-deploy",
  "context_policy_revision": "context@8",
  "attention_or_position_config": "provider-or-local-reference",
  "inference_cache_policy": "per-request-v2",
  "output_contract": "answer-with-citations/v3"
}
```

Für die Reproduzierbarkeit ist dies nützlicher als eine Aussage in Fließtext wie "verwendet einen Transformer". Ein Modellalias kann einen geänderten Tokenizer, ein verändertes Kontextverhalten oder eine andere Kernel-Implementierung verbergen.

## Performance ist ein Evaluationsproblem {#performance-work-is-an-evaluation-problem}

Attention-Kosten, Speicherbedarf, Batching, Quantisierung und Cache-Strategie können Latenz und Qualität beeinflussen. Optimieren Sie nur mit einer repräsentativen Last und einer aufgabenbezogenen Abnahmesuite.

Messen Sie:

- Latenz der Anfrage und Latenz der generierten Tokens getrennt;
- Speicherspitzen und Parallelität bei der vorgesehenen Kontextmischung;
- Aufgabenqualität, Abdeckung von Quellenangaben und Gültigkeit strukturierter Ausgaben;
- Fehler-, Timeout- und Wiederholungsraten;
- Cache-Treffer- bzw. Wiederverwendungssignale nur dort, wo die Laufzeitumgebung sie bereitstellt;
- Isolations- und Abbruchverhalten bei gleichzeitigen Anfragen.

Die Dokumentation zu `MultiheadAttention` in PyTorch ist eine nützliche Implementierungsreferenz, doch ein Framework-Primitiv definiert nicht die Architektur jedes eingesetzten Modells. [PyTorch MultiheadAttention](https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)

## Fallstricke {#gotchas}

- **"Paralleler Transformer" bedeutet nicht parallele Antwortgenerierung.** Die Generierung im Decoder-Stil schreitet weiterhin Token für Token voran. **Abhilfe:** Messen Sie die Ende-zu-Ende-Latenz im tatsächlich eingesetzten Workflow, nicht nur einen trainingsähnlichen Kernel.
- **Eine Maske ist eine Korrektheitsgrenze.** Eine umgekehrte oder fehlende Maske kann zukünftigen oder unzusammengehörigen Kontext preisgeben. **Abhilfe:** Testen Sie Masken mit adversariellen Fällen und Fällen über mehrere Datensätze hinweg.
- **Token-Position ist kein Zeichenversatz.** Tokenisierung, Kürzung und Positionsbehandlung können verändern, was das Modell tatsächlich erhält. **Abhilfe:** Erfassen Sie Revisionen von Tokenizer und Kontextrichtlinie zusammen mit dem Release.
- **KV-Caches sind kein gemeinsam genutzter Speicher.** Ein zu breit angelegter Cache-Schlüssel kann Anfragen oder Richtliniengrenzen überschreiten. **Abhilfe:** Beschränken Sie die Wiederverwendung auf die exakt freigegebene Konfiguration und Identitätsgrenze.
- **Attention-Gewichte sind kein Erklärungsnachweis.** Sie sind Modellberechnungen, keine kausale Prüfspur für eine geschäftliche Entscheidung. **Abhilfe:** Bewahren Sie Quellenangaben, Validatoren und explizite Entscheidungsbelege auf.

## Quellen {#sources}

- [Vaswani et al., Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [PyTorch MultiheadAttention](https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
- [Hugging Face KV-Cache-Leitfaden](https://huggingface.co/docs/transformers/main/en/kv_cache)

## Siehe auch {#see-also}

- [[tokenization]]
- [[kv-cache-compression]]
- [[llm-api-integration]]
- [[context-engineering]]
- [[model-optimization]]
- [[scaling-laws-and-benchmarks]]

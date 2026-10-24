---
title: "SIQ-1-35B — Öffentliches Modell und Demo"
category: projects
date: 2026-06-17
tags: [project, public-model-and-demo, siq-1-35b, siq_1_35b]
aliases: ["SIQ-1-35B"]
level: 3
source_sha256: 298e53c09186b395cb61bd1f7f411307c697c973cfa691b4a15fbf5b0af399c5
translation: machine
translated_at: '2026-10-24'
---
der Sprache und Wording: keine @@CODE-Platzhalter vorhanden. Achte auf Links: Link-Texte übersetzen, Ziele unverändert. Tabellenköpfe übersetzen. YAML: title und description übersetzen, sonst unverändert; description fehlt, also nur title.

---
title: SIQ-1-35B — Öffentliches Modell und Demo
category: projects
date: 2026-06-17
tags: [project, public-model-and-demo, siq-1-35b, siq_1_35b]
aliases: ["SIQ-1-35B"]
---

# SIQ-1-35B — Öffentliches Modell und Demo {#siq-1-35b-public-model-and-demo}

**Entwicklungslinie:** `project:siq-1-35b` · Strang `public-model-and-demo`  
**Letztes Ereignis:** 2026-06-17 · 1 datiertes Ereignis seit 2026-06-17 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

SIQ-1-35B — ein Apache-2.0-Finetune von Qwen/Qwen3.6-35B-A3B für lokales Programmieren, Schlussfolgern und Tool-Nutzung.

- Chat-Modi mit und ohne Thinking
- BF16- und GGUF-Distributionen
- Lokales, OpenAI-kompatibles Serving

## Entwicklungslinie {#development-line}

- **2026-06-17 — Das öffentliche Modell SIQ-1-35B und die Agenten-Demo wurden verknüpft.** Am 2026-06-17 wurde SIQ-1-35B mit einer öffentlichen Hugging-Face-Modellseite und einem Hermes-Agent-ZeroGPU-Space verknüpft. Daneben wurden Autoresearch-, Parameter-Golf- und Benchmark-Repositories verlinkt. Die Links bestätigen die öffentlichen Dateien, nicht aber die Benchmark-Behauptungen des Autors.

## Was sich geändert hat {#what-changed}

2026-06-17 — Die Modellkarte benannte SIQ-1-35B in „SIQ-1-tiny-35b“ um. Das Modell wird dort als universeller Agent für Autoresearch, Programmieren und Schlussfolgern dargestellt. Das Update fügte Benchmark-Diagramme, Serving-Profile, Prompts und einen Demo-Link hinzu, ohne dass an diesem Tag ein Gewichts-Upload verzeichnet ist.

## Anwendung {#how-to-use-this}

Ab 2026-06-17 ist SIQ-1-35B als öffentliches Modell mit Agenten-Demo zu behandeln. Fähigkeiten und Benchmark-Behauptungen sind vor einer Verwendung unabhängig zu prüfen.

1. Mit der lokalen Q4_K_M-GGUF beginnen: `llama serve -hf AlexWortega/SIQ-1-35B:Q4_K_M`, danach den OpenAI-kompatiblen Endpunkt auf localhost verwenden.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
2. Für Tool-Aufrufe und Thinking das dokumentierte llama.cpp-Profil mit `--jinja`, GPU-Offload und einem Kontext von 131072 Token, aufgeteilt auf vier Slots, verwenden.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
3. Für BF16-Serving die dokumentierte SGLang-Konfiguration mit Tensor-Parallelism 2 sowie den Qwen3-Parsern für Reasoning und Tool-Calls verwenden.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
4. Für anspruchsvolles Schlussfolgern `enable_thinking=true`, `Reasoning effort: high` und Temperatur 0 setzen. Für direkte Antworten Thinking deaktivieren.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
5. Vor dem Aktivieren von MTP-Speculative-Decoding die aktuelle Begleit-GGUF abrufen und prüfen, ob sie mit der gewählten Trunk-Quantisierung geladen werden kann.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B/commit/cb6f95ec76411517babbfa6a854f7f0425313ff4>

## Best Practices {#best-practices}

- `--jinja` bei llama.cpp aktiviert lassen: Die dokumentierte Qwen-Chat-Vorlage enthält die Tags für Thinking und Tool-Aufrufe.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
- Benchmark-Ergebnisse mit Präzision, Prompt-Modus und Sampling-Einstellungen angeben; die Karte unterscheidet die gemeinsame Messung für Q4 vom BF16-Ergebnis.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
- MTP als versionsabhängig behandeln: Das Begleitmodell wurde am 2026-06-23 nach einer fehlerhaften Draft-Schicht korrigiert, und Nutzer hatten zuvor über Ladefehler berichtet.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B/discussions/2>
- Bis zur Wiederherstellung eine lokale Laufzeitumgebung statt der gehosteten ZeroGPU-Demo verwenden; beim Abruf meldete sie einen Laufzeitfehler wegen fehlender `libcuda.so.1`.
  — <https://huggingface.co/spaces/AlexWortega/hermes-agent-zerogpu>
- Den Ein-A6000-Zwei-Stunden-Test der Karte nicht als offizielles Parameter-Golf-Leaderboard-Ergebnis darstellen; dieses Projekt beschränkt Leaderboard-Einreichungen auf zehn Minuten auf 8×H100.
  — <https://github.com/openai/parameter-golf>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-06-17 — Das Modell ist ein `finetune`, kein Adapter. Die Release-Historie korrigiert diese Beziehung ausdrücklich.
- 2026-06-23 — Frühere, nur mit Vokabular ausgestattete DFlash- und fehlerhafte MTP-Begleitmodelle sind veraltet; das Repository ersetzte sie durch die MTP-Schicht von Qwen3.6-35B-A3B und aktualisierte die Tensornamen.

## Noch unbekannt {#still-unknown}

- Unabhängige Evaluierungen der SIQ-Behauptungen fehlen. GPQA-, Autoresearch-, Programmier- und BullshitBench-Werte sind als vom Autor berichtet zu behandeln.
- SIQ-1-35B ist der Repository-Name, während die Karte vom 2026-06-17 dasselbe Modell als SIQ-1-tiny-35b bezeichnet. Die Commit-Historie zeigt keine separaten Modellidentitäten.
- Karpathy autoresearch und OpenAI Parameter Golf verwenden unterschiedliche Trainings- und Evaluierungsaufbauten. Die Quellen zeigen keine direkte Herkunft der Trainingsdaten von SIQ-1-35B.
- SIQ ist als Textgenerierung markiert, obwohl seine Qwen3.6-Basis multimodal ist. Die Modellkarte bestätigt keine Unterstützung für Bildeingaben.
- Der Ausfall des gehosteten ZeroGPU ist ein Problem der gehosteten Laufzeitumgebung und kein Beleg dafür, dass lokales GGUF- oder BF16-Serving fehlschlägt.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://huggingface.co/AlexWortega/SIQ-1-35B | AlexWortega/SIQ-1-35B Modellkarte | 2026-09-05 |
| https://huggingface.co/AlexWortega/SIQ-1-35B/commits/d6a09a9f86bf21d60db5b575578a1df47d222adf/README.md | SIQ-1-35B README-Commit-Historie | 2026-09-05 |
| https://huggingface.co/AlexWortega/SIQ-1-35B/commits/cb6f95ec76411517babbfa6a854f7f0425313ff4 | SIQ-1-35B Repository-Commit-Historie bis zur MTP-Korrektur | 2026-09-05 |
| https://huggingface.co/AlexWortega/SIQ-1-35B/commit/cb6f95ec76411517babbfa6a854f7f0425313ff4 | Commit „Correct MTP layer from Qwen3.6-35B-A3B“ | 2026-09-05 |
| https://huggingface.co/AlexWortega/SIQ-1-35B/discussions/2 | SIQ-1-35B MTP-Ladediskussion | 2026-09-05 |
| https://huggingface.co/spaces/AlexWortega/hermes-agent-zerogpu | Hermes · SIQ-1-35B ZeroGPU Space | 2026-09-05 |
| https://github.com/karpathy/autoresearch | karpathy/autoresearch | 2026-09-05 |
| https://github.com/openai/parameter-golf | openai/parameter-golf | 2026-09-05 |
| https://github.com/petergpt/bullshit-benchmark | BullshitBench v2 | 2026-09-05 |

## Agenten-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:siq-1-35b`, Strang `public-model-and-demo`, 1 datiertes Ereignis 2026-06-17 → 2026-06-17.
- **Praktischer Hinweis:** Ab 2026-06-17 ist SIQ-1-35B so zu behandeln, dass es ein verlinktes öffentliches Modellartefakt und einen Einstiegspunkt für eine Agenten-Demo hat; Fähigkeiten und Benchmark-Behauptungen sind vor einer Verwendung unabhängig zu prüfen.
- **Konfidenz:** mittel. Die datierten Überholungshinweise oben sind maßgeblich dafür, was veraltet ist.

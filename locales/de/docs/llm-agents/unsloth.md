---
title: "Unsloth"
description: "Artefaktbewusste Referenz für Unsloth Core, Studio, Desktop und versionsgebundene Hinweise zum Fine-Tuning."
level: 3
source_sha256: 2c9fb5a93260e2b66b6f772cad435351180aaffcb6835ecf37295c4cfc1c8fa0
translation: machine
translated_at: '2026-10-24'
---
# Unsloth {#unsloth}

Unsloth ist eine Familie lokaler Oberflächen für Fine-Tuning und Inferenz. Core-Bibliothek/Rezepte, Studio und Desktop sind verwandte Produkte, aber keine austauschbaren Laufzeitumgebungen. Status geprüft anhand offizieller englischer und chinesischer Quellen am **2026-08-27**.

## Übersicht der aktuellen Oberflächen {#current-surface-map}

| Oberfläche | Rolle | Aktuelle Abgrenzung |
|---|---|---|
| Unsloth Core/Bibliothek | Python-Integration für Training und Inferenz | Für Skript- und Notebook-Workflows verwenden und Paket sowie Modellrezept fixieren |
| Unsloth Studio | Lokale UI/Workflow-Oberfläche | Nicht dieselbe Installation, denselben Funktionsumfang oder denselben Release-Rhythmus wie Core voraussetzen |
| Unsloth Desktop | Desktop-Installer für Windows, macOS und Linux | Mit der Release-Linie vom 2026-08-13 eingeführt; aktuelle Releases müssen separat geprüft werden |
| Modellspezifische Anleitungen | Fine-Tuning-Einstellungen und Kompatibilität | Einstellungen gelten nur für die genannte Modellfamilie und Revision der Anleitung |

Die offizielle Release-Seite zeigte am 2026-08-25 `v0.1.803-beta`. Das Repository dokumentiert CPU- und Multi-GPU-Pfade für NVIDIA, AMD, Intel und Mac, die Unterstützungstiefe variiert jedoch je nach Betriebssystem, Backend, Modell und Workflow.

## Entwicklungsverlauf {#development-history}

| Datum | Strang | Ereignis | Zeitlicher Status |
|---|---|---|---|
| 2025-08-11 | Anleitungen zum Modelltraining | GPT-OSS-Fine-Tuning-Hinweise gemeldet | Historisch; vor Gebrauch die aktuelle Anleitung abrufen |
| 2026-03-11 | Anleitungen zum Modelltraining | Fine-Tuning-Hinweise für Qwen3.5 gemeldet | Aktuelle Familienanleitung; Einstellungen bleiben modellgrößenspezifisch |
| 2026-04-08 | Lokale UI | Lokaler Workflow-Bericht zu Studio/Gemma | Historischer Produktzweig |
| 2026-08-13 | Lokale UI | Unsloth Desktop eingeführt | Aktueller Produktzweig |
| 2026-08-25 | Release-Linie | `v0.1.803-beta` beobachtet | Aktuelles Release zum Zeitpunkt der Prüfung |

Anleitungen zum Modelltraining bilden eine Historie. Studio/Desktop bilden eine separate Historie der lokalen UI. Einen Studio-Artikel nicht zum Vorgänger eines unabhängigen Modellrezepts machen.

## Grenzen für Qwen3.5-Fine-Tuning {#qwen35-fine-tuning-bounds}

Die offizielle Anleitung gibt den ungefähren bf16-LoRA-Speicherbedarf nach Modellgröße an:

| Qwen3.5-Größe | Angegebener bf16-LoRA-Speicherbedarf |
|---|---:|
| 0,8B | 3 GB |
| 2B | 5 GB |
| 4B | 10 GB |
| 9B | 22 GB |
| 27B | 56 GB |
| 35B-A3B | 74 GB |

Die häufig wiederholte Angabe „5 GB“ bezieht sich ausschließlich auf das Rezept **2B bf16 LoRA**. Sie ist keine allgemeine Speicheranforderung für Qwen3.5 oder Unsloth.

Die Anleitung verlangt für diese Modellfamilie Transformers v5. Außerdem rät sie von 4-Bit-QLoRA für Qwen3.5 ab, weil sich das Quantisierungsverhalten von Rezepten unterscheidet, in denen 4-Bit-QLoRA der übliche Standard für geringen Speicherbedarf ist.

## Reproduzierbares Lauf-Protokoll {#reproducible-run-record}

```yaml
unsloth_surface: core-or-studio-or-desktop
unsloth_version: <exact-release-or-package-version>
model_id: <exact-model-and-size>
model_revision: <immutable-revision>
transformers_version: <exact-version>
training_mode: bf16-lora-or-other
quantization: none-or-exact-format
gpu_backend: nvidia-or-amd-or-intel-or-mps-or-cpu
gpu_and_vram: <exact-device>
sequence_length: <integer>
batch_and_accumulation: <values>
measured_peak_memory: <value>
```

Als verbindliche Grundlage für die Bereitstellung den gemessenen Spitzenspeicherbedarf verwenden. Die Tabellen der Anleitung sind Planungsgrenzen und keine Garantien über Sequenzlängen, Batch-Größen, Optimiererzustand und Offload-Einstellungen hinweg.

## Auswahl der Plattform {#platform-selection}

- Core verwenden, wenn Skripte, Notebooks, CI oder die exakte Fixierung von Abhängigkeiten erforderlich sind.
- Desktop verwenden, wenn eine lokale paketierte UI gefordert ist und deren aktueller Installer das Ziel-Betriebssystem/Backend unterstützt.
- Studio nur verwenden, wenn dessen aktueller Funktionsumfang zur Aufgabe passt; es nicht als Desktop bezeichnen.
- Der modellspezifischen Anleitung ist ein generisches Community-Rezept vorzuziehen.
- Nach jeder Änderung an Paket, Transformers, CUDA/Backend, Modell oder Quantisierung einen minimalen Trainingsschritt erneut ausführen.

## Community-Berichte {#community-reports}

- [Issue #7506](https://github.com/unslothai/unsloth/issues/7506) dokumentiert einen Absturz beim BF16-Training von Qwen3.5-0.8B auf einer Tesla T4. Ein Community-Vorschlag, die Trainer-Flags auf FP16 umzustellen, hat das Problem nicht vollständig behoben, weil der Berichtende weiterhin mit BF16 geladene Gewichte beobachtete. Qwen3.5-Training auf der T4 als ungelösten Fall gemischter Datentypen behandeln, nicht als Problem, das sich mit einem einzigen Flag beheben lässt.
- [Issue #9549](https://github.com/unslothai/unsloth/issues/9549) dokumentiert Unsloth Studio/Desktop `v0.1.801-beta` unter Windows 10 mit AMD W7900/W7500, bei dem ein Modell trotz VRAM-bezogener Optionen in den Systemspeicher geladen wurde. Der Bericht entstand nach dem Start von Desktop und ist weiterhin offen; das Verhalten auf dem aktuellen Release erneut prüfen, bevor man sich auf diese Schalter verlässt.
- Diese Berichte bestätigen, dass plattformübergreifende Unterstützung keine Backend-Parität bedeutet und dass Speicherangaben in der UI keine gemessenen Speicherbelege sind.

## Stolperfallen {#gotchas}

- **Problem:** Die Aussage „Qwen3.5 trainiert mit 5 GB“ ohne Modellgröße wiederholen -> **Lösung:** die Aussage an 2B bf16 LoRA binden und Sequenz- und Batch-Einstellungen festhalten.
- **Problem:** Generische 4-Bit-QLoRA-Hinweise auf Qwen3.5 anwenden -> **Lösung:** der aktuellen Familienanleitung folgen; sie empfiehlt diesen Weg nicht.
- **Problem:** Core, Studio und Desktop als eine versionierte Anwendung behandeln -> **Lösung:** die exakte Oberfläche und ihren eigenen Release- und Installationsvertrag festhalten.
- **Problem:** Plattformübergreifende Unterstützung als Funktionsparität lesen -> **Lösung:** exaktes Betriebssystem, Beschleuniger-Backend, Modell, Quantisierung und Workflow prüfen.
- **Problem:** `fp16=True` als bewährte Behebung für Qwen3.5 auf der T4 betrachten -> **Lösung:** einen Trainingsschritt reproduzieren; Issue #7506 blieb nach dieser Änderung bei gemischten Datentypen.

## Zeitlicher Status {#temporal-status}

- **Aktuell:** Produktzweig Desktop; `v0.1.803-beta` zum Zeitpunkt der Prüfung; Transformers-v5-Anforderung für Qwen3.5 und modellgrößenspezifische Hinweise zu bf16 LoRA.
- **Ersetzt oder revisionsempfindlich:** ältere Kopien der GPT-OSS-Rezepte und früher Qwen3.5-Rezepte.
- **Unbekannt bis zum Test:** exakte Hardware-/Format-Parität von Desktop sowie gemessener Speicherbedarf für die Sequenz- und Batch-Konfiguration eines Nutzers.

## Briefing für Agenten {#agent-brief}

Vor jeder Anleitung die angefragte Oberfläche (`Core`, `Studio` oder `Desktop`) und das exakte Modell festlegen. Die aktuelle offizielle Anleitung in der angefragten Sprache abrufen, alle Versionen fixieren und den angegebenen Planungsspeicher getrennt vom gemessenen Spitzenspeicher führen. Die Angabe 2B/5 GB für Qwen3.5 niemals verallgemeinern und 4-Bit-QLoRA für diese Familie nicht empfehlen, solange keine neueren offiziellen Belege vorliegen.

## Quellen {#sources}

- Offizielles Repository: https://github.com/unslothai/unsloth
- Offizielle Releases: https://github.com/unslothai/unsloth/releases
- Englische Dokumentation: https://unsloth.ai/docs
- Chinesische Dokumentation: https://unsloth.ai/docs/zh/
- Bericht zu T4/Qwen3.5 mit gemischten Datentypen: https://github.com/unslothai/unsloth/issues/7506
- Bericht zu Desktop/Studio und Systemspeicher: https://github.com/unslothai/unsloth/issues/9549

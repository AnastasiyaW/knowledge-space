---
title: "Holo3"
category: projects
date: 2026-04-02
tags: [h-company-holo3, holo3-model-release, holo3_model_release, project]
aliases: ["Holo3"]
level: 2
source_sha256: d875ab9348fa863216805b8d6709e7b8bc6d6b327ab4a26ff2a30680c7ca14c8
translation: machine
translated_at: '2026-10-24'
---
# Holo3 {#holo3}

**Entwicklungslinie:** `project:h-company-holo3` · Thread `holo3-model-release`  
**Letztes Ereignis:** 2026-04-02 · 1 datiertes seit 2026-04-02 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Holo3 ist ein multimodales MoE-Modell für Computer Use. Es nimmt Text und bis zu fünf Bilder entgegen und liefert eine Textaktion oder Entscheidung für Agenten-Workflows. Die API-Modelle sind 35B-A3B und 122B-A10B mit einem Kontext von 65 536 Token. Die Open Weights des ursprünglichen 35B-A3B sind unter Apache-2.0 veröffentlicht. Für neue Integrationen sollte man mit der aktuellen Holo3.1-Linie beginnen; das ursprüngliche Holo3 gilt als früherer, kompatibler Open-Checkpoint.

## Entwicklungslinie {#development-line}

- **2026-04-02 — H Company hat das Modell Holo3 veröffentlicht.** Am 2026-04-02 veröffentlichte H Company Holo3 als neues Modell. Verknüpfte Seiten zu Projekt, API und Modell-Repository deuten darauf hin, dass die Veröffentlichung sowohl für die direkte Nutzung als auch für den Modellzugriff gedacht war. Ohne Quelltext oder unabhängige Recherche bleiben genaue Fähigkeiten und Veröffentlichungsbedingungen unbestätigt.

## Was sich geändert hat {#what-changed}

- 2026-04-02 — Open Weights von Holo3-35B-A3B veröffentlicht; die Release-Seite beschreibt Holo3 als Computer-Use-Modell und nennt 122B-A10B als API-Flaggschiff.
- 2026-04-15 — HoloTab machte das Modell über eine Browser-Agent-Anwendung verfügbar.
- 2026-04-28 — Holotron 3 Nano (30B-A3B) als schnelleres, eigenständiges Modell für Computer-Automatisierungsaufgaben veröffentlicht.
- 2026-06-01 — Holo3.1 erweiterte die Linie um die Varianten 0.8B, 4B, 9B und 35B-A3B, Function Calling, Mobile-Unterstützung und lokale quantisierte Gewichte.

## So wird es verwendet {#how-to-use-this}

Ab 2026-04-02 sollte Holo3 anhand der Modell- und API-Dokumentation von H Company bewertet werden, bevor es für einen Workflow ausgewählt wird; unterstützte Fähigkeiten und Zugriffsbedingungen sind auf den verlinkten Seiten zu prüfen.

1. Portal-H-Konto und API-Schlüssel anlegen; der kostenlose Tarif bietet eingeschränkten Zugriff auf die 35B-A3B-API.
  — <https://hcompany.ai/holo-models-api>
2. `holo3-1-35b-a3b` für zeitlich begrenzte, klar definierte Aufgaben verwenden; `holo3-122b-a10b` für komplexe mehrstufige Szenarien, sofern die kommerziellen Bedingungen und die Preise passen.
  — <https://hcompany.ai/holo-models-api>
3. Für lokale Läufe des ursprünglichen Open-Holo3 `Hcompany/Holo3-35B-A3B` über Transformers, vLLM oder SGLang herunterladen und Nachrichten im multimodalen Chat-Template übergeben.
  — <https://huggingface.co/Hcompany/Holo3-35B-A3B>
4. Für mobile Setups, Function Calling oder lokale quantisierte Gewichte zu Holo3.1 wechseln und Gewichtsgröße sowie Format an die Zielhardware anpassen.
  — <https://hcompany.ai/holo3.1>

## Best Practices {#best-practices}

- 35B-A3B für latenzkritische, wirtschaftliche und klar definierte Automatisierungen wählen; 122B-A10B für neue oder komplexe mehrstufige Umgebungen.
  — <https://hcompany.ai/holo-models-api>
- Gewichtsformat und Laufzeitumgebung vor einem lokalen Deployment prüfen: Das ursprüngliche Holo3 ist für Transformers, vLLM und SGLang dokumentiert; Holo3.1 ergänzt FP8, Q4 GGUF und NVFP4.
  — <https://huggingface.co/Hcompany/Holo3-35B-A3B>
- Aussagen zu Zero Data Retention ersetzen keine Prüfung des Datenschutzes: Die API speichert Prompts und Antworten standardmäßig nicht, Logs enthalten jedoch Konto-Metadaten und Token.
  — <https://hcompany.ai/holo-models-api>

## Dadurch abgelöst {#superseded-by-this}

- 2026-06-01 — Holo3.1 löst das ursprüngliche Holo3 als empfohlene Linie für mobile Setups, Function Calling und lokale quantisierte Läufe ab.
- 2026-06-01 — Die Beschränkung auf eine einzelne 35B-A3B-Variante ist überholt: Die Varianten 0.8B, 4B, 9B und 35B-A3B von Holo3.1 sind verfügbar.

## Weiterhin unbekannt {#still-unknown}

- Für 122B-A10B listet die aktuelle API-Seite eine Lizenz nur für Forschung (nicht kommerziell); Zugriffsbedingungen und Lizenzierung zum Veröffentlichungsdatum am 2. April sind nicht gesondert bestätigt.
- Öffentliche Quellen bestätigen die Veröffentlichung von Holo3-35B-A3B am 2. April, während die Hauptankündigungsseite auf den 31. März datiert ist; die Differenz scheint zwischen Ankündigungsdatum und Veröffentlichungsdatum der Gewichte zu liegen, die genaue Veröffentlichungszeit ist jedoch nicht angegeben.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://hcompany.ai/holo3 | Holo3: Die Computer-Use-Grenze durchbrechen — H Company, 31. März 2026 | 2026-09-05 |
| https://hcompany.ai/holo-models-api | Holo Models API — H Company | 2026-09-05 |
| https://huggingface.co/Hcompany/Holo3-35B-A3B | Hcompany/Holo3-35B-A3B — Hugging Face | 2026-09-05 |
| https://hcompany.ai/holo3.1 | Holo3.1: Schnelle & lokale Computer-Use-Agenten — H Company, 1. Juni 2026 | 2026-09-05 |
| https://hcompany.ai/meet-holotab | HoloTab — H Company, 15. April 2026 | 2026-09-05 |
| https://hcompany.ai/holotron3 | Holotron 3 Nano — H Company, 28. April 2026 | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:h-company-holo3`, Thread `holo3-model-release`, 1 datiertes Ereignis 2026-04-02 → 2026-04-02.
- **Praxishinweis:** Ab 2026-04-02 sollten Praktiker Holo3 anhand der Modell- und API-Dokumentation von H Company bewerten, bevor sie es für einen Workflow auswählen; die genau unterstützten Fähigkeiten und Zugriffsbedingungen müssen auf den verlinkten Seiten geprüft werden.
- **Konfidenz:** hoch. Die datierten Abschnitte „Dadurch abgelöst“ sind maßgeblich dafür, was veraltet ist.

---
title: "Tencent"
category: organizations
date: 2025-12-29
tags: [ai-research-releases, organization, tencent, tencent_arc]
aliases: ["Tencent"]
level: 2
source_sha256: 2d1f4ec67910e8a5fc3c0dd39de9b3edbf38ae43ce8db575d1d6f702289935e8
translation: machine
translated_at: '2026-10-24'
---
# Tencent {#tencent}

**Entwicklungslinie:** `organization:tencent` · Strang `ai-research-releases`  
**Letztes Ereignis:** 2025-12-29 · 1 datiertes seit 2025-12-29 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Tencent bietet Verbraucherplattformen, Cloud, Marketing, Zahlungsdienste und digitale Dienste für Endverbraucher und Unternehmen an.

- Produktlinien für Verbraucher und für Unternehmen sind getrennt.
- Die DSR Suite von TencentARC ist ein VLM-Paket unter Apache-2.0, abgeleitet von Qwen2.5-VL-7B, zum Schlussfolgern über die Objektgeometrie und zeitliche Beziehungen in Videos.
- Es umfasst einen Trainingsdatensatz mit 50K QA-Paaren, einen Benchmark mit 1.484 QA-Paaren, ein 9B-BF16-Modell und ein Geometry Selection Module.

## Entwicklungslinie {#development-line}

- **2025-12-29 — Tencent ARC hat die Modell- und Code-Repositories der DSR Suite veröffentlicht.** Wir erhalten Code und Gewichte für dynamisches räumliches Schlussfolgern in Videos, mit DSR-Train, DSR-Bench und GSM auf einer Qwen2.5-VL-7B-Basis.

## Was sich geändert hat {#what-changed}

Entwicklungslinie von Tencent:

- 2023-05-02 — Tencent Cloud berichtete über eine Produktionsplattform für digitale Menschen mit geringem Stichprobenbedarf als Self-Service-Avatar-Workflow. Laut Bericht genügten ein dreiminütiges Sprechvideo und 100 Sprachsätze. Dies betrifft ein Produkt von Tencent Cloud, nicht die DSR Suite.
- 2025-12-29 — TencentARC hat die DSR Suite als offene Forschung veröffentlicht. Sie stellt Code und Gewichte für dynamisches räumliches Schlussfolgern in Videos bereit, mit DSR-Train, DSR-Bench und GSM auf einer Qwen2.5-VL-7B-Basis.
- 2025-12-25 bis 2026-02-21 — Das Repository datiert Paper und Code auf 2025-12-25 und verzeichnet die Annahme durch die CVPR 2026 am 2026-02-21. Dies ändert den akademischen Status, nicht die Verfügbarkeit als verwaltetes Tencent-Produkt.

## Anwendung {#how-to-use-this}

Stand 2025-12-29: Beginnen Sie mit dem veröffentlichten DSR-Suite-Modell und den Quell-Repositories und prüfen Sie Fähigkeiten und Lizenzierung, bevor Sie es einsetzen.

1. Wählen Sie zuerst die genannte Tencent-Produktlinie; Tencent selbst ist kein einzelner Entwickler-Endpunkt, und sein öffentlicher Katalog trennt Verbraucherdienste, Tencent Cloud und Marketingprodukte.
  — <https://www.tencent.com/what-we-create/>
2. Für die lokale Inferenz mit DSR Suite folgen Sie dem Transformers-Loader der Modellkarte für AutoProcessor und Qwen2_5_VLForConditionalGeneration_Spatial und laden TencentARC/DSR_Suite-Model mit device_map="auto".
  — <https://huggingface.co/TencentARC/DSR_Suite-Model>
3. Für eine reproduzierbare Prüfung laden Sie DSR-Bench als benchmark.parquet herunter, setzen die lokalen Video- und Parquet-Pfade in VLMEvalKit und führen dann dessen Spatial-Reasoning-Task aus.
  — <https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/README.md>
4. Für Fine-Tuning erstellen Sie die separate Python-3.11-Modellumgebung, installieren die Modellanforderungen, beschaffen Video-/Caption-Daten und optional DSR-Train, konvertieren die QA-Paare, setzen die Pfade für QA, Video und den Pi3-Checkpoint und führen anschließend train.sh aus.
  — <https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/model/README.md>

## Bewährte Vorgehensweisen {#best-practices}

- Führen Sie Datengenerierung und Modelltraining in getrennten Umgebungen aus, da sich die Paketanforderungen unterscheiden.
  — <https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/README.md>
- Planen Sie das lokale Hosting der 9B-BF16-Gewichte ein, statt von einem gehosteten Endpunkt auszugehen; die geprüfte Modellkarte nennt keinen Inferenzanbieter.
  — <https://huggingface.co/TencentARC/DSR_Suite-Model>
- Werten Sie DSR-Bench erst aus, nachdem Sie die referenzierten Videos beschafft und beide lokalen Pfade gesetzt haben; die Benchmark-Parquet-Datei liefert keine Videodateien direkt.
  — <https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/README.md>
- Entfernen Sie für eigene QA-Generierung statische Szenen vor der Generierung und konfigurieren Sie den API-Zugang: Die Kurations-Skripte benötigen Ihren eigenen Endpunkt und Token.
  — <https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/data/README.md>

## Durch dies ersetzt {#superseded-by-this}

- Keine verifizierte Produktablösung: Die DSR-Suite-Veröffentlichung vom 2025-12-29 ist nicht als Nachfolger der Tencent-Cloud-Plattform für digitale Menschen mit geringem Stichprobenbedarf vom 2023-05-02 dokumentiert.
- 2026-02-21: Die Annahme durch die CVPR 2026 ersetzt die Beschreibung des Papers von 2025 als bloße Veröffentlichung vor der Annahme; sie begründet jedoch keinen neuen verwalteten Dienst.

## Weiterhin unbekannt {#still-unknown}

- Der Bericht zur Tencent-Cloud-Plattform für digitale Menschen von 2023 und die DSR-Suite-Veröffentlichung von TencentARC aus dem Jahr 2025 betreffen unterschiedliche Produkte und Teams; keine geprüfte Quelle belegt eine gemeinsame API, eine Produktlinie oder ein Ersatzverhältnis.
- Für Zugang, Preis, regionale Verfügbarkeit oder Supportstatus der digitalen Menschen-Plattform von 2023 wurde keine aktuelle öffentliche Seite des Anbieters verifiziert.
- Die geprüften DSR-Suite-Quellen nennen keine getestete Transformers-Version, keinen GPU-Speicherbedarf und keinen Bereitstellungsweg in Tencent Cloud.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://www.tencent.com/who-we-are/ | Who we are - Tencent | 2026-09-04 |
| https://www.tencent.com/what-we-create/ | What we create - Tencent | 2026-09-04 |
| https://m.jiemian.com/article/9312569.html | 腾讯云公布小样本数智人生产平台，花费千元即可自行制作数字人 | 2026-09-04 |
| https://huggingface.co/TencentARC/DSR_Suite-Model | TencentARC/DSR_Suite-Model | 2026-09-04 |
| https://github.com/TencentARC/DSR_Suite | TencentARC/DSR_Suite | 2026-09-04 |
| https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/README.md | DSR_Suite README | 2026-09-04 |
| https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/model/README.md | DSR_Suite model training README | 2026-09-04 |
| https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/data/README.md | DSR_Suite data generation README | 2026-09-04 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `organization:tencent`, Strang `ai-research-releases`, 1 datiertes Ereignis 2025-12-29 → 2025-12-29.
- **Praxishinweis:** Stand 2025-12-29 sollten Praktiker, die Arbeiten von Tencent ARC bewerten, mit dem veröffentlichten DSR-Suite-Modell und den Quell-Repositories beginnen und deren Fähigkeiten und Lizenzierung vor dem Einsatz eigenständig prüfen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

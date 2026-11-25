---
title: "Video-DeepResearch"
category: projects
date: 2026-08-10
tags: [project, video-deepresearch]
aliases: ["Video-DeepResearch"]
level: 2
source_sha256: 0e6390d3b276f1634066f7f76499c75c1481632c4138020726a5f21b8883fb41
translation: machine
translated_at: '2026-10-24'
---
# Video-DeepResearch {#video-deepresearch}

**Entwicklungslinie:** `project:video-deepresearch` · Thread `video-deepresearch`  
**Letztes Ereignis:** 2026-08-10 · 1 datiert seit 2026-08-10 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Video-DeepResearch ist ein offener Forschungsstack und umfasst zwei Modelle für Fragen, die vor der Prüfung externer Quellen in Video-Objekten und -Ereignissen verankert sind.

- Keyframe-Auswahl: wählt Videoframes aus.
- Crop-Suche: untersucht visuelle Teilbereiche.
- Textsuche: fragt externe Quellen ab.
- Evidenzextraktion: zieht strukturierte Belege aus Webseiten.

Das dokumentierte Setup erfordert separate Inferenz-, Judge- und Extract-Dienste; Roh-Checkpoints und API-Schlüssel ersetzen diese nicht. Der Stack eignet sich für reproduzierbare Evaluation und Fine-Tuning videogestützter Agenten, nicht als eigenständiger Chat-Dienst.

## Entwicklungslinie {#development-line}

- **2026-08-10 — Öffentliches Projekt Video-DeepResearch und Quellenreferenzen wurden erfasst.** Die Videoaufgabe löst sich von der früheren, bildzentrierten Vision-DeepResearch ab und erzwingt visuelle Verankerung vor der Websuche.

## Was sich geändert hat {#what-changed}

2026-08-10 — Video-DeepResearch erschien als Projektseite und als Abschnitt im Vision-DeepResearch-Repository: Die Videoaufgabe löst sich von der früheren, bildzentrierten Vision-DeepResearch ab und erzwingt visuelle Verankerung vor der Websuche.

## So wird es verwendet {#how-to-use-this}

Stand 2026-08-10: Evaluieren Sie Video-DeepResearch anhand der verlinkten Projektseite und des Quell-Repositorys, und prüfen Sie Funktionsumfang und Veröffentlichungsstatus direkt.

1. Klonen Sie das Repository und arbeiten Sie im Unterordner Video-DeepResearch; er enthält separate Module für Preprocessing, Evaluation, SFT und RL.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
2. Extrahieren Sie Keyframes aus dem Video; die Dokumentation empfiehlt CLIP-Ähnlichkeitsfilterung, Pixeldifferenz nur als grobe Ersatzlösung.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
3. Starten Sie ein VLM für die Inferenz, einen separaten OpenAI-kompatiblen Judge und den erforderlichen Extract-Server für Visit; das Beispiel verwendet Qwen3-VL-30B-A3B-Instruct für Judge und Extract.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
4. Starten Sie ein Evaluationsskript für SGLang, vLLM oder OpenAI-kompatibles MaaS und wählen Sie den Modus tool, direct oder both.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>

## Best Practices {#best-practices}

- Sammeln Sie Belege aus Frames und Crops, bevor Sie die Textsuche öffnen: Diese Reihenfolge verhindert, dass der Agent aus dem Gedächtnis oder aus einer einzelnen Textanfrage antwortet.
  — <https://costaliya.github.io/Video-DeepResearch/>
- Verwenden Sie CLIP-Kosinus-Ähnlichkeit für Keyframes; greifen Sie nur dann auf Pixeldifferenz zurück, wenn CLIP nicht verfügbar ist, und berücksichtigen Sie die gröbere Auswahl.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
- Halten Sie den Extract-Server laufen: Ohne ihn liefert Visit rohes HTML statt strukturierter Belege, und die Dokumentation warnt, dass die Genauigkeit agentischer Abläufe deutlich sinkt.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
- Vergleichen Sie die Modi tool und direct über einen unabhängigen Judge, um Gewinne durch die Suche von Antworten zu trennen, die allein auf Keyframes beruhen.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>

## Ersetzt durch {#superseded-by-this}

- Bisher nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Öffentliche Materialien bestätigen Ankündigungen zu Code, Paper und Checkpoint, aber wir haben keine Inferenz ausgeführt und die aktuelle Verfügbarkeit, Lizenz und Hardwareanforderungen jedes Checkpoints nicht geprüft.
- VideoDR-Bench500 ist als „coming soon“ gelistet; wir können es weder als veröffentlicht behandeln noch für einen Vergleich verwenden.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://costaliya.github.io/Video-DeepResearch/ | Video-DeepResearch: Towards the Next-Generation Multimodal Deepresearch Agent | 2026-09-05 |
| https://github.com/Osilly/Vision-DeepResearch | Osilly/Vision-DeepResearch | 2026-09-05 |
| https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md | Video-DeepResearch README | 2026-09-05 |
| https://arxiv.org/abs/2608.03979 | Video-DeepResearch: Towards the Next-Generation Multimodal Deepresearch Agent | 2026-09-05 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:video-deepresearch`, Thread `video-deepresearch`, 1 datiertes Ereignis 2026-08-10 → 2026-08-10.
- **Praxishinweis:** Stand 2026-08-10 sollten Praktiker die verlinkte Projektseite und das Quell-Repository als Ausgangspunkte für die Evaluation von Video-DeepResearch nutzen und dessen Funktionsumfang und Veröffentlichungsstatus unabhängig prüfen.
- **Konfidenz:** hoch. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

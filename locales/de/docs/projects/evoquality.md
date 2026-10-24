---
title: "EvoQuality"
category: projects
date: 2026-06-11
tags: [bytedance-evoquality, bytedance-evoquality-development, evoquality, project]
aliases: ["EvoQuality"]
level: 2
source_sha256: a03c212de492ca7201b786313fc5927969d561b7fc3a86035f448fcdeb31c145
translation: machine
translated_at: '2026-10-24'
---
# EvoQuality {#evoquality}

**Entwicklungslinie:** `project:evoquality` · Thread `bytedance-evoquality-development`  
**Letztes Ereignis:** 2026-06-11 · 1 datiertes seit 2026-06-11 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

EvoQuality ist ein VLM zur referenzfreien Bildqualitätsbewertung für Forschende und Teams, die Bildpipelines betreiben.
- Bewertung: bewertet ein einzelnes Bild hinsichtlich seiner wahrgenommenen Qualität.
- Vergleich: vergleicht zwei Bilder nebeneinander.
- Ranking: erzeugt ein abstimmungsbasiertes Ranking-Signal zum Filtern oder zur Datenbereinigung.

Der veröffentlichte BF16-Checkpoint hat 8 Mrd. Parameter und stellt eine Runde der Selbstevolution dar. Er sollte als Proxy für die Wahrnehmung verwendet werden, ergänzt durch Stichprobenprüfungen, nicht als objektiver oder hochriskanter Entscheidungsträger.

## Entwicklungslinie {#development-line}

- **2026-06-11 — ByteDance veröffentlichte eine EvoQuality-Ressource auf Hugging Face.** ByteDance stellte am 2026-06-11 einen öffentlichen Link zu EvoQuality auf Hugging Face bereit. Damit ist der öffentliche Veröffentlichungszeitpunkt des Projekts markiert. Der Beitrag nennt weder Artefakttyp, Versionsdetails, Fähigkeiten noch Ankündigungshinweise.

## Was sich geändert hat {#what-changed}

2026-06-11 — Die EvoQuality-Gewichte wurden unter ByteDance/EvoQuality verfügbar. Die Veröffentlichung stellt einen BF16-Checkpoint mit 8 Mrd. Parametern bereit, der aus Qwen2.5-VL-7B durch selbstüberwachtes paarweises Abstimmen und GRPO trainiert wurde.

2025-09-30 — Die Arbeit erschien auf arXiv. Sie beschreibt die label-freie Methode aus Abstimmung und Ranking und berichtet eine Verbesserung des PLCC um 31,8 % gegenüber dem Basis-VLM in der Zero-Shot-IQA-Evaluation.

## Anwendung {#how-to-use-this}

Verwenden Sie die Hugging-Face-Ressource ByteDance/EvoQuality ab 2026-06-11 als datierten Referenzpunkt. Bestätigen Sie Artefakttyp und Nutzungsdetails vor einer Übernahme.

1. Laden Sie `ByteDance/EvoQuality` mit Transformers als Image-Text-to-Text-Modell, übermitteln Sie ein Bild zusammen mit dem Bewertungs-Prompt aus der Model Card und parsen Sie den abschließenden numerischen Wert in der Box.
  — <https://huggingface.co/ByteDance/EvoQuality>
2. Für ein lokales Ranking-Batch führen Sie das Inferenzskript für paarweises Abstimmen aus dem Repository mit Ihrem Checkpoint, Bildverzeichnis, Paar-CSV und einer explizit angegebenen Anzahl an Abstimmungen aus.
  — <https://github.com/bytedance/EvoQuality>
3. Für die Bereitstellung starten Sie das Modell mit vLLM oder SGLang und senden Bild-plus-Text-Anfragen an den Chat-Completions-Endpunkt.
  — <https://huggingface.co/ByteDance/EvoQuality>

## Best Practices {#best-practices}

- Verwenden Sie das Modell für Ranking, Filterung, Datenbereinigung und Bewertung vor dem Produktiveinsatz. Kombinieren Sie den Score mit geschäftlichen Signalen und manuellen Stichprobenprüfungen.
  — <https://huggingface.co/ByteDance/EvoQuality>
- Randomisieren Sie bei paarweiser Inferenz die Bildreihenfolge, um Positionsbias zu verringern. Halten Sie Prompts, Anzahl der Samples und Decoding-Einstellungen fest, wenn Läufe verglichen werden.
  — <https://huggingface.co/ByteDance/EvoQuality>
- Verwenden Sie die Ausgabe nicht als alleiniges Kriterium für Moderation, medizinische Bildgebung, rechtliche Beweise oder andere hochriskante Entscheidungen. Domänenverschiebung und Bias durch Pseudo-Labels bleiben dokumentierte Einschränkungen.
  — <https://huggingface.co/ByteDance/EvoQuality>

## Abgelöst durch dieses {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Die Hugging-Face-Model-Card dokumentiert den Checkpoint und die Nutzungswege, enthält jedoch keine versionierte Historie von Release Notes. In den geprüften Quellen fanden wir keinen späteren offiziellen EvoQuality-Checkpoint.
- Das Installationsbeispiel im Repository verwendet eine Platzhalter-Clone-URL (`your-organization/evoquality`). Verwenden Sie beim Klonen die oben genannte öffentliche Repository-URL.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/ByteDance/EvoQuality | ByteDance/EvoQuality Model Card | 2026-09-05 |
| https://github.com/bytedance/EvoQuality | bytedance/EvoQuality Repository | 2026-09-05 |
| https://arxiv.org/abs/2509.25787 | Self-Evolving Vision-Language Models for Image Quality Assessment via Voting and Ranking | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:evoquality`, Thread `bytedance-evoquality-development`, 1 datiertes Ereignis 2026-06-11 → 2026-06-11.
- **Praxishinweis:** Ab 2026-06-11 sollten Praktiker die Hugging-Face-Ressource ByteDance/EvoQuality als datierten öffentlichen Referenzpunkt zur Bewertung von Projektartefakten verwenden und dabei Artefakttyp und Nutzungsdetails vor einer Übernahme eigenständig prüfen.
- **Konfidenz:** hoch. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.

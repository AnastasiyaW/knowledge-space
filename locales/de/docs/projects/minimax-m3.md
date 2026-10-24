---
title: "MiniMax M3"
category: projects
date: 2026-06-13
tags: [minimax-m3, project]
aliases: ["MiniMax M3"]
level: 2
source_sha256: 4e7e7b61809a0b7c4c9e0926ff6911fbda821a3cd619a13c1294c0e433dbb829
translation: machine
translated_at: '2026-10-24'
---
# MiniMax M3 {#minimax-m3}

**Entwicklungslinie:** `project:minimax-m3` · Thread `minimax-m3`  
**Letztes Ereignis:** 2026-06-13 · 1 datiertes Ereignis seit 2026-06-13 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

MiniMax M3 ist ein Open-Weight-MoE-Modell mit nativer Multimodalität für Entwickler, die Coding-Agenten, Dokument- und Repository-Analysen sowie Workflows mit Bild- oder Videoeingabe bauen.

- Text-, Bild- und Videoeingabe.
- Gehostete Anthropic-kompatible und OpenAI-kompatible APIs.
- Lokales Serving über SGLang, vLLM, Transformers, KTransformers oder Unsloth.

1M-Token-Kontext; etwa 428B Parameter insgesamt und 23B aktivierte Parameter; der offizielle Hugging-Face-Checkpoint liegt in BF16 unter der minimax-community-Lizenz vor.

Beginnen Sie mit der gehosteten API; betreiben Sie das Modell erst selbst, nachdem Hardware- und Kontextkapazität dimensioniert wurden.

## Entwicklungslinie {#development-line}

- **2026-06-13 — Öffentliche Projekt-, Modell- und API-Ressourcen für MiniMax M3 erschienen.** Am 2026-06-13 wurde MiniMax M3 über ein öffentliches GitHub-Projekt-Repository, eine Hugging-Face-Modellseite und die Textgenerierungs-Dokumentation von MiniMax verlinkt. Diese Links verbinden die Projektquelle, die Modellverteilung und die Nutzungsdokumentation.

## Was sich geändert hat {#what-changed}

- 2026-06-01 — MiniMax M3 wurde in MiniMax Code, Token Plan und der API eingeführt; MiniMax erklärte, die Gewichte würden innerhalb von zehn Tagen folgen.
- 2026-06-13 — das öffentliche GitHub-Repository, der Hugging-Face-Checkpoint und die API-Dokumentation wurden gemeinsam aufgeführt; die vorgelagerte GitHub-Historie zeigt an diesem Datum keine separat datierte Modell- oder Dokumentationsänderung.
- 2026-06-18 — KTransformers wurde den dokumentierten Optionen für lokale Bereitstellung hinzugefügt.
- 2026-06-22 — ein Unsloth-Tutorial wurde den dokumentierten Optionen für lokale Bereitstellung hinzugefügt.

## Anwendung {#how-to-use-this}

Stand 2026-06-13 sollten Sie MiniMax M3 anhand des verlinkten Repositories, der Hugging-Face-Modellseite und der Textgenerierungs-Dokumentation bewerten, bevor Sie über den Einsatz entscheiden.

1. Erstellen Sie einen MiniMax-API- oder Abonnementschlüssel und wählen Sie `MiniMax-M3` als Modell aus.
  — <https://platform.minimax.io/docs/guides/text-generation>
2. Für den empfohlenen API-Pfad senden Sie eine Anthropic-Messages-Anfrage an `https://api.minimax.io/anthropic/v1/messages`; verwenden Sie den OpenAI-kompatiblen Endpunkt `/v1` nur, wenn Ihr Client dies erfordert.
  — <https://platform.minimax.io/docs/guides/text-generation>
3. Setzen Sie `thinking` auf `adaptive` für gemischte Workloads, auf `enabled` für bewusstes Schlussfolgern oder auf `disabled`, wenn Latenz und Durchsatz wichtiger sind.
  — <https://github.com/MiniMax-AI/MiniMax-M3>
4. Für lokale Inferenz laden Sie `MiniMaxAI/MiniMax-M3` herunter und betreiben es mit einer unterstützten Runtime wie SGLang oder vLLM.
  — <https://huggingface.co/MiniMaxAI/MiniMax-M3>

## Best Practices {#best-practices}

- Beginnen Sie mit den offiziellen Sampling-Standardwerten: `temperature=1.0` und `top_p=0.95`.
  — <https://github.com/MiniMax-AI/MiniMax-M3>
- Behandeln Sie das 1M-Kontextfenster als Bereitstellungsziel und nicht als automatische Einstellung: Wählen Sie Beschleuniger, Datentyp, Parallelisierung, Cache und maximalen Kontext passend zum tatsächlichen Traffic-Profil.
  — <https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-06-12-minimax-m3-vllm.md>
- Prüfen Sie die anbieterspezifische Tool-Unterstützung im genauen Client, bevor Sie sich darauf verlassen; ein offenes Issue berichtet, dass die Anthropic-artige integrierte Websuche trotz Messages-API-Kompatibilität nicht unterstützt wird.
  — <https://github.com/MiniMax-AI/MiniMax-M3/issues/23>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- 2026-06-01 — die Empfehlung, ein Modell der M2-Serie sei der neueste M-Serien-Standard, wird für neue, auf M3 ausgerichtete Arbeiten mit langem Kontext, Multimodalität, Coding und Agenten ersetzt. Die aktuelle Dokumentation hält M2-Modelle verfügbar, statt sie als eingestellt zu erklären.

## Weiterhin unbekannt {#still-unknown}

- Keine Release-Notiz des Herstellers und kein Upstream-Commit beschreibt am 2026-06-13 ein eigenständiges MiniMax-M3-Modell, eigene Gewichte oder eine API-Änderung; wir behandeln das Datum als Schritt der Verlinkung des Zugangs, nicht als Veröffentlichungsdatum.
- Die README-Commits vom 2026-07-01 und 2026-07-11 haben allgemeine Commit-Nachrichten, daher lassen sich ihre für Nutzer sichtbaren Änderungen nicht zuverlässig angeben.
- MiniMax hat keine einzelne aktuelle, vom Hersteller veröffentlichte Tabelle zur Hardware-Dimensionierung für den offiziellen BF16-Checkpoint von M3 über die verschiedenen Kontextlängen veröffentlicht.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://www.minimax.io/blog/minimax-m3 | MiniMax M3: Frontier Coding, 1M Context, Native Multimodality — All in One Model | 2026-09-05 |
| https://github.com/MiniMax-AI/MiniMax-M3 | MiniMax-AI/MiniMax-M3 | 2026-09-05 |
| https://github.com/MiniMax-AI/MiniMax-M3/commits/main | MiniMax-M3 commit history | 2026-09-05 |
| https://huggingface.co/MiniMaxAI/MiniMax-M3 | MiniMaxAI/MiniMax-M3 model card | 2026-09-05 |
| https://platform.minimax.io/docs/guides/text-generation | Model Invocation — MiniMax API Docs | 2026-09-05 |
| https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-06-12-minimax-m3-vllm.md | MiniMax M3 in vLLM: Day-0 Serving for 1M-Token Multimodal Reasoning | 2026-09-05 |
| https://github.com/MiniMax-AI/MiniMax-M3/issues/23 | M3 Bug: Anthropic-compatible endpoint does not support the web_search tool | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:minimax-m3`, Thread `minimax-m3`, 1 datiertes Ereignis 2026-06-13 → 2026-06-13.
- **Praktischer Hinweis:** Stand 2026-06-13 sollten Praktiker MiniMax M3 anhand des verlinkten Repositories, der Hugging-Face-Modellseite und der Textgenerierungs-Dokumentation bewerten, bevor sie über den Einsatz entscheiden.
- **Konfidenz:** mittel. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.

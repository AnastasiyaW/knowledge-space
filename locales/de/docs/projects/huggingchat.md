---
title: "HuggingChat"
category: projects
tags: [huggingchat, huggingchat-launch, project]
aliases: ["HuggingChat"]
level: 2
source_sha256: f64d57ca7de4b638158a0193013973f91b53836db6b6a0b87728d601d827bee9
translation: machine
translated_at: '2026-10-24'
---
# HuggingChat {#huggingchat}

**Entwicklungslinie:** `project:huggingchat` · Thread `huggingchat-launch`  
**Ereignisse:** 1 datiert, 2023-04-25 → 2023-04-25 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

HuggingChat ist eine webbasierte Chat-Oberfläche im Stil von ChatGPT für Hugging-Face-Nutzer, die Open-Source-Modelle betreiben. Die Chat-UI-Codebasis kann außerdem selbst gehostet werden.

- Gehostete Nutzung: Omni leitet einen Prompt automatisch weiter, oder ein Nutzer wählt ein Modell direkt aus.
- Deployment: Chat UI verbindet sich mit einer OpenAI-kompatiblen API und deren `/models`-Endpunkt.

## Entwicklungslinie {#development-line}

- **2023-04-25 — HuggingChat wurde mit einem Link auf ein OpenAssistant-Modell eingeführt.** Der Chat-Link verwies auf `OpenAssistant/oasst-sft-6-llama-30b-xor`, das in der Modellkarte als OpenAssistant LLaMA 30B SFT 6 bezeichnet wird. Dies zeigt einen frühen Modellkontext, nicht ein einzelnes gehostetes Backend.

## Was sich geändert hat {#what-changed}

HuggingChat entwickelte sich von einer OpenAssistant-Chat-Oberfläche zu einem routenden Dienst mit mehreren Anbietern.

- 2023-04-25: Der Chat-Link verwies auf `OpenAssistant/oasst-sft-6-llama-30b-xor`, dessen Modellkarte es als OpenAssistant LLaMA 30B SFT 6 identifiziert. Dies zeigt einen frühen Modellkontext, nicht ein einzelnes gehostetes Backend.
- 2023-06-11: Die Websuche lief bereits zu diesem Datum. Ein Beitrag des Betreibers vom 2023-06-02 sagt, der Schalter sei gerade erst eingeführt worden und befinde sich noch in einer frühen Phase. Der generische Chat-Link zeigt keine gesonderte Änderung am 11. Juni.
- 2025-07-01: HuggingChat kündigte an, dass der bisherige gehostete Dienst eingestellt werde, und bot den Export von Unterhaltungen an; Chat UI wird weiterhin gepflegt.
- 2025-10-16: HuggingChat kehrte mit Omni zurück, einem Richtlinien-Router über mehr als 115 Modelle und mehr als 15 Anbieter. Es zeigt an, welches Modell die jeweils weitergeleitete Anfrage bearbeitet hat.
- Heute festgestellt: Die aktive Seite bietet Omni und die direkte Modellauswahl über 138 Modelle. Die aktuelle README von Chat UI verwendet OpenAI-kompatible APIs; deren Dokumentation zur Websuche und die README widersprechen sich darin, ob ältere Hilfsfunktionen für die Websuche noch vorhanden sind.

## So wird es verwendet {#how-to-use-this}

Ab 2023-04-25 konnten wir den öffentlichen HuggingChat-Einstiegspunkt als frühe Oberfläche zu einem OpenAssistant-verknüpften Modell nutzen.

1. Öffnen Sie die gehostete App, melden Sie sich bei Aufforderung mit einem Hugging-Face-Konto an und wählen Sie Start chatting.
  — <https://huggingface.co/chat/>
2. Wählen Sie Omni für die automatische Weiterleitung oder ein benanntes Modell für einen direkten Vergleich; achten Sie bei Omni-Weiterleitung während des Streamings auf das angezeigte Modell.
  — <https://huggingface.co/spaces/huggingchat/chat-ui/discussions/764>
3. Für ein kontrolliertes Deployment klonen Sie Chat UI, konfigurieren `MONGODB_URL`, `OPENAI_API_KEY` und `OPENAI_BASE_URL` und betreiben es anschließend mit einem OpenAI-kompatiblen Anbieter.
  — <https://github.com/huggingface/chat-ui>

## Bewährte Vorgehensweisen {#best-practices}

- Prüfen Sie sachliche oder risikoreiche Ausgaben anhand von Primärquellen. Die gehostete Oberfläche warnt, dass generierte Inhalte ungenau oder falsch sein können.
  — <https://huggingface.co/chat/>
- Wählen Sie für reproduzierbare Auswertungen ein benanntes Modell oder protokollieren Sie das von Omni angezeigte Modell. Omni leitet jede Anfrage nach Richtlinien weiter und weicht auf andere Modelle aus, wenn ein primäres Modell nicht verfügbar ist.
  — <https://huggingface.co/spaces/huggingchat/chat-ui/discussions/764>
- Prüfen Sie die Bedingungen der Anbieter, bevor Sie sensible Daten senden. HuggingChat leitet Anfragen an externe Anbieter weiter, und jeder Anbieter ist für die Datensicherheit selbst verantwortlich.
  — <https://github.com/huggingface/chat-ui/blob/main/PRIVACY.md>
- Fixieren Sie für Self-Hosting die Revision von Chat UI. Testen Sie benötigte Funktionen direkt, statt anzunehmen, dass das alte Verhalten der Websuche im aktuellen Code weiterbesteht.
  — <https://github.com/huggingface/chat-ui>

## Abgelöst durch diese Informationen {#superseded-by-this}

- 2023-04-25: Behandeln Sie HuggingChat als dynamischen Router und nicht als feste OpenAssistant-LLaMA-30B-Endpunkt. Das aktuelle Produkt bietet Omni-Weiterleitung und direkte Auswahl aus einem sich ändernden Katalog.
- 2023-06-02 / 2023-06-11: Die frühen Hinweise zum Schalter der Websuche sind veraltet. Die aktuelle README besagt, dass ältere Hilfsfunktionen für die Websuche entfernt wurden, auch wenn die Dokumentation von Chat UI weiterhin die Websuche beschreibt.
- 2025-07-01: Die Ankündigung der Einstellung gilt nicht mehr. HuggingChat kündigte seine Rückkehr für den 2025-10-16 an, und die gehostete Seite war bei der Prüfung online.

## Weiterhin unbekannt {#still-unknown}

- Die Quelle vom 2023-04-25 konnte nicht abgerufen werden, daher bleiben ihr genauer Wortlaut und ihre Absicht unbestätigt. Ihr Link zur Modellkarte belegt kein alleiniges Produktions-Backend.
- Der Link vom 2023-06-11 verweist nur auf die generische Chat-URL. Der Beitrag vom 2023-06-02 bestätigt, wann die Websuche eingeführt wurde, aber nicht, ob der 11. Juni ein eigener Rollout, eine Korrektur oder eine erneute Veröffentlichung war.
- Der aktuelle Status der Websuche auf der gehosteten Seite ist ungeklärt. Die offizielle Dokumentation von Chat UI beschreibt die Websuche, während die aktuelle GitHub-README besagt, dass ältere Hilfsfunktionen für die Websuche entfernt wurden. Keine der beiden Quellen bestätigt, was auf der gehosteten Seite läuft.
- HuggingChat und das selbst gehostete Chat UI sind keine identischen Aufbauten. Der öffentliche Quellcode von Chat UI belegt nicht die genauen Modelle, Funktionen oder Anbieterkonfigurationen der gehosteten Instanz.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/chat/ | HuggingChat - Chat with AI models | 2026-09-04 |
| https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor | OpenAssistant/oasst-sft-6-llama-30b-xor · Hugging Face | 2026-09-04 |
| https://huggingface.co/spaces/huggingchat/chat-ui/discussions/185 | huggingchat/chat-ui · Feedback on the web search feature | 2026-09-04 |
| https://huggingface.co/spaces/huggingchat/chat-ui/discussions/747 | huggingchat/chat-ui · [ANNOUNCEMENT] HuggingChat is closing for now | 2026-09-04 |
| https://huggingface.co/spaces/huggingchat/chat-ui/discussions/764 | huggingchat/chat-ui · [NEW] HuggingChat Omni | 2026-09-04 |
| https://github.com/huggingface/chat-ui | GitHub - huggingface/chat-ui: The open source codebase powering HuggingChat | 2026-09-04 |
| https://github.com/huggingface/chat-ui/blob/main/PRIVACY.md | chat-ui/PRIVACY.md at main · huggingface/chat-ui · GitHub | 2026-09-04 |
| https://huggingface.co/docs/chat-ui/en/configuration/web-search | Web Search · Hugging Face | 2026-09-04 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:huggingchat`, Thread `huggingchat-launch`, 1 datiertes Ereignis 2023-04-25 → 2023-04-25.
- **Praxishinweis:** Ab 2023-04-25 konnten Praktiker den öffentlichen HuggingChat-Einstiegspunkt als frühe Oberfläche zu einem OpenAssistant-verknüpften Chatmodell nutzen.
- **Konfidenz:** mittel. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.

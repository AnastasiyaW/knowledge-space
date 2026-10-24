---
title: "Mistral Small 4 — Mistral Small"
category: projects
date: 2026-03-17
tags: [mistral-small, mistral-small-4, project]
aliases: ["Mistral Small 4"]
level: 2
source_sha256: fc77fefb86f9dd93541b002b7b0cdf46135bfeafd755ba14b6ad07d97066b7f1
translation: machine
translated_at: '2026-10-24'
---
# Mistral Small 4 — Mistral Small {#mistral-small-4-mistral-small}

**Entwicklungslinie:** `project:mistral-small-4` · Thread `mistral-small`  
**Letztes Ereignis:** 2026-03-17 · 1 datiertes seit 2026-03-17 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Worum es geht {#what-it-is}

Mistral Small 4 vereint Befehlsbefolgung, konfigurierbares Reasoning, Tool Calling, JSON-Ausgabe sowie Eingabe von Text und Bild mit Textausgabe. Das Modell hat insgesamt 119 Mrd. Parameter, davon 6,5 Mrd. aktiv pro Token, und ein Kontextfenster von 256k Token. Fazit: Einsetzen, wenn Konsolidierung wichtiger ist als minimale Infrastruktur; der Anbieter nennt für Self-Hosting mindestens vier HGX H100, zwei HGX H200 oder einen DGX B200.

## Entwicklungslinie {#development-line}

- **2026-03-17 — Das Repository Mistral Small 4 119B 2603 Eagle wurde auf Hugging Face verlinkt.** Am 2026-03-17 verzeichnete der Eintrag einen Link zum Hugging-Face-Repository für Mistral Small 4 119B 2603 Eagle. Der Repository-Name kennzeichnet ein Mistral-Small-4-Modellartefakt sowie dessen Variantenbezeichnungen 119B, 2603 und Eagle. Allein der datierte Link belegt weder Veröffentlichungsstatus, Fähigkeiten, Lizenz noch Zugangsbedingungen.

## Was sich geändert hat {#what-changed}

2026-03-17 — Das Repository Mistral-Small-4-119B-2603 Eagle stellte den trainierten Speculative-Decoding-Head für das Basismodell 119B A6B bereit. 2026-03-16 — Mistral kündigte das Basismodell Mistral Small 4 an: ein vereinheitlichter Nachfolgepfad für Instruct-, Reasoning-, multimodale und agentische Coding-Workloads, veröffentlicht unter Apache 2.0.

## So wird es verwendet {#how-to-use-this}

Stand 2026-03-17 sollten Praktiker das verlinkte Hugging-Face-Repository als konkretes Artefakt für die Variante Mistral Small 4 119B 2603 Eagle prüfen und vor einem Einsatz Model Card, Zugangsbedingungen und Veröffentlichungsstatus verifizieren.

1. Installieren Sie den Serving-Stack, den die Model Card vorgibt: vLLM, Transformers aus dem Main-Branch und mistral_common 1.10.0 oder neuer.
  — <https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle>
2. Betreiben Sie das Basismodell mit vLLM, aktivieren Sie die Mistral-Tool- und Reasoning-Parser und hängen Sie den Eagle-Head über vLLM Speculative Decoding an, wenn dessen zusätzliche Serving-Komplexität gerechtfertigt ist.
  — <https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle>
3. Setzen Sie bei Standardanfragen reasoning_effort auf none; bei schwierigen Aufgaben setzen Sie ihn über den OpenAI-kompatiblen Client oder die Mistral API auf high.
  — <https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle>

## Best Practices {#best-practices}

- Verwenden Sie reasoning_effort="high" mit temperature 0.7 bei komplexen Prompts; lassen Sie Reasoning bei Routineaufgaben deaktiviert und stimmen Sie die Temperatur zwischen 0.0 und 0.7 ab.
  — <https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle>
- Behandeln Sie das Eagle-Repository als Speculative-Decoding-Begleiter des Basismodells, nicht als eigenständiges Anwendungsmodell.
  — <https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle>
- Planen Sie das Self-Hosting entlang der dokumentierten Mindestausstattung an Beschleunigern, bevor Sie dieses Modell auswählen; die Anzahl aktiver Parameter hebt die Anforderungen an den Speicher für die Basisgewichte nicht auf.
  — <https://mistral.ai/news/mistral-small-4/?id=MistralSmall4>

## Dadurch überholt {#superseded-by-this}

- 2026-03-16 — Die Empfehlung, für diese vier zentralen Fähigkeitsklassen getrennte Modelle zu wählen (Mistral Small Instruct, Magistral Reasoning, Pixtral Multimodal und Devstral Coding), ist für Deployments überholt, in denen ein einziger Mistral-Small-4-Endpunkt die Anforderungen erfüllt.

## Noch ungeklärt {#still-unknown}

- Das am 17. März gemeldete Ereignis verlinkt das Eagle-Repository, während Mistrals eigene Ankündigung und Lifecycle-Seite die Veröffentlichung des Basismodells auf den 16. März 2026 datieren. Die heute geprüfte Repository-Seite zeigt kein Erstellungsdatum, sodass der genaue Veröffentlichungszeitpunkt nicht verifiziert ist.
- Mistrals Ankündigungsartikel nennt 6 Mrd. aktive Parameter pro Token (8 Mrd. einschließlich Embedding- und Ausgabeschichten), während die Eagle-Model-Card 6,5 Mrd. angibt. Diese Antwort übernimmt den Wert der Model Card für das aktuelle Serving-Artefakt und behandelt die Abweichung nicht als eigenständig aufgelöst.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle | mistralai/Mistral-Small-4-119B-2603-eagle | 2026-09-05 |
| https://mistral.ai/news/mistral-small-4/?id=MistralSmall4 | Introducing Mistral Small 4 | 2026-09-05 |
| https://legal.mistral.ai/ai-governance/models/mistral-small-4/ | Mistral Small 4 — Model Lifecycle | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:mistral-small-4`, Thread `mistral-small`, 1 datiertes Ereignis 2026-03-17 → 2026-03-17.
- **Praxishinweis:** Stand 2026-03-17 sollten Praktiker das verlinkte Hugging-Face-Repository als konkretes Artefakt für die Variante Mistral Small 4 119B 2603 Eagle prüfen und vor einem Einsatz Model Card, Zugangsbedingungen und Veröffentlichungsstatus verifizieren.
- **Konfidenz:** hoch. Die datierten Überholungsangaben oben sind maßgeblich dafür, was veraltet ist.

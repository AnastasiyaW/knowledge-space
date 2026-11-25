---
title: "JoyCaption"
category: projects
tags: [joycaption, joycaption-development, project]
aliases: ["JoyCaption"]
level: 3
source_sha256: 38b6b311ece1c22445c25055f730b547794ba2874c24c41f31396e5dd992cbbf
translation: machine
translated_at: '2026-10-24'
---
# JoyCaption {#joycaption}

**Entwicklungslinie:** `project:joycaption` · Thread `joycaption-development`  
**Ereignisse:** 2 datiert, 2024-09-26 → 2025-05-13 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

JoyCaption ist ein offenes Image-Captioning-VLM für Ersteller von Datensätzen für Diffusionsmodelle, eine lokale Alternative zu kostenpflichtigen Captioning-APIs wie GPT-4o.

- Erzeugt beschreibende und knappe sachliche Captions.
- Generiert Prompts im Diffusionsstil und mehrere Tag-Listenformate.
- Läuft über Transformers, ein Batch-Skript oder einen vLLM-Endpunkt mit OpenAI-kompatibler API.

## Entwicklungslinie {#development-line}

- **2024-09-26 — JoyCaption Alpha One Hugging Face Space erfasst.** Am 2024-09-26 wurde JoyCaption als Hugging Face Space fancyfeast/joy-caption-alpha-one veröffentlicht. Die Demo etablierte Alpha One, ohne öffentliche Modelldetails oder Release Notes.
- **2025-05-13 — Öffentliche Referenzen zu JoyCaption Beta One erfasst.** Am 2025-05-13 ergänzte JoyCaption Beta One um ein GitHub-Repository, einen Hugging Face Space, eine Hugging-Face-Modellseite und einen Civitai-Artikel. Diese Links etablierten Beta One, ohne technische Vergleiche mit Alpha One.

## Was sich geändert hat {#what-changed}

Entwicklungslinie von JoyCaption:

- 2024-09-26 — Alpha One wurde als öffentlicher Hugging Face Space für interaktives Captioning veröffentlicht.
- 2025-05-13 — Beta One brachte das herunterladbare Modell, eine aktualisierte Demo und lokale Skripte; es verbesserte das Befolgen von Anweisungen gegenüber Alpha Two, blieb aber in der Beta-Phase.
- Heute festgestellt — Das offizielle README nennt Beta One weiterhin als aktuell; GitHub Releases enthält kein paketiertes Release, und das Projekt hat keine 1.0 erklärt.

## Verwendung {#how-to-use-this}

Seit 2024-09-26 diente uns der Alpha-One-Hugging-Face-Space als Referenz; seit 2025-05-13 verfolgen wir Beta One über Repository, Space, Modellseite und Artikel, statt des alten Alpha-Links.

1. Testen Sie zuerst die offizielle Beta-One-Demo und prüfen Sie den Ausgabemodus und den erzeugten Prompt, bevor Sie einen Workflow automatisieren.
  — <https://github.com/fpgaminer/joycaption>
2. Für die lokale Nutzung laden Sie `fancyfeast/llama-joycaption-beta-one-hf-llava` mit Transformers, senden eine Nachricht aus Bild und Text, generieren und dekodieren nur die neu erzeugten Tokens.
  — <https://huggingface.co/fancyfeast/llama-joycaption-beta-one-hf-llava>
3. Wählen Sie `Descriptive Caption` für ausführlichen Trainingstext oder `Straightforward` für knappe, konkrete Labels; Länge und Tonalität drücken Sie in der dokumentierten Prompt-Form aus.
  — <https://github.com/fpgaminer/joycaption>
4. Für einen Datensatz führen Sie `batch-caption.py` mit `--glob` oder `--filelist` sowie `--prompt` oder einer gewichteten `--prompt-file` aus; die Captions werden als benachbarte `.txt`-Dateien geschrieben.
  — <https://github.com/fpgaminer/joycaption/blob/main/scripts/README.md>
5. Für einen Anwendungsendpunkt betreiben Sie Beta One mit vLLM und rufen dessen OpenAI-kompatible Chat-Completions-API auf.
  — <https://huggingface.co/fancyfeast/llama-joycaption-beta-one-hf-llava>

## Best Practices {#best-practices}

- Übergeben Sie `--model` in Batch-Jobs explizit: Die Skriptdokumentation verwendet noch Alpha Two als Standard, sodass das Übernehmen des Defaults ein älteres Modell auswählen kann.
  — <https://github.com/fpgaminer/joycaption/blob/main/scripts/README.md>
- Beginnen Sie mit dem Descriptive- oder Straightforward-Modus; der Maintainer bezeichnet sie als die nützlichsten und stuft mehrere andere Modi als weniger stabil ein.
  — <https://github.com/fpgaminer/joycaption>
- Prüfen Sie Labels, die für Training oder Entscheidungen verwendet werden, besonders bei mehreren Motiven, Links-rechts-Beziehungen, OCR und dem Befolgen von Anweisungen; Beta One dokumentiert verbleibende Fehler und Störungen.
  — <https://github.com/fpgaminer/joycaption>
- Bei direkten LLaVA-Integrationen behalten Sie den dokumentierten Chat-Template-Pfad bei und prüfen Sie die Input-IDs, damit doppelte BOS-Tokens die Ausgabe nicht verschlechtern.
  — <https://github.com/fpgaminer/joycaption>
- Verwenden Sie 8-Bit- oder 4-Bit-Quantisierung, wenn natives bfloat16 nicht passt, statt anzunehmen, dass das Modell leichtgewichtig ist.
  — <https://github.com/fpgaminer/joycaption>

## Abgelöst durch {#superseded-by-this}

- 2024-09-26 — JoyCaption Alpha One: für neue Arbeiten durch Beta One abgelöst, das das offizielle README weiterhin als aktuelles Modell nennt.
- 2024-09-26 — Erwartungen der Alpha-Ära an zuverlässiges Captioning: durch den leistungsfähigeren Beta-One-Workflow abgelöst, jedoch nicht durch eine Zuverlässigkeitsaussage für 1.0.

## Noch unbekannt {#still-unknown}

- Keine offizielle Ankündigung belegt ein Release nach Beta One oder bestätigt eine aktive Wartung nach den Modell- und Demo-Updates von 2025.
- Der zitierte Release-Artikel https://civitai.com/articles/14672 lieferte während der Recherche einen Fehler, daher wurden seine Release Notes nicht verwendet.
- Der gehostete Beta-One-Space ist als Running on Zero gelistet; er wurde nicht ausgeführt, daher wurden Verfügbarkeit, Kaltstartzeit und Ausgabequalität nicht unabhängig getestet.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/fpgaminer/joycaption | JoyCaption — offizielles GitHub-Repository und README | 2026-09-04 |
| https://huggingface.co/fancyfeast/llama-joycaption-beta-one-hf-llava | llama-joycaption-beta-one-hf-llava — Hugging-Face-Modellkarte | 2026-09-04 |
| https://github.com/fpgaminer/joycaption/blob/main/scripts/README.md | JoyCaption batch-caption.py Dokumentation — GitHub | 2026-09-04 |
| https://huggingface.co/spaces/fancyfeast/joy-caption-beta-one | Joy Caption Beta One — Hugging Face Space | 2026-09-04 |
| https://huggingface.co/spaces/fancyfeast/joy-caption-alpha-one | Joy Caption Alpha One — Hugging Face Space | 2026-09-04 |
| https://github.com/fpgaminer/joycaption/releases | JoyCaption Releases — GitHub | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:joycaption`, Thread `joycaption-development`, 2 datierte Ereignisse 2024-09-26 → 2025-05-13.
- **Praxishinweis:** Seit 2024-09-26 konnten Praktiker den Alpha-One-Hugging-Face-Space als öffentliche JoyCaption-Referenz nutzen; seit 2025-05-13 sollten sie zusätzlich das verlinkte Beta-One-Repository, den Space, die Modellseite und den Artikel heranziehen, statt sich allein auf die frühere Alpha-Referenz zu stützen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

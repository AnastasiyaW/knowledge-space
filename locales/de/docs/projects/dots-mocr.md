---
title: "dots.mocr"
category: projects
date: 2026-03-22
tags: [dots-mocr, project]
aliases: ["dots.mocr"]
level: 2
source_sha256: d87df4ce720a836981dbbd41e3ab80bd27a1f7feae200bad41412c8e081a2c70
translation: machine
translated_at: '2026-10-24'
---
# dots.mocr {#dotsmocr}

**Entwicklungslinie:** `project:dots-mocr` · Thread `dots-mocr`  
**Letztes Ereignis:** 2026-03-22 · 1 datiertes Ereignis seit 2026-03-22 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

dots.mocr ist ein 3B-VLM für Teams, die aus PDFs und Bildern nicht nur Text, sondern auch Layout, Tabellen, Formeln und Grafiken extrahieren müssen; Konkurrent von PaddleOCR-VL und DeepSeek-OCR. Funktionen: OCR und bbox, Markdown/HTML/LaTeX-Ausgabe, web/scene parsing, image-to-SVG über das separate dots.mocr-svg. Einschränkung: Komplexe Tabellen, Formeln und SVG können noch instabile Ergebnisse liefern. Fazit: Für self-hosted Document Parsing ist es sinnvoll, mit vLLM zu beginnen und komplexe Seiten anhand eigener Daten zu validieren.

## Entwicklungslinie {#development-line}

- **2026-03-22 — Ressourcen des dots.mocr-Projekts wurden verlinkt.** Am 2026-03-22 verlinkte eine datierte Meldung das GitHub-Repository von dots.mocr, zwei Hugging-Face-Ressourcen und eine Projektwebsite. Damit ist ein öffentlicher Referenzpunkt in der Entwicklungslinie des Projekts etabliert, einschließlich einer separat verlinkten SVG-bezogenen Ressource. Der zugrunde liegende Beitragsinhalt sowie die Art eines Releases oder Updates lagen nicht vor; daher behauptet dieser Eintrag keine Fähigkeiten, Versionen oder Leistungswerte.

## Was sich geändert hat {#what-changed}

2026-03-22 — die Hauptversion 3B dots.mocr und das separate 3B dots.mocr-svg wurden verfügbar; die erste Projektankündigung ist auf 2026-03-19 datiert, nicht auf den 22. März. Für diesen Schritt gilt: GitHub nennt das Hauptrelease vom 2026-03-19 und gibt ein Modell mit 3B Parametern sowie die Variante dots.mocr-svg für image-to-SVG an; Hugging Face nennt BF16 und die Größe 3B für beide Modelle. Weitere Ereignisse: 2026-03-13 — der MOCR-Artikel wurde erstmals auf arXiv eingereicht; 2026-03-19 — der Artikel wurde auf v2 aktualisiert, Code und beide Modelle wurden veröffentlicht; 2026-03-20 — im Repository gab es zwei nachfolgende Commits mit den Meldungen „fix ignore“ und „update“.

## Wie man es verwendet {#how-to-use-this}

Stand 2026-03-22 sollten Praktiker dots.mocr über das verlinkte GitHub-Repository, die Projektseite und die separaten Hugging-Face-Ressourcen evaluieren, einschließlich der SVG-bezogenen Ressource, bevor sie es für einen OCR-Workflow auswählen. Die datierten Links allein stützen keine Behauptungen zu Fähigkeiten oder Benchmarks.

1. Stellen Sie den Hauptdokumentparser über vLLM bereit: `vllm serve rednote-hilab/dots.mocr --trust-remote-code`; für SVG wählen Sie `rednote-hilab/dots.mocr-svg`.
  — <https://github.com/rednote-hilab/dots.mocr>
2. Übergeben Sie ein Bild oder PDF an `dots_mocr/parser.py`; das Ergebnis umfasst JSON mit Layout-Elementen, Markdown und ein Bild mit bbox.
  — <https://github.com/rednote-hilab/dots.mocr>
3. Wenn Sie einen OpenAI-kompatiblen Endpunkt benötigen, starten Sie das Modell über vLLM und senden Sie Nachrichten mit Bild und Text an `/v1/chat/completions`.
  — <https://huggingface.co/rednote-hilab/dots.mocr>

## Bewährte Verfahren {#best-practices}

- Verwenden Sie für Production-Inferenz vLLM: Die Autoren empfehlen es, und Transformers gilt als der langsamere Weg.
  — <https://github.com/rednote-hilab/dots.mocr>
- Wählen Sie `dots.mocr-svg` für image-to-SVG; das Hauptmodell ist durch die Kapazität von 3B begrenzt und nicht in allen SVG-Aufgaben gleich stark.
  — <https://github.com/rednote-hilab/dots.mocr>
- Verwenden Sie keine Punkte im Namen des lokalen Gewichtsordners: Die Dokumentation nennt `DotsMOCR` als vorübergehenden Workaround.
  — <https://github.com/rednote-hilab/dots.mocr>
- Prüfen Sie komplexe Tabellen, Formeln und Grafiken auf Ihrem Zielkorpus: Dies sind ausdrücklich genannte Einschränkungen des Modells.
  — <https://github.com/rednote-hilab/dots.mocr>

## Ersetzt durch dies {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Das Feld event_findings fehlt im bereitgestellten Ausgabeschema; sein Inhalt ist in what_changed enthalten. Auf GitHub gibt es keine versionierten Releases, daher lässt sich der aktuelle Build keinem formalen Tag oder Release-Asset zuordnen.
- Repository und Model Cards leiten von rednote-hilab auf studio-dots weiter; die Quellen erklären nicht, ob es sich nur um eine Umbenennung bzw. Übertragung der Organisation oder um einen Eigentümerwechsel handelt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/rednote-hilab/dots.mocr | studio-dots-ai/dots.mocr — Multimodal OCR: Parse Anything from Documents | 2026-09-05 |
| https://huggingface.co/rednote-hilab/dots.mocr | dots-studio/dots.mocr — Hugging Face model card | 2026-09-05 |
| https://huggingface.co/rednote-hilab/dots.mocr-svg | dots-studio/dots.mocr-svg — Hugging Face model card | 2026-09-05 |
| https://arxiv.org/abs/2603.13032 | Multimodal OCR: Parse Anything from Documents | 2026-09-05 |
| https://github.com/studio-dots-ai/dots.mocr/commits/main | studio-dots-ai/dots.mocr commit history | 2026-09-05 |
| https://github.com/studio-dots-ai/dots.mocr/releases | studio-dots-ai/dots.mocr releases | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:dots-mocr`, Thread `dots-mocr`, 1 datiertes Ereignis vom 2026-03-22 → 2026-03-22.
- **Praxishinweis:** Stand 2026-03-22 sollten Praktiker dots.mocr über das verlinkte GitHub-Repository, die Projektseite und die separaten Hugging-Face-Ressourcen evaluieren, einschließlich der SVG-bezogenen Ressource, bevor sie es für einen OCR-Workflow auswählen. Die datierten Links allein stützen keine Behauptungen zu Fähigkeiten oder Benchmarks.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

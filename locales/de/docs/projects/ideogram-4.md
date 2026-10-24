---
title: "Ideogram 4"
category: projects
tags: [ideogram, ideogram-4, ideogram-4-development, ideogram_4, project]
aliases: ["Ideogram 4"]
level: 3
source_sha256: 2ed9e9afc883dffbcc3c45325b99edeb6b3ecaa38d31c0cace7db4c0da021395
translation: machine
translated_at: '2026-10-24'
---
# Ideogram 4 {#ideogram-4}

**Entwicklungslinie:** `project:ideogram-4` · Thread `ideogram-4-development`  
**Ereignisse:** 2 datiert, 2026-06-04 → 2026-07-14 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Ideogram 4 ist ein Bildmodell mit strukturierter JSON-Eingabe für Designer und Entwickler, die kontrollierten Text, Komposition und Farbpalette benötigen. Es ersetzt generische Workflows mit flachen Prompts.

- rendert wörtlichen Text im Bild und mehrsprachige Typografie
- platziert Objekte und Text mit normalisierten Begrenzungsrahmen (Bounding Boxes)
- steuert Farbpaletten, Beleuchtung, Stil und Komposition über JSON
- läuft über gesperrte quantisierte Gewichte, die Ideogram-API, ComfyUI und eigenständige fal-Speed-Derivate

## Entwicklungslinie {#development-line}

- **2026-06-04 — Ideogram-4-Quellcode, Modellvarianten und ComfyUI-Integration wurden erfasst.** Inferenzcode sowie gesperrte FP8/NF4-Gewichte wurden öffentlich. Das Release führte strukturierte JSON-Steuerung für Text, Paletten und Layout über Begrenzungsrahmen ein. ComfyUI kündigte Unterstützung am Starttag an.
- **2026-07-14 — Ideogram v4 Instant und Fast wurden erfasst.** `ideogram-v4-instant` ist ein 8-Schritt-BF16-Checkpoint vor QAD. `ideogram-v4-fast` ist ein 20-Schritt-FP4/QAD-Checkpoint. Beide wurden von fal auf Basis von Ideograms FP8-Basis entwickelt und entfernen die CFG zur Laufzeit.

## Was sich geändert hat {#what-changed}

2026-06-04 — Ideogram 4.0 hielt Einzug in den lokalen Workflow. Das offizielle Release war auf 2026-06-03 datiert. Inferenzcode sowie gesperrte FP8/NF4-Gewichte wurden öffentlich. Sie ermöglichen strukturierte JSON-Steuerung für Text, Paletten und Begrenzungsrahmen-Layout. ComfyUI kündigte Unterstützung am Starttag an.

2026-07-14 — fal hat zwei getrennte, speed-destillierte Derivate hinzugefügt, anstatt ein neues kanonisches Ideogram-Release zu veröffentlichen. `ideogram-v4-instant` ist ein 8-Schritt-BF16-Checkpoint vor QAD. `ideogram-v4-fast` ist ein 20-Schritt-FP4/QAD-Checkpoint. Beide wurden von fal auf Basis von Ideograms FP8-Basis entwickelt und entfernen die CFG zur Laufzeit.

Heute erfasst, 2026-09-04 — Die offizielle Dokumentation nennt den kanonischen Endpunkt weiterhin Ideogram 4.0. Er akzeptiert entweder `text_prompt` oder `json_prompt`. Er unterstützt Ausgaben in 1K/2K und die Geschwindigkeitsstufen Default/Turbo/Quality. `FLASH` ist aufgeführt, liefert aktuell aber HTTP 400. Die aktuelle Lizenzierung trennt nicht-kommerzielle öffentliche Gewichte, kommerzielle API-Nutzung, lizenziertes Self-Hosting und Enterprise-Bedingungen.

## So wird es verwendet {#how-to-use-this}

Wir evaluieren Ideogram 4 nach dem 2026-06-04 über die verlinkten Pfade für Quelle, Modellvarianten und ComfyUI. Nach dem 2026-07-14 vergleichen wir Instant und Fast separat, wenn wir eine Ideogram-4-Route auswählen.

1. Wähle zuerst den Bereitstellungs- und Lizenzpfad. Nutze die gehostete API für kommerzielle Generierung. Verwende öffentliche quantisierte Gewichte nur für Forschung, Evaluierung, Prototyping oder persönliche Zwecke, sofern du nicht kommerzielle Self-Hosting-Rechte erwirbst.
  — <https://ideogram.ai/licensing/>
2. Für gehostete Generierung rufe `POST /v1/ideogram-v4/generate` mit einem `Api-Key` und genau einem von `text_prompt` oder `json_prompt` auf. Wähle 1K oder 2K sowie Default, Turbo oder Quality und lade das zurückgegebene Bild zeitnah herunter.
  — <https://developer.ideogram.ai/api-reference/generate-images/generate-v4>
3. Beginne die Exploration mit `text_prompt`, das Magic Prompt aktiviert. Wechsle zu `json_prompt`, wenn Palette, Layout oder wörtlicher Text deiner Spezifikation exakt folgen müssen.
  — <https://developer.ideogram.ai/api-reference/generate-images/generate-v4>
4. Für kontrollierte Designs baue `high_level_description`, `style_description` und `compositional_deconstruction` auf. Verwende bei Bedarf typisierte `text`-Elemente, wörtliche `text`-Werte und normalisierte `bbox`-Koordinaten.
  — <https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md>
5. Für lokale Inferenz mit dem Basismodell akzeptiere das Hugging-Face-Gate und authentifiziere dich mit `hf auth login`. Installiere das offizielle Repository, wähle den NF4- oder FP8-Checkpoint und führe den mitgelieferten Inferenz-Einstiegspunkt aus.
  — <https://github.com/ideogram-oss/ideogram4>
6. Für einen Node-Workflow nutze die Ideogram-4-Unterstützung in ComfyUI und deren JSON-Prompt-Struktur, anstatt das Layout in einen Fließtext-Prompt zu flachen.
  — <https://blog.comfy.org/p/ideogram-4-day-0-support-in-comfyui>
7. Für eine ausdrücklich latenzorientierte fal-Route konfiguriere `FAL_KEY` serverseitig und rufe `ideogram/v4/instant` auf. Kennzeichne die Ergebnisse weiterhin als fal-Derivat und nicht als Ausgabe des Basismodells Ideogram 4.0.
  — <https://fal.ai/models/ideogram/v4/instant/api>

## Best Practices {#best-practices}

- Für exakt gerenderten Text lege wörtlichen Text in ein JSON-`text`-Element oder setze ihn im Fließtext in Anführungszeichen. Halte jede Zeichenkette bei etwa 5–7 Wörtern und bevorzuge Wörter gegenüber kleinen numerischen Symbolen.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Behalte die vorgeschriebene JSON-Schlüsselreihenfolge bei, verwende Farbpalettenwerte in Großbuchstaben als `#RRGGBB` und führe den CaptionVerifier aus, bevor du ein lokales Prompt-Rezept übernimmst.
  — <https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md>
- Begrenze eine Komposition auf fünf oder weniger Elemente. Behandle Begrenzungsrahmen als Orientierung mit Abstand statt als Zuschnitt und beschreibe Boden oder Untergrund als `background`.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Verwende `V4_QUALITY_48` für finale lokale Renderings. Vergleiche die Presets Default mit 20 Schritten und Turbo mit 12 Schritten mit deinen eigenen Abnahmebildern, bevor du Qualität gegen Geschwindigkeit eintauschst.
  — <https://github.com/ideogram-oss/ideogram4/blob/main/docs/inference.md>
- Setze die öffentlichen Checkpoints nicht ohne Prüfung kommerziell ein. Die aktuellen Bedingungen behalten diese Nutzung der gehosteten API oder einer Self-Serve-/Enterprise-Lizenz vor.
  — <https://ideogram.ai/licensing/>
- Halte Ausgaben des Basismodells und von fal-Derivaten in getrennten Evaluierungssätzen. Instant ist ein von fal entwickeltes 8-Schritt-Derivat mit einem einzigen Zweig, kein checkpoint-identischer Lauf des Basismodells.
  — <https://huggingface.co/fal/ideogram-v4-instant>

## Hierdurch abgelöst {#superseded-by-this}

- 2026-06-03/04 — Die Vorgabe, Ideogram dürfe nur als geschlossener gehosteter Dienst genutzt werden, ist für Forschung und Prototyping überholt. Offizieller Inferenzcode und gesperrte öffentliche quantisierte Gewichte machten die lokale Nutzung möglich. Dies gewährt keine kommerziellen Self-Hosting-Rechte.
- 2026-06-18 — Flache, adjektivlastige Prompt-Rezepte sind für Ideogram 4 nicht mehr der Standard für Präzision. Strukturiertes JSON ist der bevorzugte Weg für Typografie-, Paletten- und Layoutsteuerung.
- 2026-07-14 — Die Behandlung von fal Instant oder Fast als kanonischen Nachfolger im Stil von Ideogram 4.1 ist überholt. Es handelt sich um speed-destillierte fal-Derivate, nicht um einen Ersatz für den Basis-Checkpoint 4.0.

## Weiterhin unbekannt {#still-unknown}

- Die beiden datierten Einträge beziehen sich auf eine gemeinsame Basis-Modellfamilie Ideogram. Die Juli-Einträge sind von fal erstellte Speed-Derivate und kein offizielles Kernmodell-Release von Ideogram.
- Keine geprüfte Quelle liefert eine unabhängige Evaluierung, die belegt, dass die 8-Schritt- oder 20-Schritt-Varianten von fal die Typografie- und Layouttreue des Basismodells 4.0 für Produktionslasten bewahren.
- Die geprüften öffentlichen offiziellen Seiten nennen keinen versionierten Basis-Checkpoint Ideogram 4.1 oder neuer. Dass diese Seiten ihn nicht nennen, beweist nicht, dass keine private oder unangekündigte Revision existiert.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://ideogram.ai/news/ideogram-4.0/ | Ideogram 4.0 Pressemitteilung | Ideogram | 2026-09-04 |
| https://ideogram.ai/blog/ideogram-4.0/ | Ideogram 4.0 Technical Details: Open model at the forefront of design | 2026-09-04 |
| https://github.com/ideogram-oss/ideogram4 | GitHub - ideogram-oss/ideogram4: Ideogram 4: Open image model at the forefront of design | 2026-09-04 |
| https://huggingface.co/ideogram-ai/ideogram-4-nf4 | ideogram-ai/ideogram-4-nf4 · Hugging Face | 2026-09-04 |
| https://blog.comfy.org/p/ideogram-4-day-0-support-in-comfyui | Ideogram 4.0 Day-0 Support in ComfyUI: Open Weights and Structured Control | 2026-09-04 |
| https://huggingface.co/fal/ideogram-v4-instant | fal/ideogram-v4-instant · Hugging Face | 2026-09-04 |
| https://huggingface.co/fal/ideogram-v4-fast | fal/ideogram-v4-fast · Hugging Face | 2026-09-04 |
| https://developer.ideogram.ai/api-reference/generate-images/generate-v4 | Generate with Ideogram 4.0 | Ideogram | Documentation | 2026-09-04 |
| https://ideogram.ai/blog/ideogram-4-json-prompting/ | How to JSON prompt for Ideogram 4.0 | 2026-09-04 |
| https://ideogram.ai/licensing/ | Licensing | Ideogram | 2026-09-04 |
| https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md | ideogram4/docs/prompting.md at main · ideogram-oss/ideogram4 · GitHub | 2026-09-04 |
| https://github.com/ideogram-oss/ideogram4/blob/main/docs/inference.md | ideogram4/docs/inference.md at main · ideogram-oss/ideogram4 · GitHub | 2026-09-04 |
| https://fal.ai/models/ideogram/v4/instant/api | V4.0q [instant] Text to Image API Docs | fal | 2026-09-04 |

## Agenten-Briefing {#agent-brief}

- **Gegenstand:** `project:ideogram-4`, Thread `ideogram-4-development`, 2 datierte Ereignisse 2026-06-04 → 2026-07-14.
- **Praktischer Hinweis:** Evaluiere Ideogram 4 nach dem 2026-06-04 über die verlinkten Pfade für Quelle, Modellvarianten und ComfyUI. Vergleiche Instant und Fast nach dem 2026-07-14 separat, wenn du eine Ideogram-4-Route auswählst.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, sind die datierten Abschnitte „Hierdurch abgelöst“ maßgeblich.

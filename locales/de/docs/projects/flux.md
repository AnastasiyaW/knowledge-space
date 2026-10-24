---
title: "FLUX.2"
category: projects
date: 2025-12-30
tags: [flux, flux-2-development, project]
aliases: ["1.58-bit FLUX", "FLUX", "FLUX.1", "FLUX.2", "FLUX.2 [dev] Turbo"]
level: 3
source_sha256: bc3cabda9ea9570ad8fa128565ffa8e2068cdf8568ff981b33a32e4939392e28
translation: machine
translated_at: '2026-10-24'
---
# FLUX.2 {#flux2}

**Entwicklungslinie:** `project:flux` · Thread `flux-2-development`  
**Letztes Ereignis:** 2025-12-30 · 5 datierte Einträge seit 2024-11-07 · **Recherchiert:** 2026-09-07 · Konfidenz: mittel

## Was es ist {#what-it-is}

FLUX.2 ist die Modellfamilie von Black Forest Labs für API-Teams, lokale Entwickler und ComfyUI-Pipelines, die Generierung und Bearbeitung über eine gemeinsame Pipeline abwickeln.
- Text-zu-Bild, textgesteuerte Bearbeitung und Komposition aus mehreren Referenzen.
- [max], [pro] und [flex] für die API-Nutzung, [dev] und [klein] für den lokalen Einsatz.
- Typografie, strukturiertes Prompting und Farbsteuerung für produktive Layouts.

[pro] begrenzt das Budget auf 9 MP, bezogen auf Eingaben und Ausgabe zusammen. Die lokalen Gewichte [dev] und [klein] 9B unterliegen einer nicht-kommerziellen Lizenz, während [klein] 4B unter Apache 2.0 steht.

FLUX.2 bietet sich an, wenn ein Workflow Referenzen und Bildbearbeitung zugleich benötigt. Eigenständige FLUX.1.1-API-Endpunkte sollten nicht automatisch ersetzt werden.

## Entwicklungslinie {#development-line}

- **2024-11-07 — FLUX 1.1 Ultra wurde öffentlich dokumentiert.** Am 2024-11-07 verlinkte diese Entwicklungslinie die Seite von Black Forest Labs zu FLUX 1.1 Ultra sowie die entsprechende Modellroute bei fal.ai. Zusammen markieren die datierten Links einen Meilenstein bei Dokumentation und Verfügbarkeit von FLUX 1.1 Ultra in der Linie, die FLUX.2 vorausgeht.
- **2024-12-30 — Ein Forschungspapier zu FLUX wurde in die Entwicklungslinie aufgenommen.** Am 2024-12-30 wurde in dieser Linie das Hugging-Face-Papier 2412.18653 verlinkt. Damit ist ein datierter Forschungsverweis in der FLUX-Linie festgehalten. Die vorliegenden Belege belegen jedoch nicht den genauen Beitrag des Papers zu einem bestimmten Release.
- **2025-11-25 — Ein Entwicklungs-Modell-Repository für FLUX.2 wurde verlinkt.** BFL veröffentlichte FLUX.2 [pro] und [flex] mit einer vereinheitlichten Pipeline für Generierung und Bearbeitung, einer Auflösung von bis zu 4 MP, Mehrfachreferenz-Eingaben, strukturierten Prompts und Typografie.
- **2025-11-27 — Prompting-Hinweise zu FLUX.2 wurden dokumentiert.** Am 2025-11-27 wurde der Prompting-Leitfaden von Black Forest Labs zu FLUX.2 zusammen mit einer Quellenangabe verlinkt. Damit ist die Anleitung zum Prompting ein datierter Bestandteil der öffentlichen FLUX.2-Entwicklungslinie. Der verlinkte Quelltext lag nicht vor.
- **2025-12-30 — FLUX.2-dev-Turbo wurde mit einer gehosteten Demo verlinkt.** fal verlinkte eine gehostete Demo, die 8 Schritte statt der üblichen 50 beansprucht und Text-zu-Bild sowie Bearbeitung unterstützt.

## Was sich geändert hat {#what-changed}

FLUX.2 trennt zwischen den älteren FLUX.1-Modellen, den eigentlichen FLUX.2-Releases und Adaptern von Drittanbietern.
- **2024-11-07**: FLUX1.1 [pro] Ultra ergänzte bis zu 4 MP Ausgabe und den RAW-Modus als FLUX.1-Release-Linie, nicht als FLUX.2-Release.
- **2024-12-30**: 1.58-bit FLUX zeigte 1.58-Bit-Quantisierung für FLUX.1-dev als Forschungsmethode, nicht als Gewichtsformat von FLUX.2.
- **2025-11-25**: BFL veröffentlichte FLUX.2 [pro] und [flex] mit einer vereinheitlichten Pipeline für Generierung und Bearbeitung, bis zu 4 MP, mehreren Referenzen, strukturierten Prompts und Typografie.
- **2025-11-25**: Comfy-Org stellte quantisierte FLUX.2-dev-Komponenten für ComfyUI als Community-Distribution bereit, nicht als Basis-Release von BFL.
- **2025-11-27**: Die Hinweise von BFL legten das Prompting für [pro] und [max] ohne Negativ-Prompts fest, mit strukturierten JSON-Prompts und Bearbeitung mit mehreren Referenzen.
- **2025-12-30**: fal/FLUX.2-dev-Turbo ergänzte einen LoRA-Adapter eines Drittanbieters für FLUX.2-dev, der 8 statt der üblichen 50 Schritte beansprucht und Text-zu-Bild sowie Bearbeitung unterstützt.
- **2026-01-15**: BFL veröffentlichte die Base-Varianten [klein] 4B und 9B für lokale interaktive Anwendungen. 4B steht unter Apache 2.0, 9B unter FLUX NCL.
- **2026-02-17**: Der Erfolgsstatus des API-Webhooks wurde von SUCCESS auf Ready geändert.
- **2026-03-03**: Qualitätsverbesserungen für [pro] werden über flux-2-pro-preview ausgeliefert, während flux-2-pro als fixierter Snapshot zur Reproduzierbarkeit erhalten bleibt.
- **2026-04-23**: Die öffentliche Beta des verwalteten LoRA-Inferenzbetriebs für [klein] wurde über -finetuned-Endpunkte geöffnet.
- **2026-07-31**: Es wurde keine verifizierte Änderung erfasst, da die verlinkte Veröffentlichung nicht lesbar war.

## So verwenden Sie es {#how-to-use-this}

1. Passen Sie die Variante an die Aufgabe an: [max] für höchste Qualität und Grounding-Suche, [pro] für kommerzielle Pipelines, [flex] für Typografie im Bildrahmen, [klein] für niedrige Latenz und [dev] für nicht-kommerzielle Anpassung. Prüfen Sie die Gewichtslizenz, bevor Sie Modelle lokal ausführen.
  — <https://help.bfl.ai/articles/6122710168-which-flux-2-model-should-i-choose>
2. Senden Sie Anfragen an den gewählten BFL-API-Endpunkt, speichern Sie die zurückgegebene polling_url und laden Sie das generierte Asset von dort. Der Status Ready markiert einen Erfolg, Error und Failed sind terminale Fehler.
  — <https://docs.bfl.ai/quick_start/generating_images>
3. Nutzen Sie den Preview-Endpunkt, um Modellverbesserungen zu prüfen. Für reproduzierbare Produktionsausgaben wählen Sie einen fixierten Nicht-Preview-Endpunkt und mischen Sie die Endpunkte innerhalb eines Generierungslaufs nicht.
  — <https://docs.bfl.ai/quick_start/generating_images>
4. Akzeptieren Sie die Repository-Bedingungen auf Hugging Face, um FLUX.2-dev lokal zu nutzen. Laden Sie die Gewichte über Diffusers in bfloat16 auf CUDA und übergeben Sie für die Bearbeitung ein Bild zusammen mit dem Prompt.
  — <https://huggingface.co/black-forest-labs/FLUX.2-dev/tree/main>
5. Aktualisieren Sie ComfyUI, um [klein] 4B lokal auszuführen. Wählen Sie einen vorhandenen Text-zu-Bild- oder Bearbeitungs-Workflow und legen Sie Text-Encoder, Diffusionsmodell und VAE in die vorgesehenen Modellverzeichnisse.
  — <https://docs.comfy.org/zh/tutorials/flux/flux-2-klein>
6. Binden Sie den Turbo-LoRA von fal als Drittanbieter-Adapter an FLUX.2-dev an, wenn die Latenz der Hauptengpass ist, und verwenden Sie dessen eigene 8-Schritte-Sigmas. Das veröffentlichte Beispiel nutzt 8 Schritte und guidance_scale 2.5.
  — <https://huggingface.co/fal/FLUX.2-dev-Turbo>

## Bewährte Praktiken {#best-practices}

- Strukturieren Sie Prompts für [pro] und [max] nach dem Schema Subjekt + Aktion + Stil + Kontext. Platzieren Sie zentrale Details am Anfang und halten Sie Beschreibungen zwischen 30 und 80 Wörtern.
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- Verzichten Sie vollständig auf Negativ-Prompts. Beschreiben Sie das gewünschte Ergebnis direkt, etwa „durchgehend scharfer Fokus“ statt „keine Unschärfe“.
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- Verwenden Sie JSON-Prompts für strukturierte Automatisierung und beginnen Sie mit einfachen Schemastrukturen. Weisen Sie HEX-Farbcodes einzelnen Objekten zu statt dem gesamten Bild.
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- Weisen Sie bei der Bearbeitung mit mehreren Referenzen jedem Eingabebild eine explizite Rolle zu. Bleiben Sie bei [pro] im Gesamtbudget von 9 MP. Dieses erlaubt höchstens 8 Referenzbilder zusammen mit einem Ausgabebild von 1 MP.
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- Halten Sie die Endpunkte bei Evaluierungsläufen konstant. Wählen Sie Preview für aktuelle Modelländerungen und fixierte Endpunkte, wenn reproduzierbare Ausgaben erforderlich sind.
  — <https://docs.bfl.ai/quick_start/generating_images>
- Trainieren Sie LoRA-Adapter auf dem undestillierten Klein Base, deployen Sie für interaktive Bildgenerierung aber das destillierte Klein. Prüfen Sie die Lizenzen getrennt: 4B steht unter Apache 2.0, 9B bleibt unter FLUX NCL.
  — <https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence>

## Durch diesen Stand überholt {#superseded-by-this}

- 2026-02-17: Die Webhook-Verarbeitung mit status=SUCCESS ist veraltet; prüfen Sie stattdessen status=Ready.
- 2026-03-03: Die Annahme, dass flux-2-pro Modellaktualisierungen automatisch übernimmt, ist veraltet. Verwenden Sie für neue Aktualisierungen flux-2-pro-preview und behalten Sie flux-2-pro für wiederholbare Ausgaben.
- 2026-04-23: Die Finetuning-API aus der FLUX.1-Ära wurde im Oktober 2025 eingestellt. BFL verweist selbstbedientes LoRA-Training auf die Endpunkte FLUX.2 [klein] -finetuned mit finetune_id und finetune_strength.
- 2024-12-30: 1.58-bit FLUX taugt nicht als Einrichtungsanleitung für FLUX.2, weil das Paper FLUX.1-dev quantisiert.

## Weiterhin unbekannt {#still-unknown}

- Der Inhalt der Veröffentlichung vom 2026-07-31 konnte weder über den bereitgestellten Spiegel noch über die kanonische X-URL gelesen werden. Eine Änderung wird daher nicht behauptet.
- Die Meilensteine vom 2024-11-07 und 2024-12-30 beschreiben FLUX.1.1 bzw. FLUX.1-dev und nicht FLUX.2. Sie gehören zu einer verwandten Linie und nicht zu einem einzelnen Release-Strang.
- Qualität und Kompatibilität von FLUX.2 [dev] Turbo stützen sich allein auf die Modellkarte bei fal. Unabhängige Benchmarks haben wir nicht geprüft.
- Für ComfyUI existiert offizielle chinesische Dokumentation, doch eine lokale Ausführung auf bestimmter Hardware haben wir nicht verifiziert.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://blackforestlabs.ai/flux-1-1-ultra/ | Vorstellung von FLUX1.1 [pro] Ultra und Raw-Modi | Black Forest Labs | 2026-09-04 |
| https://huggingface.co/papers/2412.18653 | 1.58-bit FLUX | Hugging Face Papers | 2026-09-04 |
| https://huggingface.co/Comfy-Org/flux2-dev | Comfy-Org/flux2-dev | Hugging Face | 2026-09-04 |
| https://bfl.ai/blog/flux-2 | FLUX.2: Frontier Visual Intelligence | Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/guides/prompting_guide_flux2 | Prompting-Leitfaden – FLUX.2 [pro] & [max] | Black Forest Labs | 2026-09-04 |
| https://huggingface.co/fal/FLUX.2-dev-Turbo | FLUX.2 [dev] Turbo LoRA | fal | 2026-09-04 |
| https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence | FLUX.2 [klein]: Towards Interactive Visual Intelligence | Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/release-notes | Release Notes | Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/quick_start/generating_images | Bildgenerierung mit Text-Prompts | Black Forest Labs | 2026-09-04 |
| https://help.bfl.ai/articles/6122710168-which-flux-2-model-should-i-choose | Welches FLUX.2-Modell sollte ich wählen? | Wissensdatenbank von Black Forest Labs | 2026-09-04 |
| https://huggingface.co/black-forest-labs/FLUX.2-dev/tree/main | black-forest-labs/FLUX.2-dev at main | Hugging Face | 2026-09-04 |
| https://docs.comfy.org/zh/tutorials/flux/flux-2-klein | ComfyUI Flux.2 Klein 4B 指南 | ComfyUI | 2026-09-04 |
| https://bfl.ai/models/flux-2 | FLUX.2 – Next Generation Image Generation | Black Forest Labs | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:flux`, Thread `flux-2-development`, 5 datierte Ereignisse vom 2024-11-07 bis 2025-12-30.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Die datierten Überholungen oben sind maßgeblich für das, was veraltet ist.

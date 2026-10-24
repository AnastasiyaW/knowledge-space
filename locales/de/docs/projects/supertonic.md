---
title: "Supertonic — Öffentliche Projektreferenz"
category: projects
date: 2026-05-18
tags: [project, public-project-reference, supertonic]
aliases: ["Supertonic"]
level: 2
source_sha256: b8209c813e5a50c276e7949bddc5586982a8dba4bc95aeb80ba9058573b0761b
translation: machine
translated_at: '2026-10-24'
---
# Supertonic — Öffentliche Projektreferenz {#supertonic-public-project-reference}

**Entwicklungslinie:** `project:supertonic` · Thread `public-project-reference`  
**Letztes Ereignis:** 2026-05-18 · 1 datiertes seit 2026-05-18 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Supertonic — ein ONNX-Runtime-Stack für Text-to-Speech für Entwickler, die eine selbst gehostete Alternative zu gehosteten TTS-APIs benötigen.

- Python-SDK, CLI und HTTP-Server auf Loopback
- Supertonic-3 mit 31 Sprachcodes plus `na` als Fallback
- zehn mitgelieferte Voice-Styles und JSON-Import für den Voice Builder

## Entwicklungslinie {#development-line}

- **2026-05-18 — Öffentliche Repository-Referenz zu Supertonic.** Am 2026-05-18 verlinkte der Supertonic-Thread auf das öffentliche GitHub-Repository des Projekts zusammen mit einer Quellenreferenz. Damit ist ein datierter öffentlicher Referenzpunkt für das Projekt etabliert, ohne dass ein bestimmtes Release, Feature oder eine Code-Änderung behauptet wird.

## Was sich geändert hat {#what-changed}

- 2025-12-10 — das Python-Paket und sechs zusätzliche eingebaute Voice-Styles wurden eingeführt.
- 2026-01-06 — Supertonic 2 erweiterte das Modell von Englisch auf fünf Sprachen; sein Code-Pfad blieb auf einem Release-Branch.
- 2026-01-22 — Voice Builder ging für dauerhafte benutzerdefinierte Voice-Profile live.
- 2026-04-29 — Supertonic 3 wurde mit Unterstützung für 31 Sprachen, Verbesserungen bei der Lesestabilität und einer zu v2 kompatiblen öffentlichen ONNX-Schnittstelle veröffentlicht.
- 2026-05-18 — Python-SDK 1.3.1 ergänzte die lokale HTTP-Schnittstelle `supertonic serve`; Voice Builder ergänzte JSON-Profile für Supertonic 3.
- 2026-05-20 — Supertonic 3 wurde in Supertone Play und der Supertone API verfügbar.

## So verwenden Sie es {#how-to-use-this}

Beginnen Sie mit dem verlinkten öffentlichen GitHub-Repository in dem Stand vom 2026-05-18. Wir haben keine Belege für versionsspezifische Einführungshinweise.

1. Installieren Sie `supertonic`; verwenden Sie Python 3.9 oder neuer.
  — <https://pypi.org/project/supertonic/>
2. Erstellen Sie `TTS(auto_download=True)`, wählen Sie einen mitgelieferten Voice-Style, synthetisieren Sie Text und speichern Sie die WAV-Ausgabe.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>
3. Übergeben Sie einen unterstützten ISO-Sprachcode, sofern bekannt, oder `na` für sprachunabhängige Verarbeitung.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>
4. Für HTTP-Clients installieren Sie `supertonic[serve]`, starten Sie `supertonic serve --host 127.0.0.1 --port 7788` und rufen Sie anschließend `/v1/tts` oder `/v1/audio/speech` auf.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>

## Best Practices {#best-practices}

- Beginnen Sie mit dem Standardwert von acht Syntheseschritten und messen Sie dann Qualität gegen Latenz. Die Abstimmung läuft über 5–12 Schritte und die Geschwindigkeit über 0,7–2,0.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>
- Laden Sie das etwa 400 MB große Modell-Asset während der CI- oder Deployment-Einrichtung vorab herunter, damit die erste Produktionsanfrage nicht die Download-Kosten trägt.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>
- Belassen Sie `supertonic serve` standardmäßig auf Loopback. Stellen Sie es nur hinter einem Reverse-Proxy bereit.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>
- Trennen Sie die Lizenz- und Einwilligungspflichten des Modells von der MIT-Lizenz des Python-Quellcodes, insbesondere beim Import eines benutzerdefinierten Voice-Profils.
  — <https://github.com/supertone-inc/supertonic-py/blob/main/llms.txt>
- Testen Sie vor einem Barrierefreiheits-Einsatz die Latenz mit Screenreadern und die sprachspezifische Aussprache von Zahlen. Ein türkischsprachiger NVDA-Nutzer berichtete nach dem v3-Release über Verzögerungen und Fehler bei der Aussprache von Ziffern.
  — <https://github.com/supertone-inc/supertonic/issues/144>

## Hierdurch abgelöst {#superseded-by-this}

- 2026-04-29 — Supertonic 3 ersetzt für neue mehrsprachige Deployments die Empfehlung für Supertonic 2 mit fünf Sprachen. Es unterstützt 31 Sprachen und behält die zu v2 kompatible öffentliche ONNX-Schnittstelle bei. Supertonic 2 bleibt für Legacy-Integrationen auf seinem Release-Branch im Einsatz.
- 2026-05-18 — Die Python-Einbettung ist nicht mehr der einzige offizielle Integrationspfad. Das SDK 1.3.1 ergänzte eine lokale HTTP-Fassade, während die eingebettete Nutzung dort, wo sie einfacher ist, weiterhin gültig bleibt.

## Weiterhin unbekannt {#still-unknown}

- Wir haben in der geprüften chinesischen Suchspur keine offizielle Dokumentation in vereinfachtem Chinesisch gefunden. Die geprüften Materialien aus erster Hand waren Englisch oder Koreanisch, was das Vorhandensein einer solchen Seite nicht ausschließt.
- PyPI listet am 2026-05-18 sowohl 1.3.0 als auch 1.3.1. Wir haben keine Release-Notes gefunden, die 1.3.0 als eigenständiges Entwicklungsereignis ausweisen würden.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/supertone-inc/supertonic | GitHub - supertone-inc/supertonic: Lightning-Fast, On-Device, Multilingual TTS — running natively via ONNX. | 2026-09-05 |
| https://pypi.org/project/supertonic/ | supertonic · PyPI | 2026-09-05 |
| https://supertone-inc.github.io/supertonic-py/quickstart/ | Quick Start - supertonic-py | 2026-09-05 |
| https://github.com/supertone-inc/supertonic-py/blob/main/llms.txt | supertonic-py/llms.txt at main · supertone-inc/supertonic-py | 2026-09-05 |
| https://www.supertone.ai/en/work/faster-and-more-accurate-across-31-languages----introducing-supertonic-3 | Faster and more accurate across 31 languages — introducing Supertonic 3! | Supertone | 2026-09-05 |
| https://supertonic3.github.io/ | Supertonic 3 — Lightning-Fast, On-Device, Multilingual TTS | 2026-09-05 |
| https://github.com/supertone-inc/supertonic/issues/144 | supertonic tts turkish language and screen readers · Issue #144 | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:supertonic`, Thread `public-project-reference`, 1 datiertes Ereignis 2026-05-18 → 2026-05-18.
- **Praktischer Hinweis:** Beginnen Sie mit dem verlinkten öffentlichen GitHub-Repository in dem Stand vom 2026-05-18. Wir haben keine Belege für versionsspezifische Einführungshinweise.
- **Konfidenz:** hoch. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.

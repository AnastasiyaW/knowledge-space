---
title: "WhatModels — Öffentliche Website"
category: projects
date: 2026-05-15
tags: [project, public-website, whatmodels]
aliases: ["WhatModels"]
level: 2
source_sha256: 85187382ea7faecedce3c6be6ff706959f25d4844fe4396c72eb9d591f6959f5
translation: machine
translated_at: '2026-10-24'
---
# WhatModels — Öffentliche Website {#whatmodels-public-website}

**Entwicklungslinie:** `project:whatmodels` · Thread `public-website`  
**Letztes Ereignis:** 2026-05-15 · 1 datiertes seit 2026-05-15 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

WhatModels ist ein Modellauswahlwerkzeug für Nutzer von Ollama, llama.cpp und anderen lokalen Laufzeitumgebungen, um Modelle nach GPU oder manuell eingegebenem VRAM auszuwählen und dabei maximalen Kontext und Generierungsgeschwindigkeit abzuschätzen.

- GPU-Katalog zur Auswahl von Hardware-Voreinstellungen.
- Manuelle VRAM-Eingabe zur Festlegung benutzerdefinierter Speichergrenzen.
- Filter für minimalen Kontext, um Konfigurationen auszusortieren, die darunter liegen.
- Quantisierungsvergleich zur Bewertung von Größe gegenüber Speicherbedarf.
- Passformkategorien zur Gruppierung von Modellen in „läuft gut“, „knappe Passung“ und „passt nicht“.

Die Generierungsgeschwindigkeit erscheint nur für Katalog-GPUs und bleibt eine Schätzung statt eines Laufzeit-Benchmarks.

Das Werkzeug eignet sich für die erste Auswahl von Modell und Hardware, doch der Produktionsbetrieb erfordert eine Überprüfung auf der lokalen Hardware.

## Entwicklungslinie {#development-line}

- **2026-05-15 — Öffentliche Website von WhatModels dokumentiert.** Am 2026-05-15 verlinkte eine Nachricht im WhatModels-Thread auf die öffentliche Website des Projekts. Dies legt einen datierten öffentlichen Referenzpunkt für WhatModels fest, die verfügbaren Belege belegen jedoch keinen Start, kein Release und keine Funktionsänderung.

## Was sich geändert hat {#what-changed}

2026-05-15 — WhatModels arbeitete als webbasierter Kompatibilitätsrechner für lokale LLMs. Das veröffentlichte Beispiel konfigurierte zwei RTX 5060 Ti 16 GB Karten, 16K Kontext, mindestens 10 Tokens/s und 64 GB RAM.

Nach 2026-05-15 — Wir haben über das erste Ereignis hinaus keine bestätigten datierten Releases gefunden. Die aktuelle Repository-Dokumentation beschreibt eine statische Berechnung im Browser ohne Backend oder API: Der VRAM-Bedarf setzt sich aus den Modellgewichten und dem KV-Cache zusammen, und die Generierungsgeschwindigkeit ergibt sich aus der Speicherbandbreite und der Gewichtsgröße.

## So nutzen Sie es {#how-to-use-this}

Stand 2026-05-15 können Praktiker die dokumentierte öffentliche Website von WhatModels als Einstiegspunkt zum Projekt nutzen; ihre konkreten Funktionen und ihr Release-Status müssen noch separat überprüft werden.

1. Öffnen Sie den Rechner und wählen Sie eine GPU aus der Liste oder geben Sie den verfügbaren VRAM manuell ein.
  — <https://whatmodelscanirun.com/>
2. Legen Sie den minimal akzeptablen Kontext fest; bei Auswahl einer GPU aus der Liste vergleichen Sie die geschätzten Tokens pro Sekunde.
  — <https://github.com/BenD10/whatmodels>
3. Beginnen Sie mit den Ergebnissen „Läuft gut“; prüfen Sie Optionen mit „Knappe Passung“ lokal mit dem erforderlichen Kontext und der Quantisierung.
  — <https://github.com/BenD10/whatmodels>

## Best Practices {#best-practices}

- Berücksichtigen Sie den KV-Cache zusammen mit den Gewichten: Ein Modell, das anhand der GGUF-Dateigröße passt, kann bei dem Zielkontext trotzdem den Speicher erschöpfen.
  — <https://github.com/BenD10/whatmodels>
- Behandeln Sie Geschwindigkeitsschätzungen als vorläufig: Die Generierungsgeschwindigkeit hängt von Speicherbandbreite, Quantisierung, Kontext und dem Overhead der Laufzeitengine ab.
  — <https://github.com/BenD10/whatmodels>
- Vergleichen Sie Konfigurationen mit demselben Modell und derselben Quantisierung bei demselben erforderlichen Kontext und bestätigen Sie das Ergebnis anschließend in der Zielumgebung.
  — <https://habr.com/ru/articles/1035862/>

## Durch dies ersetzt {#superseded-by-this}

- 2026-05-16 — Die Auswahl eines lokalen LLM allein nach Parameteranzahl oder Dateigröße ist für Aufgaben mit langem Kontext veraltet: Die Berechnung muss KV-Cache und Quantisierung einbeziehen.

## Weiterhin unbekannt {#still-unknown}

- Für WhatModels existiert kein primäres datiertes Changelog für Änderungen ab 2026-05-15; das GitHub-Repository zeigt den aktuellen Code, enthält im verfügbaren Material jedoch keine datierten Release-Meilensteine.
- Das ursprüngliche Schema erfasste das Ereignis vom 2026-05-15 ohne eigene Befundfelder; außerhalb dieses Ereignisses sind keine weiteren datierten Entwicklungsschritte bestätigt.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://whatmodelscanirun.com/ | What Models? — Pick the right model for your GPU in seconds | 2026-09-05 |
| https://github.com/BenD10/whatmodels | BenD10/whatmodels — Figure out what models you can run locally | 2026-09-05 |
| https://www.forum.mista.ru/topic/901896 | Confaster — ИИ-агент для 1С Конфигуратора с MCP сервером | 2026-09-05 |
| https://habr.com/ru/articles/1035862/ | Калькулятор VRAM для локальных LLM: Какие модели ИИ запустятся у вас на компьютере? | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:whatmodels`, Thread `public-website`, 1 datiertes Ereignis 2026-05-15 → 2026-05-15.
- **Praktischer Hinweis:** Stand 2026-05-15 können Praktiker die dokumentierte öffentliche Website von WhatModels als Einstiegspunkt zum Projekt nutzen; ihre konkreten Funktionen und ihr Release-Status müssen noch separat überprüft werden.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

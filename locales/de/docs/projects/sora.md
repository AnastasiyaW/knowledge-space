---
title: "Sora"
category: projects
date: 2025-09-30
tags: [project, sora, sora-access-expansion, sora-public-development]
aliases: ["Sora", "Sora 2"]
level: 4
source_sha256: 2ca1a62c4b1655791975cd267fc0edb7f40d8bca2f33eea8d646fdeae8facaa9
translation: machine
translated_at: '2026-10-24'
---
# Sora {#sora}

**Entwicklungslinie:** `project:sora` · Thread `sora-public-development`  
**Letztes Ereignis:** 2025-09-30 · 4 datierte Einträge seit 2024-02-15 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

Sora ist die Modellfamilie von OpenAI zum Erzeugen, Erweitern und Bearbeiten von kurzen Videos mit Audio auf Basis von Text- oder Bild-Prompts.

- Text-zu-Video: erzeugt Videos aus Text-Prompts.
- Bildgestützte Generierung: erzeugt Videos unter Verwendung von Referenzbildern.
- Charakterpersistenz: verwendet konsistente Charaktere über mehrere Generierungen hinweg.
- Erweiterung: verlängert bestehende Videoclips.
- Gezielte Bearbeitung: verändert bestimmte Abschnitte innerhalb eines Videos.
- MP4-Download: exportiert fertige Generierungen als Videodateien.

Sora 2 und Sora 2 Pro unterstützen Clips mit 16 und 20 Sekunden Dauer; die API ist veraltet und wird am 2026-09-24 abgeschaltet. Neue Produktionsarbeiten darauf zu starten ist nur vorübergehend möglich und riskant; bestehende Integrationen brauchen einen Migrationsplan und einen Export der Ergebnisse.

## Entwicklungslinie {#development-line}

- **2024-02-15 — OpenAI stellte Sora öffentlich vor.** Am 2024-02-15 veröffentlichte OpenAI die Projektseite zu Sora und markierte damit die öffentliche Vorstellung. Ein begleitender Social-Media-Link deutete auf zeitgleiche öffentliche Diskussion hin, ohne dass Inhalte des Beitrags vorlagen. Wir führen dies als den ersten öffentlichen Meilenstein des Projekts.
- **2024-12-09 — OpenAI dokumentierte die von Sora unterstützten Länder.** Sora Turbo startete auf sora.com für ChatGPT-Plus- und Pro-Abonnenten mit Clips bis 1080p und 20 Sekunden sowie Storyboard, Remix, Blend und Erweiterung. Der Rollout schloss zunächst das Vereinigte Königreich, die Schweiz und den EWR aus.
- **2024-12-09 — Sora erhielt einen öffentlich zugänglichen Dienst und eine Videopräsentation.** Sora Turbo startete auf sora.com für ChatGPT Plus und Pro und unterstützte Clips bis 1080p und 20 Sekunden, Storyboard, Remix, Blend und Erweiterung. Der initiale Zugang schloss das Vereinigte Königreich, die Schweiz und den EWR aus.
- **2025-09-30 — Sora stellte ein Explore-Ziel in ChatGPT bereit.** Das Release fügte Video- und Audiogenerierung, Steuerung für Multi-Shot-Regie, Charaktere und eine eigenständige Social-iOS-Anwendung hinzu. Sora 2 Pro lieferte qualitativ höherwertige Exporte in 1080p.

## Was sich geändert hat {#what-changed}

- **2024-02-15:** OpenAI stellte Sora als Forschungs-Diffusion-Transformer mit Spacetime-Patches vor. Der technische Bericht bestätigte variable Dauern, Auflösungen und Seitenverhältnisse mit einer behaupteten Maximallänge von einer Minute HD-Video, doch existierte noch kein öffentliches Produkt.
- **2024-03-14:** Ein Interview mit CTO Mira Murati, veröffentlicht am 2024-03-13, bestätigte einen geplanten öffentlichen Release im Jahr 2024, während Trainingsdaten, Fehler und Sicherheit offene Fragen blieben.
- **2024-12-09:** Die Forschungsvorschau wurde zum Produktionsmodell Sora Turbo auf sora.com für ChatGPT Plus und Pro. Zum Start umfasste Plus bis zu 50 Videos in 480p oder weniger in 720p, während Pro ein zehnfaches Volumen bot. Es erzeugte Clips bis 1080p und 20 Sekunden mit Storyboard, Remix, Blend und Erweiterung. Der Rollout schloss zunächst das Vereinigte Königreich, die Schweiz und den EWR aus.
- **2024-12-21:** Der referenzierte X-Beitrag konnte nicht verifiziert werden, weshalb für dieses Datum keine bestätigten Ergänzungen vorliegen.
- **2025-02-27:** OpenAI erweiterte die Verfügbarkeit von Sora auf die EU, das Vereinigte Königreich, die Schweiz, Norwegen, Liechtenstein und Island.
- **2025-09-30:** OpenAI veröffentlichte Sora 2 mit Video- und Audiogenerierung, Multi-Shot-Steuerung, Charakteren und einer eigenständigen Social-iOS-App. Die Produktions-API führte `sora-2` und `sora-2-pro` für Clips mit 16 und 20 Sekunden ein, wobei Sora 2 Pro qualitativ höherwertige Exporte in 1080p lieferte.
- **2026-03-25:** Die referenzierte X-Seite ließ sich nicht laden, weshalb für diesen Tag keine unabhängige datierte Klärung vorliegt.
- **2026-04-26:** OpenAI stellte die Web- und Mobilversionen der Anwendung Sora ein.
- **2026-09-05:** Die API ist weiterhin dokumentiert, aber veraltet, und ihre Abschaltung ist für den 2026-09-24 angesetzt.

## Anleitung zur Nutzung {#how-to-use-this}

Stand 2024-12-09 sollte die Verfügbarkeit von Sora in einzelnen Ländern direkt über den öffentlichen Dienst geprüft werden, statt anzunehmen, dass die Ankündigung vom Februar 2024 einen universellen Zugang implizierte.

1. Wenn Sie vor dem Abschaltdatum neue Generierungen benötigen, prüfen Sie, ob die kurze Laufzeit der API zu Ihrem Produkt passt. Verwenden Sie `sora-2` für schnelle Iterationen und `sora-2-pro` für den Export in 1080p.
  — <https://developers.openai.com/api/docs/guides/video-generation>
2. Erstellen Sie eine asynchrone Aufgabe über `POST /videos`, und geben Sie Modell, Text-Prompt, Abmessungen und Dauer an.
  — <https://developers.openai.com/api/docs/guides/video-generation>
3. Empfangen Sie das Ergebnis über den Webhook `video.completed` oder `video.failed` und laden Sie anschließend die MP4-Datei mit `GET /videos/{video_id}/content` herunter.
  — <https://developers.openai.com/api/docs/guides/video-generation>
4. Für Inhalte, die in den geschlossenen Web- oder App-Versionen von Sora erstellt wurden, öffnen Sie `sora.chatgpt.com/sunset`, wählen Sie Export und warten Sie auf die Bestätigung per E-Mail.
  — <https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation>

## Best Practices {#best-practices}

- Beginnen Sie mit kurzen, niedrig aufgelösten Clips, um Prompts, Bewegung und Komposition zu testen; reservieren Sie 1080p und längere Renderings für finale Exporte.
  — <https://developers.openai.com/api/docs/guides/video-generation>
- Geben Sie Einstellungstyp, Motiv, Handlung, Umgebung und Beleuchtung an, damit unerwünschte Details ausbleiben.
  — <https://developers.openai.com/api/docs/guides/video-generation>
- Behandeln Sie `video.failed`-Ereignisse und nutzen Sie Webhooks statt Polling in Produktionspipelines.
  — <https://developers.openai.com/api/docs/guides/video-generation>
- Reichen Sie keine menschlichen Gesichter, öffentlichen Personen, urheberrechtlich geschützten Figuren oder Musik ein, da aktuelle API-Beschränkungen solche Inhalte ablehnen.
  — <https://developers.openai.com/api/docs/guides/video-generation>
- Exportieren Sie bisherige Arbeiten und vermeiden Sie neue Abhängigkeiten von der Sora-API ohne Migrationsplan vor dem 2026-09-24.
  — <https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation>

## Hierdurch überholt {#superseded-by-this}

- 2024-02-15: Die Forschungsversion Sora mit behaupteter Einminuten-Generierung beschreibt nicht die verfügbare Sora-2-API.
- 2024-12-09: Sora Turbo und seine Stufenlimits wurden durch Sora 2 und Sora 2 Pro ersetzt und dienen nicht mehr als Integrationsleitfaden.
- 2025-09-30: Anleitungen zur Nutzung von Sora über die iOS- oder Web-Anwendungen wurden am 2026-04-26 obsolet, als diese Produkte eingestellt wurden.
- 2026-09-24: Jede Empfehlung, neue Abhängigkeiten zur Sora-Videos-API aufzubauen, wird nach der geplanten Abschaltung obsolet.

## Weiterhin ungeklärt {#still-unknown}

- Inhalte des X-Beitrags vom 2024-12-21 unter `https://x.com/rohanjamin/status/1870525134664278331?s=46&t=AR_orbfYSU6RyY_sYcnmhQ` waren zur Überprüfung nicht verfügbar, daher lässt sich eine Erweiterung des Zugangs oder eine andere Veröffentlichung nicht bestätigen.
- Das Konto `https://x.com/soraofficialapp` ließ sich am 2026-03-25 nicht öffnen; es könnte mit einer separaten App oder einem anderen Handle zusammenhängen statt mit Änderungen am Modell oder der API.
- Die offizielle Dokumentation bestätigt den Zeitplan der API-Abschaltung, doch Live-API-Aufrufe in diesem Durchgang konnten ihn nicht verifizieren.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://openai.com/index/video-generation-models-as-world-simulators/ | Video generation models as world simulators | 2026-09-05 |
| https://www.youtube.com/watch?v=mAUpxN-EIgU | OpenAI's Sora Made Me Crazy AI Videos—Then the CTO Answered (Most of) My Questions | 2026-09-05 |
| https://openai.com/index/sora-is-here/ | Sora is here | 2026-09-05 |
| https://techcrunch.com/2025/02/27/openais-sora-is-now-available-in-the-eu-uk/ | OpenAI’s Sora is now available in the EU, UK | 2026-09-05 |
| https://openai.com/index/sora-2/ | Sora 2 is here | 2026-09-05 |
| https://developers.openai.com/api/docs/guides/video-generation | Video generation with Sora | 2026-09-05 |
| https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation | What to know about the Sora discontinuation | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:sora`, Thread `sora-public-development`, 4 datierte Ereignisse 2024-02-15 → 2025-09-30.
- **Praktischer Hinweis:** Stand 2024-12-09 sollten Praktiker die aktuelle Länderverfügbarkeit von Sora prüfen und den öffentlichen Sora-Dienst nutzen, statt anzunehmen, dass die Ankündigung vom Februar 2024 einen universellen Zugang implizierte.
- **Konfidenz:** hoch. Datierte „überholt“-Einträge oben sind maßgeblich für die Frage, was veraltet ist.

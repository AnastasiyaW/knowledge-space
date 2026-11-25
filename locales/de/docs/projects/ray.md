---
title: "Ray 3.2 — Luma AI Ray-Entwicklung"
category: projects
date: 2026-06-10
tags: [luma-ray, project, ray]
aliases: ["Ray 3.2"]
level: 2
source_sha256: 1ff3cca3123e45be15e2c71401126a9b0aa20e87295171f472aa428ff2696e75
translation: machine
translated_at: '2026-10-24'
---
# Ray 3.2 — Luma AI Ray-Entwicklung {#ray-32-luma-ai-ray-development}

**Entwicklungslinie:** `project:ray` · Thread `luma-ray`  
**Letztes Ereignis:** 2026-06-10 · 1 datiertes seit 2026-06-10 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

Ray 3.2 ist Lumas Videomodell für Editoren, die echte Kamerabewegungen erhalten möchten, und für Entwickler, die Videogenerierung einbetten wollen.

- Modify Video in der Luma-App: quellgetriebenes Video-zu-Video, das einen Clip neu stylt und dabei seine Dauer beibehält.
- `ray-3.2` in der Agents API: unterstützt Text-zu-Video, Bild-zu-Video, Videobearbeitung, Verlängerung und Reframing.

Video-zu-Video in der App setzt ein Quellvideo voraus und ist auf 20 Sekunden begrenzt; API-Generierungsanfragen laufen mit 5 oder 10 Sekunden. Verwende die App, wenn die Quellaufnahme das eigentliche Asset ist. Verwende die API für automatisierte Generierung oder Bearbeitung. Die V2V-Einschränkung der App gilt nicht für die API.

## Entwicklungslinie {#development-line}

- **2026-06-10 — Luma AI stellt Ray 3.2 vor.** Am 2026-06-10 hat ein datierter Link von Luma AI Ray 3.2 innerhalb der Ray-Produktlinie als eigenständiges Update auf Versionsebene ausgewiesen. Die vorliegenden Belege belegen nicht die Fähigkeiten, Verfügbarkeit oder Migrationsfolgen der Veröffentlichung.

## Was sich geändert hat {#what-changed}

- 2026-05-27 — Luma hat Anleitungen für Ray 3.2 Modify Video in der App veröffentlicht: quellgetriebenes V2V, Ausgabe mit exakter Dauer und Multi-Keyframe-Art-Direction.
- 2026-06-10 — Das Ray3.2-Release-Event hat Multi-Keyframe-Steuerung, HDR/16-Bit-EXR, Reframe und die erste API mit voller Kontrolle eingeführt. Lumas kanonische Ankündigung ist auf 2026-06-09 datiert.
- 2026-07-13 — Lumas Statusseite führte Ray3.2 als aktuelles Videomodell und markierte Dream Machine und Ray2 als veraltet (deprecated).

## Anwendung {#how-to-use-this}

1. Wähle in der Luma-App ein Videoasset aus und öffne Modify Video → Ray 3.2 für den Standard-V2V-Workflow.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
2. Stelle einen Quellclip bereit und beschreibe anschließend den gewünschten Endzustand und/oder hänge Guide-Frame-Keyframes an exakten Quellframe-Positionen an.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
3. Verwende Motion-, Structure- und Charakter-Steuerungen nur für Eigenschaften, die den Restyle überstehen müssen; iteriere bei niedrigerer Auflösung, bevor du die finale Ausgabe erzeugst.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
4. Für eine Integration erstelle einen API-Schlüssel, sende Jobs mit `model: "ray-3.2"` an `POST /v1/generations` und wähle für die Aufgabe `video`, `video_edit` oder `video_reframe`.
  — <https://docs.agents.lumalabs.ai/>
5. Frage `GET /v1/generations/{id}` ab, bis der Status `completed` oder `failed` ist, und lade danach die fertige Ausgabe herunter; signierte Ausgabe-URLs laufen nach einer Stunde ab.
  — <https://docs.agents.lumalabs.ai/guides/model/>

## Best Practices {#best-practices}

- Formuliere für App-V2V eine konkrete, positive Beschreibung des finalen Frame-Zustands; vermeide Befehle, Verneinungen und eine neue zeitbasierte Handlung, da der Quellclip bereits Bewegung und Timing liefert.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
- Verwende Prompt plus Keyframes für gezielte Art-Direction und platziere die Keyframes an den Quellmomenten, die einen Look oder eine Komposition halten müssen.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
- Erkunde im Speed-Modus mit 540p oder 720p und wechsle dann nur die gewählte Richtung zu Quality, 1080p, HDR oder EXR, wenn die Delivery-Pipeline es erfordert.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
- Verwende für API-Bild-zu-Video entweder Start-/End-Anker oder gepaarte `keyframes` und `keyframe_indexes`; Multi-Keyframes erfordern Arrays gleicher Länge mit eindeutigen Frame-Positionen und dürfen nicht mit der Single-Anchor-Variante kombiniert werden.
  — <https://docs.agents.lumalabs.ai/guides/videos/generation/>

## Dadurch abgelöst {#superseded-by-this}

- 2026-05-27 — Für gewöhnliche V2V-Transformation wird der reine Start-/End-Workflow von Ray 3.14 Modify durch den beliebigen Multi-Keyframe-Workflow von Ray 3.2 abgelöst; Ray 3.14 bleibt die dokumentierte Ausnahme für Daueränderungen oder Looping.
- 2026-06-09 — Die Auffassung, Ray sei ein reines App-Tool ohne API mit voller Kontrolle, ist für Ray3.2 überholt.
- 2026-07-13 — Dream Machine und Ray2 sind veraltet und keine aktuellen Videomodell-Optionen von Luma mehr.

## Weiterhin unbekannt {#still-unknown}

- Das Ereignisdatum 2026-06-10 und Lumas kanonische Ankündigung vom 2026-06-09 unterscheiden sich um einen Tag; keine Quelle aus erster Hand erklärt die Differenz, daher behandeln wir sie als Datumskorrektur und nicht als zweiten Launch.
- Die angegebene URL https://lumalabs.ai/ray3-2 lieferte bei der Prüfung keine verwertbaren Inhalte und wird daher nicht als Beleg verwendet.
- Luma hat kein datiertes Changelog, das die Angabe von 16 Keyframes pro Clip aus dem Launch bzw. der Statusseite mit den 64-Anchor-Workflows der aktuellen App- und API-Dokumentation abgleicht; die Grenzwerte werden oberflächenspezifisch geführt.
- Wir haben nach dem 2026-06-10 keine datierte Modell- oder API-Veröffentlichung von Ray3.2 aus erster Hand gefunden; der Eintrag vom 2026-07-13 ist eine Aktualisierung der Statusdokumentation.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://lumalabs.ai/news/introducing-ray-3-2 | Luma Introduces Ray3.2 Model & API: Complete Creative Control for Video Generation | 2026-09-06 |
| https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video | Ray 3.2 Video to Video | Luma | 2026-09-06 |
| https://docs.agents.lumalabs.ai/guides/model/ | Models | Luma Agents | 2026-09-06 |
| https://docs.agents.lumalabs.ai/ | Quickstart | Luma Agents | 2026-09-06 |
| https://docs.agents.lumalabs.ai/guides/videos/generation/ | Video generation | Luma Agents | 2026-09-06 |
| https://lumalabs.ai/llm-info | Luma — Official Information for AI Assistants | 2026-09-06 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:ray`, Thread `luma-ray`, 1 datiertes Ereignis vom 2026-06-10 → 2026-06-10.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

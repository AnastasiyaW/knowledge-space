---
title: "WAN"
category: "projects"
date: 2026-09-26
tags: ["project", "wan", "wan-skills", "wan-video-generation"]
aliases: ["WAN", "Wan", "Wan2.2 dyno"]
level: 2
source_sha256: 843f0d7a364cd697f2a450a59c1ac122a9d34804322cf52522e7a6fad9bbfeb5
translation: machine
translated_at: '2026-10-24'
---
# WAN {#wan}

**Entwicklungslinie:** project:wan-skills · thread wan-video-generation  
**Letztes Ereignis:** 2026-09-26 · 6 datierte Einträge seit 2025-09-23 · **Recherchiert:** 2026-09-26 · Konfidenz: niedrig

## Was es ist {#what-it-is}

WAN Skills ist ein GitHub-Paket von Alibaba Wan für Entwickler von Agenten. Es enthält einen Skill für Bilderzeugung und -bearbeitung mit wan2.7 sowie einen Skill für die PPTX-Erzeugung. Es stellt Skripte für API-Aufrufe, Hilfsfunktionen für Upload und Task-Status sowie Referenzanleitungen bereit. Das öffentliche Repository listet derzeit zwei Skill-Verzeichnisse. Es eignet sich für die agentenseitige Integration der Wan-APIs. Es belegt nicht, dass das Web-Produkt von WAN einen Marktplatz für Videoeffekte veröffentlicht hat.

## Entwicklungslinie {#development-line}

- **2025-09-23 — Alibaba Wan 2.5 erscheint auf WaveSpeed als Text-zu-Video-Modell.** Am 2025-09-23 führte eine Modellroute auf WaveSpeed Alibaba Wan 2.5 als Text-zu-Video-Angebot. Damit stand Praktikern eine benannte gehostete Route für Videoerzeugung mit dieser WAN-Version zur Verfügung.
- **2025-10-01 — Wan-2.2-Lightning-Assets tauchen für Vierschritt-Workflows zur Text-zu-Video-Erzeugung auf.** Am 2025-10-01 verwiesen die verlinkten Ressourcen auf eine vierschrittige Dyno-Variante von Wan 2.2 Lightning, ein passendes FP8-Artefakt für ComfyUI und eine Workflow-Seite. Zusammen deuten sie auf einen schnelleren, workflow-tauglichen Inferenzpfad für die Text-zu-Video-Erzeugung mit Wan 2.2 hin.
- **2026-04-17 — WAN-Aktualisierung.** Wan-skills wurde öffentlich als aktualisiert gelistet, mit zwei dokumentierten Skill-Verzeichnissen: wan2.7-image-skill und wan-pptx-generator.
- **2026-07-31 — WAN stellt eine Echtzeit-Playground-Route bereit.** Am 2026-07-31 enthielt die Seite WAN Create eine Lab-Playground-Route mit der Bezeichnung realtime. Dies weist auf einen interaktiven Echtzeit-Einstiegspunkt für WAN hin, getrennt von einem Link zum Modell-Download oder zu einem Batch-Workflow.
- **2026-09-26 — WAN führt Skills-Funktion für Plattform ein.** WAN führt eine Plattformfunktion namens „skills“ ein, bestehend aus Voreinstellungen zur Videobearbeitung, die sich auf Effekte beziehen, die ursprünglich von Pika stammen. Die Einführung wird als aktuell dargestellt, obwohl sie auf Effekten des Vorjahres beruht.
- **2026-09-26 — WAN startet Skills-Funktion auf seiner Plattform.** WAN hat Skills \(Voreinstellungen zur Videobearbeitung\) auf seiner Plattform gestartet. Die Effekte werden als Effekte des Vorjahres beschrieben und sind nun als Skills umbenannt. Dies markiert einen weiteren Entwicklungsschritt des WAN-Projekts.

## Was sich geändert hat {#what-changed}

Öffentliche Belege bestätigen eine datierte Änderung an der zitierten Web-Funktion von WAN nicht unabhängig. Das separat dokumentierte Wan-skills-Repository wurde zuletzt am 2026-04-17 aktualisiert und stellt Skills für die Integration von Agenten bereit, nicht die behaupteten Plattform-Voreinstellungen.

## So wird es verwendet {#how-to-use-this}

1. Erstelle ein Alibaba-Cloud-Konto, aktiviere ModelStudio und erstelle einen DashScope-API-Schlüssel.
  — <https://github.com/Wan-Video/Wan-skills>
2. Setze DASHSCOPE\_API\_KEY und wähle die DashScope-Basis-URL für die gewünschte Region.
  — <https://github.com/Wan-Video/Wan-skills>
3. Klone Wan-skills und installiere das benötigte Skill-Verzeichnis im KI-Agenten, z. B. skills/wan2.7-image-skill.
  — <https://github.com/Wan-Video/Wan-skills>
4. Für Bildarbeiten übergib eine Textanforderung und optional Bild-URLs. Das bereitgestellte Skript sendet eine asynchrone wan2.7-image-Aufgabe und prüft deren Task-Status.
  — <https://github.com/Wan-Video/Wan-skills/blob/main/skills/wan2.7-image-skill/scripts/image-generation-editing.py>

## Bewährte Praktiken {#best-practices}

- Wähle den regionalen DashScope-Endpunkt explizit, statt dich auf eine nicht genannte Bereitstellungsregion zu verlassen.
  — <https://github.com/Wan-Video/Wan-skills>
- Behandle die Bilderzeugung als asynchron und bewahre die Task-ID auf, bis der Status ein endgültiges Ergebnis erreicht.
  — <https://github.com/Wan-Video/Wan-skills/blob/main/skills/wan2.7-image-skill/scripts/image-generation-editing.py>

## Hiermit ersetzt {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Die zitierte WAN-Webseite lieferte bei der Prüfung keinen zugänglichen Inhalt. Die behauptete Plattform-Veröffentlichung vom 2026-09-26, ihr Umfang zur Videobearbeitung, ihre Anzahl an Voreinstellungen und ein möglicher Zusammenhang mit Pika-Effekten ließen sich nicht verifizieren.
- Öffentliches Material belegt ein offizielles GitHub-Projekt namens Wan-skills, das die KI-Agenten-API-Integration für Bilderzeugung, Bildbearbeitung und PPTX-Erzeugung dokumentiert. Es belegt nicht, dass dies dasselbe Produkt wie die zitierte Seite create.wan.video/skills ist.
- Die beiden geprüften Einträge vom selben Tag beschreiben möglicherweise eine einzige, nicht verfügbare Änderung der Plattformseite und nicht zwei unabhängig unterscheidbare Veröffentlichungen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://create.wan.video/lab/skill | WAN Skills | 2026-09-27 |
| https://github.com/Wan-Video/Wan-skills | Wan-Video/Wan-skills | 2026-09-27 |
| https://github.com/wan-video | Wan-Video on GitHub | 2026-09-27 |
| https://github.com/Wan-Video/Wan-skills/blob/main/skills/wan2.7-image-skill/scripts/image-generation-editing.py | image-generation-editing.py | 2026-09-27 |

## Agenten-Kurzbriefing {#agent-brief}

- **Gegenstand:** project:wan-skills, thread wan-video-generation, 6 datierte Ereignisse 2025-09-23 → 2026-09-26.
- **Praktischer Hinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** niedrig. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

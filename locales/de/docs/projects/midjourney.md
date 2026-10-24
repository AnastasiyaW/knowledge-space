---
title: "Midjourney"
category: projects
date: 2025-04-04
tags: [midjourney, midjourney-beta-access, midjourney-model-and-feature-releases, midjourney_blend_command, midjourney_v4, midjourney_v5, project, releases]
aliases: ["Midjourney"]
level: 3
source_sha256: af03fc429e02812f57852a31c4ce74a65f57fae81841a6ee4c6bb1db9a84b678
translation: machine
translated_at: '2026-10-24'
---
# Midjourney {#midjourney}

**Entwicklungslinie:** `project:midjourney` · Thread `midjourney-model-and-feature-releases`  
**Letztes Ereignis:** 2025-04-04 · 6 datierte Einträge seit 2022-07-12 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Midjourney ist ein abonnementbasierter Generator für Bilder und Videos, der für Art Direction, Konzeptarbeit und schnelle visuelle Iteration eingesetzt wird.

- Erzeugt Standbilder aus Textprompts, Bildprompts, Stil-Referenzen, Personalisierung und Edit-Model-Referenzen.
- Unterstützt Variationen, Inpainting, Outpainting, Canvas-Erweiterung sowie die Umwandlung eines Standbilds in ein 5-Sekunden-Video.

## Entwicklungslinie {#development-line}

- **2022-07-12 — Midjourney eröffnete den Beta-Zugang.** Am 2022-07-12 begann der Beta-Zugang mit einem verkürzten Link, ohne öffentliche Angaben zu Berechtigung oder Einführung.
- **2022-11-07 — Midjourney stellte V4 vor.** Am 2022-11-07 veröffentlichte Midjourney V4 mit offiziellen Links und externer Berichterstattung; die genauen Zugangsbedingungen blieben unspezifiziert.
- **2023-01-16 — Midjourney dokumentierte den Blend-Befehl.** Am 2023-01-16 erschien Blend als nutzerseitiger Meilenstein, ohne erhaltene Quell-URL für die Einführung.
- **2023-03-09 — Midjourney eröffnete die Staging-Evaluierung für V5.** Die Ausgaben wirkten fotografischer und entsprachen den Prompts genauer, allerdings benötigten Nutzer längere Prompts für die beabsichtigte Ästhetik.
- **2023-03-16 — Midjourney dokumentierte V5.** Am 2023-03-16 markierte V5 einen wichtigen Modell-Meilenstein, ohne erhaltene URL für den Veröffentlichungszeitpunkt oder die Verfügbarkeit der Funktionen.
- **2025-04-04 — Midjourney veröffentlichte V7 Alpha.** Am 2025-04-04 verlinkte Midjourney das offizielle V7-Alpha-Update und die Imagine-Seiten und markierte damit den Meilenstein, ohne die vollständigen Kontoregeln zu beschreiben.

## Was sich änderte {#what-changed}

- **2022-07-12** — Die Notiz zum Beta-Zugang hat keine zugängliche Quelle; die offizielle Dokumentation führt V3 ab Juli 2022 als Standardmodell.
- **2022-07-26** — Keine erhaltene URL und keine bestätigte Produktänderung.
- **2022-11-07** — V4, veröffentlicht im November 2022, führte eine neue Codebasis und eine neue KI-Architektur ein, mit stärkerer Kohärenz, besserer Detailbehandlung, Bildprompting und Multi-Prompts.
- **2023-01-16** — Das Einführungsdatum von Blend ist nicht unabhängig überprüfbar; `/blend` bleibt in Discord verfügbar, um 2–5 Bilder zu kombinieren.
- **2023-03-09** — Die V5-Staging-Phase passt zur V5-Veröffentlichung im März 2023: fotografischere Ausgaben und genauere Prompt-Umsetzung, wobei für die beabsichtigte Ästhetik längere Prompts nötig sein konnten.
- **2023-03-16** — Es gibt keine erhaltene URL, die diese V5-Erwähnung von der V5-Einführung im März trennt.
- **2023-05-03** — Ein Community-Bericht behauptete eine neue Prompt-Blockade in V5.1. Die offizielle Historie datiert V5.1 auf den 4. Mai 2023 und verzeichnet stärkere Standardästhetik, Kohärenz, Interpretation natürlicher Sprache und `--tile`; die konkrete Blockade-Behauptung ist nicht verifiziert.
- **2023-08-22** — Keine erhaltene URL belegt eine eigenständige Produktänderung.
- **2025-04-04** — V7 Alpha wurde zum Testen geöffnet, mit standardmäßig aktivierter Personalisierung, Draft Mode und verbesserter Kohärenz zwischen Prompt und Bild; einige Bearbeitungsfunktionen griffen zunächst auf V6 zurück.
- **2025-06-17** — V7 wurde das Standardmodell.
- **2026-04-14 / 2026-06-10** — V8.1 startete und wurde danach Standard; es brachte schnellere Generierungen und optionale 2K-HD-Bilder.
- **2026-07-24** — V8.2 wurde das Standardmodell. Sein Edit Model ersetzte im aktuellen V8-Workflow V7 Omni Reference, Character Reference und Retexture.

## So wird es verwendet {#how-to-use-this}

Stand 2025-04-04 sollten Midjourney-Modellversionen und Alpha-Releases als getrennte Workflow-Ziele behandelt werden: Vor dem Einsatz einer Version in der Produktion die aktuelle Verfügbarkeit auf den offiziellen Update- und Imagine-Seiten prüfen.

1. Konto anlegen oder anmelden, einen Abo-Tarif wählen und die Create-Seite öffnen.  
  — <https://docs.midjourney.com/hc/en-us/articles/33329261836941-Getting-Started-Guide>
2. Im Imagine-Feld einen knappen visuellen Prompt eingeben und absenden, um einen ersten Satz Bilder zu erzeugen.  
  — <https://docs.midjourney.com/hc/en-us/articles/33390732264589-Creating-on-Web>
3. V8.2 als Standard beibehalten oder ein Modell mit `--v #` festlegen, wenn ein Projekt reproduzierbares versionsspezifisches Verhalten braucht.  
  — <https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version>
4. Bis zu vier Referenzbilder hinzufügen oder ein bestehendes Bild mit schriftlichen Anweisungen über das V8 Edit Model bearbeiten.  
  — <https://docs.midjourney.com/hc/en-us/articles/48495453462797-Edit-Model>
5. Ein vielversprechendes Ergebnis auswählen und dann Subtle- oder Strong-Variationen erstellen, statt neu zu beginnen.  
  — <https://docs.midjourney.com/hc/en-us/articles/32692978437005-Variations>
6. Wenn Bewegung benötigt wird, ein Standbild als erstes Frame verwenden und ein 5-Sekunden-Video erzeugen; Bewegungs- und Planungseinstellungen bewusst wählen, da Videos mehr GPU-Zeit verbrauchen.  
  — <https://docs.midjourney.com/hc/en-us/articles/37460773864589-Video>

## Best Practices {#best-practices}

- Kurze, konkrete visuelle Beschreibungen schreiben; nur Motiv, Medium, Umgebung, Licht, Farbe, Stimmung und Komposition angeben, soweit sie relevant sind.  
  — <https://docs.midjourney.com/docs/prompts>
- Bildprompts als Einfluss behandeln, nicht als Vorlage zum Kopieren: Jedes gewünschte Endelement im Text beschreiben und für präzise Änderungen den Editor verwenden.  
  — <https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts>
- Für einen einheitlichen Look eine Style Reference für den Stil verwenden und das gewünschte Motiv als Inhalt formulieren, nicht als Anweisung, die Referenz zu verändern.  
  — <https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference>
- `--seed` nutzen, um Prompt-Änderungen bei nahezu identischem V8-Startpunkt zu vergleichen; einen Seed nicht als wiederverwendbaren Stil oder Charakter-Lock behandeln.  
  — <https://docs.midjourney.com/hc/en-us/articles/32604356340877-Seeds>
- Ein Personalisierungsprofil oder ein Moodboard für wiederkehrende Projektästhetik aufbauen; bewusstere Bildauswahl verbessert die Passgenauigkeit des Profils.  
  — <https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization>
- Nur Bilder hochladen, für deren Nutzung man die Rechte besitzt, und externe Bildbearbeitungen innerhalb der Dienstregeln und des geltenden Rechts halten.  
  — <https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- Beta- und V3-Zugangsregeln aus 2022 sind für die Standardarbeit veraltet: Man beginnt mit einem Abo auf der Web-Create-Seite oder im Discord-Bot.
- V8.2 löst die Standardempfehlungen für V4, V5 und V5.1 ab; `--v` nur festlegen, wenn ein Projekt ein Legacy-Verhalten benötigt.
- Blend-Empfehlungen aus 2023 entsprechen nicht mehr dem Web-Workflow: Im Web mehrere Bildprompts ohne Text verwenden; `/blend` bleibt nur in Discord verfügbar.
- Das Edit Model ersetzt im V8-Workflow V7 Omni Reference, V6 Character Reference und Retexture.
- V8.2 löst V7 als Standardmodell ab; V7 bleibt als auswählbare Legacy-Version erhalten und ist nicht mehr der aktuelle Standard.

## Weiterhin unbekannt {#still-unknown}

- Die Behauptungen hinter dem Beta-Zugangsereignis vom 2022-07-12 sowie die nicht verlinkten Ereignisse vom 2022-07-26, 2023-03-16 und 2023-08-22 lassen sich anhand der verfügbaren Belege nicht rekonstruieren.
- Die Kurz-URL, die V5-Staging-Seite, die verlinkte Discord-Nachricht, der verlinkte Reddit-Beitrag und die verlinkte DTF-Seite konnten in dieser Recherche nicht abgerufen werden; ihre Behauptungen wurden nicht als sachliche Belege verwendet.
- Die offizielle aktuelle Dokumentation datiert die V7-Veröffentlichung auf 2025-04-03, während die V7-Alpha-Ankündigung auf 2025-04-04 datiert ist; die Ein-Tages-Differenz ist ungeklärt.
- Aktuelle Tarifpreise und Nutzungskontingente wurden nicht erhoben, daher wird keine bestimmte Abo-Stufe empfohlen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://docs.midjourney.com/hc/en-us/articles/33329788681101-Legacy-Features | Legacy-Funktionen – Midjourney | 2026-09-04 |
| https://updates.midjourney.com/v7-alpha/ | V7 Alpha | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version | Version – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/33329261836941-Getting-Started-Guide | Einstiegsanleitung – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/33390732264589-Creating-on-Web | Erstellen im Web – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/48495453462797-Edit-Model | Edit Model – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32692978437005-Variations | Variationen – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/37460773864589-Video | Video – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/docs/prompts | Prompt-Grundlagen – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts | Image Prompts – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference | Style Reference – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32604356340877-Seeds | Seeds – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization | Personalisierung – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor | Editor – Midjourney | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:midjourney`, Thread `midjourney-model-and-feature-releases`, 6 datierte Ereignisse vom 2022-07-12 bis 2025-04-04.
- **Praxishinweis:** Stand 2025-04-04 sollten Praktiker Midjourney-Modellversionen und Alpha-Releases als getrennte Workflow-Ziele behandeln: Vor dem Einsatz einer Version in einem Produktions-Workflow die aktuelle Verfügbarkeit über die offiziellen Update- und Imagine-Seiten prüfen.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten die datierten Abschnitte „Abgelöst durch diesen Eintrag“ als maßgeblich.

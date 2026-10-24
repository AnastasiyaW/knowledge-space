---
title: "Adobe Firefly Video Model — Rollout des Firefly Video Model"
category: projects
date: 2024-10-14
tags: [adobe-firefly-video-model, adobe_firefly, firefly-video-model-rollout, project]
aliases: ["Adobe Firefly Video", "Adobe Firefly Video Model"]
level: 3
source_sha256: bc85afd17b65aec9d8e00189b769a96375b2d09bb1993044fc9602322f9c1da0
translation: machine
translated_at: '2026-10-24'
---
# Adobe Firefly Video Model — Rollout des Firefly Video Model {#adobe-firefly-video-model-firefly-video-model-rollout}

**Entwicklungslinie:** `project:adobe-firefly-video-model` · Thread `firefly-video-model-rollout`  
**Letztes Ereignis:** 2024-10-14 · 2 datierte seit 2024-09-11 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

Adobe Firefly Video Model erzeugt kurze Clips aus Text und Bildern. In Generate video steht es neben Partnermodellen, daher wählen wir Firefly Video explizit aus.

- Text-to-Video und Image-to-Video mit erstem und letztem Keyframe.
- Steuerung von Seitenverhältnis, Auflösung, Shot size, Kamerawinkel, Kamerabewegung und Stil.
- Export oder Übertragung von Clips in den Firefly-Videoeditor und Premiere.

Clips sind 5 Sekunden lang, laufen mit 24 fps und liegen in 540p, 720p oder 1080p sowie in den Seitenverhältnissen 16:9, 9:16 oder 1:1 vor; höhere Auflösung verbraucht mehr generative Credits. Für geplante Einstellungen, Übergänge und B-Roll einsetzen; längere Szenen werden im Editor aus einzelnen Clips zusammengesetzt.

## Entwicklungslinie {#development-line}

- **2024-09-11 — Adobe kündigt ein kommendes Videomodell für Firefly an.** Am 2024-09-11 gab Adobe bekannt, dass für Firefly ein Videomodell geplant ist. Damit wurde die Produktrichtung festgelegt, bevor Nutzer Zugang zur Videogenerierung hatten.
- **2024-10-14 — Adobe führt eine Beta-Videogenerierung in Firefly ein.** Am 2024-10-14 eröffnete Adobe in der Firefly-Webanwendung eine Beta-Oberfläche zur Videogenerierung. Das Modell ging damit von der Ankündigung in den Nutzertest über.

## Was sich geändert hat {#what-changed}

Adobe Firefly Video Model ging von der ersten Ankündigung in die allgemeine Verfügbarkeit innerhalb der Oberfläche Generate video über, die mehrere Modelle unterstützt.

- **2024-09-11:** Adobe kündigte das Modell an und eröffnete eine Warteliste. Versprochen wurden Text-to-Video, Image-to-Video, Referenzbilder und Kamerasteuerung für B-Roll und zum Schließen redaktioneller Lücken.
- **2024-10-14:** Ausgewählte Community-Mitglieder erhielten frühen Zugang in der Firefly-Webanwendung und setzten Text-to-Video und Image-to-Video für Inserts und neue Elemente in bestehendem Material ein.
- **2025-02-12:** Die öffentliche Beta startete in der aktualisierten Firefly-Webanwendung mit Text- und Bildgenerierung und 1080p zum Start.
- **2025-04-24:** Adobe überführte Firefly Video Model aus der Beta in die allgemeine Verfügbarkeit.
- **2025-07-17:** Adobe verbesserte die Bewegungsgenauigkeit, erweiterte die Videosteuerung, ergänzte die Generierung von Soundeffekten und erweiterte die Auswahl an Partnermodellen in der Oberfläche.
- **2026-08-18–19:** Die aktuelle Dokumentation führt Firefly Video als explizite Modellwahl in Generate video auf, während der einheitliche Arbeitsbereich für Generierung und Bearbeitung weiterhin in der Beta ist.

## So wird es verwendet {#how-to-use-this}

Stand 2024-10-14 ließ sich die Videogenerierung mit Firefly als Beta-Workflow in der Firefly-Webanwendung nutzen; am 2024-09-11 war sie nur eine angekündigte Funktion.

1. Öffnen Sie Firefly, wählen Sie Video → Generate video und wählen Sie unter Model Firefly Video; die Oberfläche kann beim ersten Start standardmäßig Veo 3.1 vorauswählen.
  — <https://helpx.adobe.com/sg/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-text-prompts.html>
2. Legen Sie Auflösung, Seitenverhältnis, Shot size, Camera angle und Motion fest. Firefly Video unterstützt 540p, 720p oder 1080p sowie 16:9, 9:16 oder 1:1.
  — <https://helpx.adobe.com/firefly/web/work-with-audio-and-video/work-with-video/use-style-presets-for-video-generation.html>
3. Schreiben Sie einen Prompt nach dem Schema shot + subject + action + location + aesthetic und legen Sie danach Stil und Kamerabewegung fest.
  — <https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html>
4. Für einen kontrollierten Übergang laden Sie ein erstes Bild, ein letztes Bild oder beide hoch. Bei zwei Bildern beschreiben Sie den Übergang im Text.
  — <https://helpx.adobe.com/in/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-images.html>
5. Generieren Sie den Clip und laden Sie ihn herunter oder fügen Sie ihn Project media, Timeline oder dem Clip-Editor für die weitere Montage hinzu.
  — <https://helpx.adobe.com/firefly/web/unified-generation-and-editing-experience/generate-and-edit-content.html>
6. Prüfen Sie den Credit-Verbrauch vor dem Start über die Schaltfläche neben Generate; die Kosten hängen von der gewählten Auflösung ab.
  — <https://helpx.adobe.com/firefly/web/work-with-audio-and-video/work-with-video/use-style-presets-for-video-generation.html>

## Bewährte Vorgehensweisen {#best-practices}

- Formulieren Sie Prompts präzise: shot, subject, action, location, light, color und style. Mehr als vier Subjekte verwirren das Modell oft.
  — <https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html>
- Beschreiben Sie Aktion mit Verben und Tempo und legen Sie Kamerabewegung entweder im Prompt oder über die Camera control fest.
  — <https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html>
- Verfeinern Sie einen Basis-Prompt, indem Sie entlang einer Dimension Details ergänzen, und speichern Sie Seed, Prompt und Einstellungen für ähnliche Ergebnisse.
  — <https://helpx.adobe.com/sg/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-text-prompts.html>
- Verwenden Sie für Image-to-Video optisch kompatible Keyframes und beschreiben Sie den Übergang. Ein erstes Bild deaktiviert einige manuelle Steuerungen, ein letztes Bild deaktiviert Motion.
  — <https://helpx.adobe.com/in/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-images.html>
- Laden Sie nur Bilder hoch, für die Sie Nutzungsrechte besitzen. Lassen Sie den Browser-Tab geöffnet und vermeiden Sie gleichzeitige Generierungen in mehreren Tabs.
  — <https://helpx.adobe.com/cn/firefly/web/work-with-audio-and-video/work-with-video/about-generate-video.html>

## Überholte Angaben {#superseded-by-this}

- 2024-09-11: Der Status „demnächst verfügbar“ und die reine Wartelistenphase endeten mit der öffentlichen Beta am 2025-02-12 und der allgemeinen Verfügbarkeit am 2025-04-24.
- 2024-10-14: Früher Zugang für ausgewählte Community-Mitglieder ist überholt; Zugang auf Kontoebene und die allgemeine Verfügbarkeit am 2025-04-24 haben ihn ersetzt.
- 2025-02-12: Der Status „öffentliche Beta“ ist nach der allgemeinen Verfügbarkeit am 2025-04-24 überholt.
- 2025-02-12: Die Zusage „4K demnächst“ ist keine aktuelle Einstellung von Firefly Video. Die Dokumentation vom 2026-08-18 führt für diesen Workflow 540p, 720p und 1080p auf.

## Weiterhin unbekannt {#still-unknown}

- Konkrete verfügbare Modelle, Image-to-Video, Credit-Kosten und Kontoberechtigungen wurden nicht auf einem aktiven Konto geprüft. Adobe knüpft den Zugang an Tarif, Region, Nutzertyp und regulatorische Beschränkungen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://blog.adobe.com/en/publish/2024/09/11/bringing-gen-ai-to-video-adobe-firefly-video-model-coming-soon | Bringing generative AI to video with Adobe Firefly Video Model | Adobe Blog | 2026-09-04 |
| https://blog.adobe.com/en/publish/2024/10/14/generate-video-beta-on-firefly-web-app | Generate Video (beta) on Firefly Web App | Adobe Blog | 2026-09-04 |
| https://blog.adobe.com/en/publish/2025/02/12/meet-firefly-video-model-ai-powered-creation-with-unparalleled-creative-control | Meet Firefly Video Model: AI-Powered creation with unparalleled creative control | Adobe Blog | 2026-09-04 |
| https://news.adobe.com/news/2025/04/adobe-revolutionizes-ai-assisted-creativity-firefly | Adobe Revolutionizes AI-Assisted Creativity with Firefly, the All-In-One Home for AI Content Creation, with New Partner and Firefly Models | 2026-09-04 |
| https://blog.adobe.com/en/publish/2025/07/17/firefly-adds-new-video-capabilities-industry-leading-ai-models-generate-sound-effects-feature | Firefly adds new video capabilities, industry leading AI models, and Generate Sound Effects feature | Adobe Blog | 2026-09-04 |
| https://helpx.adobe.com/sg/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-text-prompts.html | Generate videos using text prompts | Firefly | 2026-09-04 |
| https://helpx.adobe.com/in/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-images.html | Generate videos using images | Firefly | 2026-09-04 |
| https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html | Writing effective text prompts for video generation | Firefly | 2026-09-04 |
| https://helpx.adobe.com/firefly/web/work-with-audio-and-video/work-with-video/use-style-presets-for-video-generation.html | Use style presets for video generation | Firefly | 2026-09-04 |
| https://helpx.adobe.com/firefly/web/unified-generation-and-editing-experience/generate-and-edit-content.html | Generate and edit images and videos in Firefly | Firefly | 2026-09-04 |
| https://helpx.adobe.com/cn/firefly/web/work-with-audio-and-video/work-with-video/about-generate-video.html | 生成视频常见问题 | Firefly | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:adobe-firefly-video-model`, Thread `firefly-video-model-rollout`, 2 datierte Ereignisse 2024-09-11 → 2024-10-14.
- **Praxishinweis:** Stand 2024-10-14 ließ sich die Videogenerierung mit Firefly als Beta-Workflow in der Firefly-Webanwendung nutzen; am 2024-09-11 war sie nur eine angekündigte Funktion.
- **Konfidenz:** hoch. Die datierten Angaben zu Überholungen oben sind maßgeblich dafür, was veraltet ist.

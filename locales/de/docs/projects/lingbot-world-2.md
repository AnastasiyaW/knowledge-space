---
title: "LingBot-World 2.0"
category: projects
date: 2026-07-09
tags: [lingbot-world, lingbot-world-2, lingbot-world-2-development, project]
aliases: ["LingBot-World 2.0"]
level: 2
source_sha256: 7a51723070bff0da9e3c7aa8ee04c60cd512f8076efc2bd7fe527217edb07f2d
translation: machine
translated_at: '2026-10-24'
---
# LingBot-World 2.0 {#lingbot-world-20}

**Entwicklungslinie:** `project:lingbot-world-2` · Thread `lingbot-world-2-development`  
**Letztes Ereignis:** 2026-07-09 · 1 datiertes Ereignis seit 2026-07-09 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

LingBot-World 2.0, auch LingBot-World-Infinity genannt, erzeugt navigierbare Bild-zu-Video-Welten für Forscher und Entwickler. Es unterstützt unbegrenztes Streaming, Action-Conditioning und ein Pilot- bzw. Director-Agent-Harness. Der öffentliche lokale Checkpoint ist `robbyant/lingbot-world-v2-14b-causal-fast` (14B). Das Repository dokumentiert Inferenz mit 480p auf mehreren GPUs, während Reactor `reactor/lingbot-world-2` mit 1664×960 und 48 fps hostet. Wir nutzen Reactor für Prototypen und das 14B-Repository-Release für nicht-kommerzielle Forschung, nicht für selbst gehostetes Echtzeit-Deployment.

## Entwicklungslinie {#development-line}

- **2026-07-09 — Öffentliche Entwicklungsressourcen für LingBot-World 2.0 wurden verlinkt.** Am 2026-07-09 verknüpfte ein Eintrag LingBot-World 2.0 mit der Projektseite, dem GitHub-Repository, der Hugging-Face-Collection und der Reactor-Seite. Das markiert einen öffentlichen Meilenstein, wobei die Quelle keine Details zu Release-Inhalten, Fähigkeiten oder Betriebsstatus nennt.

## Was sich geändert hat {#what-changed}

- **2026-07-08** — Der technische Bericht erschien auf arXiv und beschreibt das 14B-Modell sowie ein geplantes 1.3B-Pendant.
- **2026-07-09** — LingBot-World 2.0 veröffentlichte Bericht, Code und Modelle. Der offene Arbeits-Checkpoint war `lingbot-world-v2-14b-causal-fast`. Die Varianten 14B causal-pretrain, 14B bidirectional und 1.3B blieben als TODO gelistet. Das Release ergänzte kausale Langhorizont-Generierung, eine destillierte Echtzeitvariante, Action- und Text-Steuerung, Multiplayer-Unterstützung und ein Pilot/Director-Harness.
- **2026-07-10** — Das Repository benannte eine kausale Klasse aus Gründen der Code-Wartung um, ohne neue Fähigkeit.
- **2026-07-14** — Das Repository überarbeitete eine Video-Prompt-Beschreibung in der Dokumentation, ohne neues Modell-Release.

## So verwendest du es {#how-to-use-this}

Stand 2026-07-09 solltest du LingBot-World 2.0 als eigenständige Linie behandeln. Prüfe Projektseite, Repository, Modell-Collection und Reactor-Dokumentation, bevor du es einsetzt.

1. Für einen gehosteten Prototyp erstelle ein Reactor-Gerüst mit `npx create-reactor-app my-lingbot-world-2-app --model=lingbot-world-2`.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
2. Öffne eine Session mit dem Modellnamen `reactor/lingbot-world-2`, lade ein Referenzbild hoch, setze einen Text-Prompt und sende dann `start`. Die Generierung schlägt fehl, solange Bild und Prompt nicht beide vorhanden sind.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
3. Steuere die laufende Welt mit longitudinaler und lateraler Bewegung, Blicksteuerung oder `set_camera_pose`. Aktualisiere Bedingungen während des Streams mit `set_prompt`.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
4. Für lokale Forschungsinferenz klone das Repository, installiere die Anforderungen mit Torch 2.4+ und FlashAttention, lade `robbyant/lingbot-world-v2-14b-causal-fast` herunter und führe dann das mitgelieferte Multi-GPU-Kommando für causal-fast oder `run_fast.sh` aus.
  — <https://github.com/robbyant/lingbot-world-v2>

## Best Practices {#best-practices}

- Trenne Prompts in Basis-, Kamera-, Bewegungs-, Ereignis- und vertikale Steuerungsebenen. Halte jede Ebene auf einer Steuerachse, damit Prompts nicht mit der aktiven Bewegung in Konflikt geraten.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/prompt-guide>
- Halte die Gesamtlänge des Prompts unter etwa 2.000 Zeichen. Kürze Ereignisklauseln, bevor du Basis-Identität oder Steuerregeln kürzt.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/prompt-guide>
- Behandle Bewegung als persistenten Zustand und sende einen expliziten Leerlaufbefehl. Kurze Impulse können die Chunk-Grenze verfehlen.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
- Erwarte keinen offiziellen Deployment-Code für das offene Modell. Das Repository hält ihn zurück, und die Lizenz ist CC BY-NC-SA 4.0 für nicht-kommerzielle Nutzung.
  — <https://github.com/robbyant/lingbot-world-v2>

## Dadurch abgelöst {#superseded-by-this}

- **2026-07-09** — Die Hinweise zu LingBot-World 1.0 sind auf Reactor veraltet. World 2 ersetzt sie durch Zwei-Achsen-Navigation, Kameraposen und Prompt-Steuerung während des Streams.
- **2026-07-09** — Die Erwartung, dass alle angekündigten 14B- und 1.3B-Modelle heruntergeladen werden können, ist veraltet. Nur der 14B-causal-fast-Checkpoint ist öffentlich; die übrigen bleiben TODO.

## Weiterhin unbekannt {#still-unknown}

- Der Beitrag vom 9. Juli behauptet, das Echtzeitmodell laufe mit 720p und 60 fps, während Reactor 1664×960 bei 48 fps angibt. Die Quellen enthalten keinen direkten Vergleich.
- Das Repository hält Deployment-Code zurück. Hardware-Anforderungen, Serving-Stack und Latenz für offizielles Echtzeit-Serving sind weiterhin nicht dokumentiert.
- Das arXiv-Paper beschreibt ein 1.3B-Pendant, doch die TODO-Liste des Repositorys vom 9. Juli enthält weder herunterladbare 1.3B-Gewichte noch Code.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://technology.robbyant.com/lingbot-world-v2 | LingBot-World 2.0 project page | 2026-09-05 |
| https://github.com/robbyant/lingbot-world-v2 | Robbyant/lingbot-world-v2 | 2026-09-05 |
| https://huggingface.co/collections/robbyant/lingbot-world-v2 | LingBot-World-V2 collection | 2026-09-05 |
| https://www.reactor.inc/lingbot-world-2 | LingBot World 2 — Reactor | 2026-09-05 |
| https://arxiv.org/abs/2607.07534 | Infinite Worlds with Versatile Interactions | 2026-09-05 |
| https://github.com/robbyant/lingbot-world-v2/commits/main | LingBot-World-V2 commit history | 2026-09-05 |
| https://huggingface.co/robbyant/lingbot-world-v2-14b-causal-fast | robbyant/lingbot-world-v2-14b-causal-fast | 2026-09-05 |
| https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview | LingBot World 2 overview | 2026-09-05 |
| https://docs.reactor.inc/model-api-reference/lingbot-world-2/prompt-guide | LingBot World 2 prompt guide | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:lingbot-world-2`, Thread `lingbot-world-2-development`, 1 datiertes Ereignis 2026-07-09 → 2026-07-09.
- **Praktischer Hinweis:** Stand 2026-07-09 solltest du LingBot-World 2.0 als eigenständige Linie behandeln. Prüfe Projekt, Code, Collection und Produktdokumentation, bevor du es einsetzt.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

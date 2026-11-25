---
title: "Alibaba — Forschung zu generativen Modellen"
category: organizations
tags: [alibaba, alibaba:mofusion, alibaba_latent_to_pixel, generative-model-research, humanomniv2, organization]
aliases: ["Alibaba"]
level: 3
source_sha256: 28bbaa01ab471f806049beba20d436f43945fadea07eb788e4ea2212558d189f
translation: machine
translated_at: '2026-10-24'
---
# Alibaba — Forschung zu generativen Modellen {#alibaba-generative-model-research}

**Entwicklungslinie:** `organization:alibaba` · Thread `generative-model-research`  
**Ereignisse:** 3 datierte, 2022-12-11 → 2026-08-23 · **Recherchiert:** 2026-09-03 · Konfidenz: mittel

## Was es ist {#what-it-is}

Alibaba ist kein einzelnes KI-Werkzeug, sondern eine Sammlung von Forschungsergebnissen für R&D-Teams: — MoFusion — Diffusionsmodell für Text-to-Motion, Motion Completion und die Mischung von Steuersignalen. — HumanOmniV2 — Open-Weight-Modell für Schlussfolgerungen über Bilder, Video und Audio unter Berücksichtigung des vollständigen Kontexts. — Latent-to-Pixel — Trainingsrezept für ein Text-to-Image-Modell: zuerst Latent Space, dann Pixel Space. Einschränkung: Von diesen drei Arbeiten veröffentlicht nur HumanOmniV2 Code, Gewichte und einen Evaluation-Workflow; der Eintrag gibt 9B BF16 an und keinen gehosteten Inference-Provider. Fazit: HumanOmniV2 eignet sich für einen lokalen Forschungslauf; die beiden anderen Arbeiten dienen als Forschungsgrundlagen, nicht als fertiger Ersatz für ein Production-Werkzeug.

## Entwicklungslinie {#development-line}

- **2022-12-11 — Die Entwicklungslinie von Alibaba erfasste das MoFusion-Projekt.** Am 2022-12-11 erfasste die Alibaba-Entwicklungslinie einen Link zum MoFusion-Projekt. Dies wird als wesentlicher Forschungs- und Entwicklungs-Checkpoint behandelt, weil die versiegelten Belege ein benanntes Projektartefakt identifizieren. Die vorliegenden Belege belegen nicht Wortlaut, Urheberschaft oder Einsatzstatus des ursprünglichen Beitrags.
- **2025-07-09 — Die Entwicklungslinie von Alibaba erfasste Forschungsressourcen zu HumanOmniV2.** Am 2025-07-09 erfasste die Alibaba-Entwicklungslinie Links zu Forschungsressourcen von HumanOmniV2, darunter eine Paper-Seite und das Quell-Repository. Dies wird als wesentlicher Checkpoint behandelt, weil die datierten Links ein benanntes Forschungsartefakt mit zugehörigem Code identifizieren. Die versiegelten Belege belegen nicht Wortlaut, Urheberschaft, technische Aussagen oder Veröffentlichungsstatus des ursprünglichen Beitrags.
- **2026-08-23 — Die Entwicklungslinie von Alibaba erfasste ein Latent-to-Pixel-Paper.** Am 2026-08-23 erfasste die Alibaba-Entwicklungslinie einen Link zu einem Latent-to-Pixel-Paper. Dies wird als wesentlicher Forschungs-Checkpoint in der Linie zu generativen Modellen behandelt, nicht als Behauptung über eine Produktveröffentlichung. Die vorliegenden Belege belegen nicht Wortlaut, Urheberschaft, technische Aussagen oder Verfügbarkeit des ursprünglichen Beitrags.

## Was sich geändert hat {#what-changed}

Die Linien von Alibaba entwickeln sich parallel, nicht als aufeinanderfolgende Versionen eines einzelnen Produkts. — 2022-12-11: MoFusion schlug ein einheitliches vortrainiertes Diffusion Transformer für Aufgaben der Bewegungssynthese vor, mit Cross-Attention für verschiedene Steuerungen und einem Skelett-Adapter. — 2025-07-09: HumanOmniV2 ergänzte kontextorientiertes omni-modales Reasoning: kontextuelle und logische Rewards, IntentBench und einen offenen Forschungsstack für Video-, Audio- und Bildaufgaben. — 2026-08-23: Eine Arbeit zu Diffusion im Pixel Space zeigte, dass direktes großskaliges Pre-Training im Pixelraum langsamer konvergiert; vorgeschlagen wird ein Übergang von Latent zu Pixel während des Post-Trainings, mit einer angegebenen Beschleunigung der End-to-End-Inferenz um den Faktor 3,18–4,75. — Heute gefunden, 2026-09-03: Das MoFusion-Repository ist archiviert und nur lesbar; HumanOmniV2 veröffentlicht Gewichte, Code und Daten; für das Paper 2608.16887 sind zum Zeitpunkt der Prüfung kein Modell, Datensatz oder Space verknüpft.

## Verwendung {#how-to-use-this}

Stand 2026-08-23 sollten Praktiker, die Alibaba verfolgen, die datierten Artefakte MoFusion, HumanOmniV2 und Latent-to-Pixel als Forschungslinie behandeln und jedes Paper bzw. Repository direkt prüfen, bevor sie es als Grundlage für Implementierung oder Deployment verwenden.

1. Wenn ein lauffähiges Artefakt aus dieser Linie benötigt wird, beginnen Sie mit HumanOmniV2: Klonen Sie das Repository der Autoren und laden Sie die Gewichte über die angegebenen Links auf Hugging Face oder ModelScope.
  — <https://github.com/HumanMLLM/HumanOmniV2>
2. Für eine reproduzierbare Evaluation laden Sie IntentBench, Daily-Omni und WorldSense herunter, geben Sie die Pfade zu den Videos an und starten Sie die bereitgestellte verteilte Evaluation; das Beispiel verwendet 8 Prozesse.
  — <https://github.com/HumanMLLM/HumanOmniV2>
3. Für das Training laden Sie die Long-CoT-Daten und die angegebenen Datensätze herunter, setzen Sie JSON- und Video-Pfade in den YAML-Konfigurationen und führen Sie SFT, Stage-1-RL und Stage-2-RL in der dokumentierten Reihenfolge aus.
  — <https://github.com/HumanMLLM/HumanOmniV2>
4. Für neue Text-to-Image-Forschung und -Entwicklung verwenden Sie Pre-Training im Latent Space und passen das Modell anschließend separat an den Pixel Space an; dabei handelt es sich um ein Trainingsrezept, nicht um einen veröffentlichten, fertigen Inference-Endpunkt.
  — <https://arxiv.org/pdf/2608.16887>

## Best Practices {#best-practices}

- Für Video- und Audio-Reasoning bilden Sie zuerst den vollständigen multimodalen Kontext und antworten erst danach: Die Arbeit zielt gezielt auf übersehene visuelle und auditive Signale ab.
  — <https://arxiv.org/pdf/2506.21277>
- Bewerten Sie HumanOmniV2 nicht anhand eines einzelnen bequemen Beispiels: Verwenden Sie IntentBench zusammen mit Daily-Omni und WorldSense und prüfen Sie vorher die Video-Pfade.
  — <https://github.com/HumanMLLM/HumanOmniV2>
- Trennen Sie die Rechte an Code, Gewichten und Videos: Code und Modell sind als Apache-2.0 ausgewiesen, die selbst zusammengestellten Videos unter CC BY-NC-SA 4.0.
  — <https://huggingface.co/PhilipC/HumanOmniV2>
- Behandeln Sie IntentBench als eigenständigen Datensatz mit Einschränkungen für nicht-kommerzielle Nutzung und Bearbeitungen (non-commercial/no-derivatives) und prüfen Sie die Zulässigkeit der Nutzung vor Training oder kommerzieller Anwendung.
  — <https://huggingface.co/datasets/PhilipC/IntentBench>
- Übernehmen Sie beim Latent-to-Pixel-Ansatz den Noise Scale nicht als theoretische Konstante: Die Autoren erzielten das beste Ergebnis mit gamma=2 in ihrem Setup und fordern ausdrücklich eine empirische Kalibrierung.
  — <https://arxiv.org/pdf/2608.16887>

## Dadurch überholt {#superseded-by-this}

- 2023-02-28 — Die Annahme, dass MoFusion ein aktiv gepflegter offizieller Implementierungspfad ist, ist überholt: Das Repository ist archiviert und nur lesbar.
- 2025-07-01 — Der Zustand von HumanOmniV2 „nur Paper und ein Teil des Codes“ wurde durch veröffentlichten Training- und Evaluation-Code, Gewichte, IntentBench und Trainingsdaten ersetzt.
- Es ist nicht belegt, dass MoFusion, HumanOmniV2 und die Latent-to-Pixel-Arbeit einander ersetzen: Es handelt sich um unterschiedliche Aufgaben und Modalitäten, daher ist eine Migration zwischen ihnen kein Upgrade-Pfad.

## Weiterhin unbekannt {#still-unknown}

- MoFusion, HumanOmniV2 und die Arbeit zum Pixel Space sind durch die gemeinsame Zugehörigkeit zu Alibaba verbunden, aber die Primärquellen zeigen kein gemeinsames Modell, keine gemeinsame API und keine gemeinsame Produkt-Roadmap.
- Für das Paper 2608.16887 wurde kein offizieller Code, keine Gewichte, kein Datensatz und kein Serving-Endpunkt gefunden; praktische Reproduzierbarkeit erfordert eine eigene Implementierung.
- Für HumanOmniV2 sind Training- und Evaluation-Workflows veröffentlicht, aber kein vom Autorenteam bereitgestellter Quickstart für Endnutzer-Inferenz; das generische Transformers-Snippet auf Hugging Face wurde nicht unabhängig ausgeführt.
- Die aktuelle Kompatibilität des archivierten MoFusion mit modernen Abhängigkeiten und seine Eignung für den Production-Einsatz sind nicht bestätigt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://ofa-sys.github.io/MoFusion/ | MoFusion: Pretrained Diffusion Models for Unified Human Motion Synthesis | 2026-09-03 |
| https://github.com/OFA-Sys/MoFusion | OFA-Sys/MoFusion | 2026-09-03 |
| https://arxiv.org/pdf/2212.02837 | Pretrained Diffusion Models for Unified Human Motion Synthesis | 2026-09-03 |
| https://huggingface.co/papers/2506.21277 | Paper-Seite — HumanOmniV2: From Understanding to Omni-Modal Reasoning with Context | 2026-09-03 |
| https://arxiv.org/pdf/2506.21277 | HumanOmniV2: From Understanding to Omni-Modal Reasoning with Context | 2026-09-03 |
| https://github.com/HumanMLLM/HumanOmniV2 | HumanMLLM/HumanOmniV2 | 2026-09-03 |
| https://huggingface.co/PhilipC/HumanOmniV2 | PhilipC/HumanOmniV2 | 2026-09-03 |
| https://huggingface.co/datasets/PhilipC/IntentBench | PhilipC/IntentBench | 2026-09-03 |
| https://huggingface.co/papers/2608.16887 | Paper-Seite — An Empirical Study of Training Pixel-Space Text-to-Image Diffusion Models | 2026-09-03 |
| https://arxiv.org/pdf/2608.16887 | An Empirical Study of Training Pixel-Space Text-to-Image Diffusion Models | 2026-09-03 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `organization:alibaba`, Thread `generative-model-research`, 3 datierte Ereignisse 2022-12-11 → 2026-08-23.
- **Praktischer Hinweis:** Stand 2026-08-23 sollten Praktiker, die Alibaba verfolgen, die datierten Artefakte MoFusion, HumanOmniV2 und Latent-to-Pixel als Forschungslinie behandeln und jedes Paper bzw. Repository direkt prüfen, bevor sie es als Grundlage für Implementierung oder Deployment verwenden.
- **Konfidenz:** mittel. Die datierten Überholungen oben sind maßgeblich dafür, was veraltet ist.

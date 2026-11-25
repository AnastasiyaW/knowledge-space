---
title: "MiniMax-H3 Turbo LoRA"
category: projects
date: 2026-08-06
tags: [minimax-h3-turbo-lora, minimax_h3_turbo_lora, project]
aliases: ["MiniMax-H3 Turbo LoRA"]
level: 2
source_sha256: 806ab26f3197dcf77473d6886509367823a094edbc3813fdb6ad37beb1a37ca5
translation: machine
translated_at: '2026-10-24'
---
# MiniMax-H3 Turbo LoRA {#minimax-h3-turbo-lora}

**Entwicklungslinie:** `project:minimax-h3-turbo-lora` · Thread `minimax-h3-turbo-lora`  
**Letztes Ereignis:** 2026-08-06 · 1 datiertes seit 2026-08-06 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

MiniMax-H3 Turbo LoRA ist ein Community-Adapter mit ComfyUI-Nodes für Text-zu-Video- und Bild-zu-Video-Workflows mit MiniMax-H3.

- Gemeinsames Audio-Video-Sampling mit weniger Schritten.
- Grundlegende Unterstützung für vollständige und gekürzte (pruned) H3-Modelle.
- Eigener Sampler für getrennte Audio- und Video-Zeitpläne.

Praktisches Sampling benötigt mindestens 4 Schritte, bevorzugt 6–8 Schritte; Audio und intensive Bewegung befinden sich weiterhin in einer Vorschauphase. Verwende es für schnelle Iterationen, validiere Aufnahmen mit schneller Bewegung jedoch gegen den Basis-Workflow.

## Entwicklungslinie {#development-line}

- **2026-08-06 — Ressourcenbündel für MiniMax-H3 Turbo LoRA dokumentiert.** Am 2026-08-06 verknüpfte die Dokumentation die Modellressource MiniMax-H3 Turbo LoRA mit einem Demo-Space, einem ComfyUI-Integrations-Repository und einer auf ComfyUI ausgerichteten Modellressource. Damit entsteht ein zugänglicher Workflow über Modellverteilung, Demonstration und ComfyUI-Nutzung hinweg. Die verlinkten Ressourcen allein belegen jedoch weder ihre einzelnen Veröffentlichungsdaten, Versionen, Urheberschaft noch Leistungsaussagen.

## Was sich geändert hat {#what-changed}

- 2026-08-06 — Die öffentliche ComfyUI-Integration ergänzte den Turbo-LoRA-Loader und den 4-Schritt-Sampler und fügte danach Unterstützung für gekürzte bzw. Curve-Basen, die Anwendung des Adapters zur Laufzeit sowie einen Schalter für geringen VRAM-Bedarf hinzu.
- 2026-08-07 — Der v4-EMA-Checkpoint bei Schritt 600 wurde zur Standardempfehlung; die Empfehlung beschränkte das praktische Sampling auf 4–8 Schritte und behielt v1 bei Schritt 850 nur für starke Bewegung bei vier Schritten bei.
- 2026-08-08 — Die Node-Integration behob eine Diskrepanz bei der AdaLN-Injektion für die Konditionierung mit Audio-Referenz.
- 2026-08-10 — Die Integration korrigierte die Berechnung der Modulationssegmente über die Nachschlagetabelle der AdaLN-Zeit.
- 2026-08-12 — Die Integration übernahm eine Korrektur der AdaLN-Zeile für Audio-Referenzen.
- 2026-08-14 — Die Integration übernahm einen weiteren Beitrag aus dem Upstream; der benutzerdefinierte Node sollte aktuell gehalten werden.

## Anwendung {#how-to-use-this}

Ab 2026-08-06 sollte MiniMax-H3 Turbo LoRA über den verlinkten Modell- und ComfyUI-Integrationspfad bewertet werden, nicht als isolierter Checkpoint; Kompatibilität, Lizenzierung und Setup-Anforderungen sind vor der Verwendung anhand des aktuellen Stands zu prüfen.

1. Installiere `Larryvrh/ComfyUI-MiniMax-H3-Turbo` über ComfyUI-Manager oder klone es nach `ComfyUI/custom_nodes`, und starte anschließend ComfyUI neu.
  — <https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo>
2. Lade die Turbo-LoRA-`.safetensors` nach `ComfyUI/models/loras/` herunter und installiere das MiniMax-H3-Basismodell, die VAEs und den Text-Encoder.
  — <https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora>
3. Beginne mit einem offiziellen H3-Text-zu-Video- oder Bild-zu-Video-Workflow; platziere den Turbo-LoRA-Node zwischen dem Diffusionsmodell-Loader und `SamplerCustomAdvanced` und speise diesen Sampler anschließend aus dem MiniMax-H3 Turbo Sampler.
  — <https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo>
4. Setze den Scheduler auf `simple`, die Stärke auf 1.0 und beginne mit 6–8 Schritten; verwende 4 nur dann, wenn Geschwindigkeit wichtiger ist als die Bewegungsqualität.
  — <https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora>

## Best Practices {#best-practices}

- Verwende für die meisten Aufnahmen `minimax_h3_turbo_v4_step600_ema.safetensors`; reserviere v1 bei Schritt 850 für ungewöhnlich schnelle, starke Bewegung mit genau vier Schritten.
  — <https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora>
- Lasse `low_vram` für die schärfere Anwendung zur Laufzeit deaktiviert; aktiviere es erst nach einem Out-of-Memory-Fehler und nimm dabei eine weichere Ausgabe auf quantisierten Basen in Kauf.
  — <https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo>
- Behalte den Turbo Sampler im Graphen über ComfyUI-Updates hinweg bei, da er sich an die native Unterstützung von `ModelSamplingAV` anpasst und auf älteren Builds eine korrekte Audio-Zeitplanung sicherstellt.
  — <https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo>

## Hierdurch abgelöst {#superseded-by-this}

- 2026-08-07 — v1 bei Schritt 850 ist nicht mehr der allgemeine Standard; v4-EMA bei Schritt 600 wird bevorzugt, außer bei Clips mit starker Bewegung und vier Schritten.
- 2026-08-06 — Frühere Empfehlungen beschränkten den Adapter auf nicht gekürzte H3-Basen; der benutzerdefinierte Node ergänzte Unterstützung für gekürzte und Curve-Varianten.

## Weiterhin ungeklärt {#still-unknown}

- Der Adapter und sein Node sind Community-Veröffentlichungen und kein offizielles Produkt von MiniMax Turbo.
- Es wurde kein unabhängiger Benchmark gefunden, der eine allgemeingültige Qualitäts- oder Geschwindigkeitsrangfolge über GPU, Auflösung, Dauer und Bewegungsart hinweg belegt.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora | larryvrh/MiniMax-H3-Turbo-Lora · Hugging Face | 2026-09-05 |
| https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo | Larryvrh/ComfyUI-MiniMax-H3-Turbo · GitHub | 2026-09-05 |
| https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo/commits/main/ | Commit-Verlauf für Larryvrh/ComfyUI-MiniMax-H3-Turbo · GitHub | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:minimax-h3-turbo-lora`, Thread `minimax-h3-turbo-lora`, 1 datiertes Ereignis 2026-08-06 → 2026-08-06.
- **Praktischer Hinweis:** Ab 2026-08-06 sollte MiniMax-H3 Turbo LoRA über den verlinkten Modell- und ComfyUI-Integrationspfad bewertet werden, nicht als isolierter Checkpoint; Kompatibilität, Lizenzierung und Setup-Anforderungen sind vor der Verwendung anhand des aktuellen Stands zu prüfen.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

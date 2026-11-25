---
title: "Sol-Attn"
category: projects
date: 2026-08-03
tags: [project, sana, sol-attn, sol-attn-development]
aliases: ["Sol-Attn"]
level: 2
source_sha256: 747603d60cfce7b1ebcbca2de0fd076a19d90fb090b9c86a75c3035834607262
translation: machine
translated_at: '2026-10-24'
---
# Sol-Attn {#sol-attn}

**Entwicklungslinie:** `project:sol-attn` · Thread `sol-attn-development`  
**Letztes Ereignis:** 2026-08-03 · 1 datiertes seit 2026-08-03 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Sol-Attn — NVIDIAs Methode für blockweise dünnbesetzte Aufmerksamkeit zur Inferenzzeit für vortrainierte Diffusions-Transformer.

- leitet Schlüssel-/Wert-Blöcke während des Online-Softmax weiter, statt eine separate Proxy-Karte aufzubauen;
- berechnet ausgewählte Blöcke exakt und approximiert den Beitrag übersprungener Blöcke;
- wird für die Selbstaufmerksamkeit bei der visuellen Generierung verwendet, während die Kreuzaufmerksamkeit dicht bleiben kann.

Einschränkung: Die veröffentlichte B200-Implementierung unterstützt nur Forward-Inferenz und wurde an bidirektionaler visueller Diffusionsgenerierung evaluiert, nicht an autoregressivem Video. Fazit: Verwenden Sie es als modell- und hardwarespezifische Beschleunigungsoption, nicht als Garantie für die veröffentlichten Beschleunigungswerte.

## Entwicklungslinie {#development-line}

- **2026-08-03 — Projektseite und Implementierungs-Branch zu Sol-Attn referenziert.** 3,95× beziehen sich auf den gesamten Stack, während das Hinzufügen von Sol-Attn nach Kernel-Fusion das kumulative Ergebnis von 1,394× auf 1,534× veränderte. Das Modell ist MiniMax-H3, ein 33B-Omni-Modal-Generator für Video und Audio.

## Was sich geändert hat {#what-changed}

2026-07-27 — Das Sol-Attn-Paper wurde veröffentlicht und definierte query-abhängiges Schwellenwert-Routing, dünnbesetzte Berechnung mit Online-Softmax in einem Durchlauf sowie Korrektur über Proxy-Scores. 2026-07-28 — NVIDIA veröffentlichte den Sol-Attn-Code mit Kernels für SM89, SM90, SM100 und SM120; die damals berichteten Sol-Engine-End-to-End-Ergebnisse umfassten etwa 5,03× für HunyuanVideo-13B und 3,48× für Wan2.1-T2V-14B. 2026-08-03 — Die Unterstützung für MiniMax-H3 wurde zu einem gemessenen Sol-Engine-Rezept auf acht GB200-GPUs: 3,95× beziehen sich auf den gesamten Stack, während das Hinzufügen von Sol-Attn nach Kernel-Fusion das kumulative Ergebnis von 1,394× auf 1,534× veränderte. Das Modell ist MiniMax-H3, ein 33B-Omni-Modal-Generator für Video und Audio. 2026-08-06 — MiniMax-H3-Rezepte wurden auf DGX Spark und RTX 5090 erweitert, mit berichteten Gesamtergebnissen von 3,92× bzw. 4,52×. 2026-08-13 — LTX-2.5-Rezepte ergänzten Sol-Attn für B200, RTX 5090 und DGX Spark; NVIDIA berichtete bis zu 4,68× für seine mehrstufige Pipeline und 1,90× für seine destillierte Pipeline. 2026-08-17 — Für RTX 4090 wurde ein optimierter SM89-CuTe-DSL-Sol-Attn-Kernel hinzugefügt; NVIDIA berichtete 4,44× End-to-End für das vollständige MiniMax-H3-Rezept. 2026-08-22 — MiniMax-H3 Super Acceleration kombinierte einen H3-Entwurf mit vier Schritten und drei LTX-2.5-Verfeinerungsschritten; NVIDIA berichtete 22,2× für fünf Sekunden 768p und 27,7× für zehn Sekunden Video auf einer GB200.

## Anwendung {#how-to-use-this}

Ab 2026-08-03 sollten Praktiker Sol-Attn als eigenständige Sana-Entwicklungslinie behandeln und vor einer Evaluierung oder Übernahme die verlinkte Projektseite und den Branch `sol-engine` konsultieren; der Veröffentlichungsstatus und die technischen Aussagen bedürfen weiterer Überprüfung.

1. Prüfen Sie, ob die Ziel-Selbstaufmerksamkeit in BF16 mit Head-Dimension 128 vorliegt und ob die vorgesehene Laufzeitumgebung CUDA ist; SGLang dokumentiert Sol-Attn im Diffusions-Backend als reines CUDA.
  — <https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx>
2. Installieren Sie das Upstream-Paket aus dem Branch `sol-engine` des NVlabs-Sana-Repositories.
  — <https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx>
3. Wählen Sie `sol_attn` explizit aus und konfigurieren Sie `tau`, die Anzahl dichter Warm-up-Schritte und -Layer, exakte Präfix-Senken dort, wo Konditionierungs-Tokens sie benötigen, sowie `kv_splits=auto` für lange Sequenzen.
  — <https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx>
4. Führen Sie das exakte Zielmodell, die Auflösung, Dauer, den Prompt-Mix und die GPU gegen eine dichte Baseline aus; vergleichen Sie Ausgabequalität und End-to-End-Latenz, bevor Sie die Konfiguration übernehmen.
  — <https://nvlabs.github.io/Sana/Sol-Engine/H3-OnDevice/>

## Best Practices {#best-practices}

- Halten Sie die ersten Entrauschungsschritte und ausgewählte frühe Layer dicht; bewahren Sie Text- oder Audio-Präfix-Tokens als exakte KV-Senken, wenn das Modell sie benötigt.
  — <https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx>
- Erhöhen Sie `tau` vorsichtig: Ein höherer Schwellenwert wählt weniger exakte KV-Blöcke aus und erhöht die Approximation.
  — <https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx>
- Stimmen Sie die Einstellungen auf das eingesetzte Modell, die Hardware, Auflösung, Dauer und den Beschleunigungs-Stack ab; NVIDIA gibt an, dass sich Einstellungen zwischen Kombinationen nicht zuverlässig übertragen lassen.
  — <https://nvlabs.github.io/Sana/Sol-Engine/H3-OnDevice/>

## Durch dieses ersetzt {#superseded-by-this}

- 2026-08-03 — Das Behandeln des berichteten 3,95×-Ergebnisses von MiniMax-H3 als reinen Sol-Attn-Effekt ist überholt: NVIDIAs Aufschlüsselung ordnet 1,394× der Kernel-Fusion bzw. Graph-Capture zu, 1,534× nach Hinzufügen von Sol-Attn und 3,95× erst nach Cross-Step-Caching.
- 2026-08-03 — Die Annahme, ein Beschleunigungsrezept sei qualitätserhaltend, nur weil es trainingsfrei ist, ist überholt: NVIDIAs Preset „super-efficient“ aktiviert Sol-Attn für einen weiteren Faktor 1,25×, meldet jedoch eine größere wahrnehmbare Distanz als sein qualitätserhaltendes Preset.

## Weiterhin unbekannt {#still-unknown}

- Die beiden Links des Quellereignisses sind undatierte aktuelle Seiten, daher lässt sich der genaue Inhalt, den Leser am 2026-08-03 sahen, aus ihnen allein nicht rekonstruieren. NVIDIAs datierte MiniMax-H3-Seite liefert die ereignisspezifische Korrektur und den Geltungsbereich.
- Die aktuelle SGLang-Dokumentation beschreibt ihre `sol_attn`-Integration als reines CUDA; sie belegt nicht die Hardware-Abdeckung aller direkten oder Community-Integrationen des Upstream-Pakets.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://nvlabs.github.io/Sana/Sol-Attn/ | Sol-Attn | On-the-Fly Attention Sparsification | 2026-09-05 |
| https://github.com/NVlabs/Sana/tree/sol-engine | NVlabs/Sana — Branch sol-engine | 2026-09-05 |
| https://arxiv.org/abs/2607.24027 | Sol-Attn: Accelerating Video Generation Inference via On-the-Fly Attention Sparsification | 2026-09-05 |
| https://nvlabs.github.io/Sana/Sol-Engine/H3/ | Deploy MiniMax-H3 with Sol Engine achieving 3.95× acceleration in 4.5 hours of optimization | 2026-09-05 |
| https://nvlabs.github.io/Sana/Sol-Engine/H3-OnDevice/ | Deploy MiniMax-H3 on DGX Spark and RTX 5090 with Sol Engine: 4.52× Acceleration | 2026-09-05 |
| https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx | SGLang diffusion attention backends | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:sol-attn`, Thread `sol-attn-development`, 1 datiertes Ereignis 2026-08-03 → 2026-08-03.
- **Praktischer Hinweis:** Ab 2026-08-03 sollten Praktiker Sol-Attn als eigenständige Sana-Entwicklungslinie behandeln und vor einer Evaluierung oder Übernahme die verlinkte Projektseite und den Branch `sol-engine` konsultieren; der Veröffentlichungsstatus und die technischen Aussagen bedürfen weiterer Überprüfung.
- **Konfidenz:** hoch. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was überholt ist.

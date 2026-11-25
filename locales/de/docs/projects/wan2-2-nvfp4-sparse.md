---
title: "Wan2.2-NVFP4-Sparse"
category: projects
date: 2026-06-05
tags: [project, wan, wan2-2-nvfp4-sparse, wan2-2-nvfp4-sparse-development]
aliases: ["Wan2.2-NVFP4-Sparse"]
level: 3
source_sha256: 91fef09886dce840d729573fcbe91cc227d6364644e8a1cd022fad6117b8ec67
translation: machine
translated_at: '2026-10-24'
---
# Wan2.2-NVFP4-Sparse {#wan22-nvfp4-sparse}

**Entwicklungslinie:** `project:wan2-2-nvfp4-sparse` · Thread `wan2-2-nvfp4-sparse-development`  
**Letztes Ereignis:** 2026-06-05 · 1 datiert seit 2026-06-05 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Wan2.2-NVFP4-Sparse, seit dem 27. Juli im Modellkarten-Eintrag als LightWan2.2-A14B bezeichnet, ist eine Version von Wan2.2-T2V/I2V-A14B für Besitzer von Blackwell-GPUs, die einen lokalen Videogenerator mit vier Schritten benötigen. Funktionen: T2V; I2V; NVFP4-Paare high/low; dynamic sparse attention. Maßstab und Grenzen: Die Angaben der Autoren zur RTX 5090 ergeben 9,1–26,7 s bei 4 Schritten für 480p/720p, doch der Pfad erfordert RTX 50/Blackwell sowie T5/VAE, und für I2V zusätzlich einen image encoder. Fazit: Sinnvoll als spezialisierte LightX2V-Pipeline; auf anderer Hardware sind die angegebenen Vorteile nicht bestätigt.

## Entwicklungslinie {#development-line}

- **2026-06-05 — Hugging-Face-Referenz für Wan2.2-NVFP4-Sparse.** Wan2.2-NVFP4-Sparse — es erschienen benannte T2V/I2V-high/low-NVFP4-Gewichte, einschließlich der Comfy-Varianten, und sie wurden neu geordnet; aus dem Stammverzeichnis wurden zwei mehrdeutige Duplikate entfernt.

## Was sich geändert hat {#what-changed}

2026-05-28: Wan2.2-NVFP4-Sparse — das Modell-Repository wurde auf Hugging Face angelegt. 2026-05-29: Wan2.2-NVFP4-Sparse — LightX2V kündigte eine Variante von Wan 2.2 14B für T2V und I2V mit NVFP4 quantization-aware step distillation und sparse attention für Blackwell an; angegeben wurden mehr als 50× auf einer einzelnen RTX 5090. 2026-06-05: Wan2.2-NVFP4-Sparse — es erschienen benannte T2V/I2V-high/low-NVFP4-Gewichte, einschließlich der Comfy-Varianten, und sie wurden neu geordnet; aus dem Stammverzeichnis wurden zwei mehrdeutige Duplikate entfernt. 2026-06-09: Wan2.2-NVFP4-Sparse — die Modellkarte legte I2V als Basismodell fest und ergänzte einen eigenen Startpfad mit image encoder und Eingabebild. 2026-07-18: Wan2.2-NVFP4-Sparse — die Anleitungen wurden vom veralteten Verzeichnis distill auf die aktuellen Skripte wan22/extreme umgestellt, und es wurden Varianten für sequence parallel auf mehreren GPUs ergänzt. 2026-07-27: Wan2.2-NVFP4-Sparse — die Modellkarte wurde in LightWan2.2-A14B umbenannt; die alte Adresse leitet nun auf die neue weiter.

## So wird es verwendet {#how-to-use-this}

Ab dem 2026-06-05 sollten Praktiker das verlinkte Hugging-Face-Repository als mögliche Quelle für Wan2.2-NVFP4-Sparse behandeln und vor der Verwendung Modellkarte, Dateien, Lizenz und Kompatibilität prüfen.

1. Prüfen Sie die Plattform: Dieser Pfad erfordert NVIDIA RTX 50-Series oder eine andere Blackwell-Architektur; auf einer anderen GPU ist der angegebene NVFP4-Modus nicht zu erwarten.
  — <https://huggingface.co/lightx2v/LightWan2.2-A14B>
2. Starten Sie den empfohlenen Container lightx2v/lightx2v:26052801-cu130-5090 oder bauen Sie LightX2V und den NVFP4-Kernel mit CUTLASS gemäß der Anleitung der Modellkarte.
  — <https://huggingface.co/lightx2v/LightWan2.2-A14B>
3. Laden Sie das zur Aufgabe passende high/low-NVFP4-Gewichtspaar für T2V oder I2V herunter und bereiten Sie Wan2.2 T5 und VAE vor; für I2V zusätzlich den image encoder und das Ausgangsbild.
  — <https://huggingface.co/lightx2v/LightWan2.2-A14B>
4. Tragen Sie in der Konfiguration die Pfade zu beiden checkpoint files ein, high_noise_quantized_ckpt und low_noise_quantized_ckpt; die Start-Konfiguration für T2V setzt 4 Schritte, 81 Frames, 480×832 und ein Sparse-Attention-Verhältnis von 0.9.
  — <https://github.com/ModelTC/LightX2V/blob/main/configs/wan22/extreme/wan_moe_t2v_distill_nvfp4_sparse_attn.json>
5. Setzen Sie für T2V lightx2v_path und model_path im aktuellen run_wan22_moe_t2v_extreme.sh und starten Sie das Skript; es ruft model_cls wan2.2_moe mit der T2V-extreme-Konfiguration auf.
  — <https://github.com/ModelTC/LightX2V/blob/main/scripts/wan22/extreme/run_wan22_moe_t2v_extreme.sh>
6. Setzen Sie für I2V dieselben Pfade sowie image_path in run_wan22_moe_i2v_extreme.sh; das Skript verwendet die I2V-extreme-Konfiguration und speichert das Ergebnis als MP4.
  — <https://github.com/ModelTC/LightX2V/blob/main/scripts/wan22/extreme/run_wan22_moe_i2v_extreme.sh>

## Best Practices {#best-practices}

- Verwenden Sie das empfohlene Docker-Image und die offiziellen extreme-Skripte: Sie sind der dokumentierte Weg für dieses Modell und nicht nur das allgemeine Hub-Widget von Diffusers.
  — <https://huggingface.co/lightx2v/LightWan2.2-A14B>
- Speichern Sie high- und low-noise-Gewichte als Paar und setzen Sie beide expliziten Pfade in der Konfiguration; greifen Sie nicht auf die entfernten generischen Dateinamen high_nvfp4/low_nvfp4 zurück.
  — <https://github.com/ModelTC/LightX2V/blob/main/configs/wan22/extreme/wan_moe_t2v_distill_nvfp4_sparse_attn.json>
- Wenden Sie sparse attention vor allem bei hoher Auflösung an; aktivieren Sie CPU offload nur bei Speichermangel, da die Modellkarte vor einem Rückgang des Throughputs warnt.
  — <https://huggingface.co/lightx2v/LightWan2.2-A14B>
- Vergleichen Sie vor dem produktiven Einsatz Ihren eigenen Prompt-Satz mit der FP8-Basis hinsichtlich prompt adherence: Ein offenes, aber nicht geschlossenes Issue berichtete über schlechtere Promptbefolgung bei FP4; das ist jedoch kein bestätigter allgemeiner Qualitätsrückgang.
  — <https://github.com/ModelTC/LightX2V/issues/1147>

## Hierdurch überholt {#superseded-by-this}

- {"claim":"Anleitungen, die auf die generischen Dateien high_nvfp4.safetensors und low_nvfp4.safetensors verweisen, sind veraltet: Beide Dateien wurden aus dem Repository entfernt.","obsolete_since":"2026-06-05","source_url":"https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/0191e9d9499dfc0bc7fcfbc24b678e94b918c405"}
- {"claim":"Anleitungen mit den Pfaden scripts/wan22/distill/run_wan22_moe_*_extreme.sh sind veraltet: Die Modellkarte hat den Start auf scripts/wan22/extreme umgestellt und Varianten für sequence parallel ergänzt.","obsolete_since":"2026-07-18","source_url":"https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/3eef5caddabe719c0a96fd8f3f703f5f1f235f8b"}
- {"claim":"Wan2.2-NVFP4-Sparse als aktueller Name der Modellkarte ist veraltet: Auf der Karte wurde er durch LightWan2.2-A14B ersetzt; die alte URL bleibt als Redirect erhalten.","obsolete_since":"2026-07-27","source_url":"https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/27213d1d4a6cfb1ecd9c60d214764c917d0f6c45"}

## Weiterhin unbekannt {#still-unknown}

- Der im README des Projekts genannte LightX2V-Blogbeitrag vom 19. Juli 2026 lieferte bei der Überprüfung einen 404-Fehler; er wird daher nicht als Beleg für ein Modell- oder Laufzeit-Update verwendet.
- Die Zeiten auf der RTX 5090 und die Angabe von mehr als 50× stammen von den Autoren; hier wurde keine unabhängige Reproduktion auf Blackwell durchgeführt.
- Issue #1147 berichtet über schwächere Promptbefolgung im Vergleich zu einem FP8-Vergleich, ist aber keinem Bearbeiter zugewiesen und hat weder eine Antwort des Maintainers noch einen reproduzierbaren Benchmark; es belegt daher keinen allgemeinen Qualitätsrückgang.
- Der Hub zeigt generischen Beispielcode für Diffusers, doch es wurde keine Ausführung gefunden, die belegt, dass er das dokumentierte LightX2V-Setup mit expliziten high/low-Checkpoint-Pfaden und NVFP4-Kerneln ersetzt.
- Der 27. Juli belegt die Umbenennung der Modellkarte und dass die alte URL derzeit weiterleitet; der genaue Zeitstempel der Weiterleitung im Hugging-Face-Repository wurde jedoch nicht angezeigt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/lightx2v/Wan2.2-NVFP4-Sparse | Historische Wan2.2-NVFP4-Sparse-URL, leitet auf LightWan2.2-A14B weiter | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B | Modellkarte LightWan2.2-A14B | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B/commits/main | Commit-Verlauf von LightWan2.2-A14B | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/0191e9d9499dfc0bc7fcfbc24b678e94b918c405 | Zusätzliche NVFP4-safetensors-Dateien entfernen | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/4dbf88dc61135c02943f3f54c99acee05ed856db | Aktualisierung der Modellkarte mit dem I2V-Pfad | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/3eef5caddabe719c0a96fd8f3f703f5f1f235f8b | Aktualisierung der Modellkarte: Umstellung auf extreme- und sequence-parallel-Skripte | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/27213d1d4a6cfb1ecd9c60d214764c917d0f6c45 | Aktualisierung der Modellkarte: Umbenennung in LightWan2.2-A14B | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/blob/main/README.md | Englische README von LightX2V mit datiertem Release-Log | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/blob/main/README_zh.md | Vereinfachtes-Chinesisch-README von LightX2V mit datiertem Release-Log | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/blob/main/configs/wan22/extreme/wan_moe_t2v_distill_nvfp4_sparse_attn.json | Konfiguration für T2V-NVFP4-Sparse-Attention | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/blob/main/scripts/wan22/extreme/run_wan22_moe_t2v_extreme.sh | T2V-extreme-Startskript | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/blob/main/scripts/wan22/extreme/run_wan22_moe_i2v_extreme.sh | I2V-extreme-Startskript | 2026-09-06 |
| https://lightx2v-en.readthedocs.io/en/latest/getting_started/model_structure.html | Anleitung zu Modellformat und Laden in LightX2V | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/issues/1147 | Offener Community-Bericht zur Prompt-Befolgung bei NVFP4 | 2026-09-06 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:wan2-2-nvfp4-sparse`, Thread `wan2-2-nvfp4-sparse-development`, 1 datiertes Ereignis 2026-06-05 → 2026-06-05.
- **Praktischer Hinweis:** Ab dem 2026-06-05 sollten Praktiker das verlinkte Hugging-Face-Repository als mögliche Quelle für Wan2.2-NVFP4-Sparse behandeln und vor der Verwendung Modellkarte, Dateien, Lizenz und Kompatibilität prüfen.
- **Konfidenz:** mittel. Die datierten Überholungsvermerke oben sind maßgeblich dafür, was veraltet ist.

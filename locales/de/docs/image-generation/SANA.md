---
title: "SANA"
category: models
tags: [text-to-image, dit, flow-matching, efficient, 1.6b, 600m, 4.8b, linear-attention, dc-ae, litela, mix-ffn, gemma, nvlabs, jewelry-retouching]
aliases: ["SANA 1.5", "SANA 1.6B", "SANA-Sprint", "SANA-Video"]
level: 4
source_sha256: 37c4e864f5e1877975afe4e579cbb97e287f7bd5a274acf785d4ecfa64157b08
translation: machine
translated_at: '2026-10-24'
---
# SANA (effiziente hochauflösende Bildsynthese) {#sana-efficient-high-resolution-image-synthesis}

Effizientes DiT von NVlabs/MIT Han Lab. 600M–4.8B Parameter mit konkurrenzfähiger Qualität bei 1024–4096px. Verwendet **lineare Attention O(n)**, **DC-AE mit 32×-Kompression** und den Textencoder **Gemma-2-2B**. ICLR 2025 Oral.

## Aktueller Status (verifiziert am 2026-08-27) {#current-status-verified-2026-08-27}

Der Name SANA umfasst inzwischen mehrere verwandte, aber nicht austauschbare Zweige. Wählen Sie das Artefakt aus, bevor Sie Aussagen zu Leistung, Speicherbedarf oder Lizenzierung übernehmen.

| Zweig | Aktueller Stand des Artefakts | Vorgesehene Verwendung |
|---|---|---|
| SANA / SANA 1.5 / Sprint | Veröffentlichter Bildgenerierungscode und Checkpoints | Text-zu-Bild und Bildverfeinerung |
| SANA-Video (2025) | Veröffentlichte Forschungsimplementierung; Diffusers-Integration folgte | Frühere kausale Videogenerierung |
| SANA-WM (2026) | Veröffentlichter 2.6B-World-Model-Zweig | 720p interaktive Welt-Simulation, bis zu einer Minute, 6-DoF-Steuerung |
| SANA-Video2 (2026) | Trainings- und Inferenzcode sowie **5B-720p-Checkpoint, veröffentlicht am 2026-08-19** | Aktuelle 720p-Videogenerierung |
| SANA-Video2 14B | Architektur/Konfiguration besprochen, aber kein 14B-Checkpoint im offiziellen Repository | Nur als Forschungsreferenz; nicht für ein lauffähiges Rezept auswählen |

Die Meldung vom 4. August 2026, dass Video2 keine öffentlichen Gewichte besitze, war zum damaligen Zeitpunkt korrekt und ist für das 5B-Modell nun **überholt**. Für den 14B-Checkpoint trifft sie zum Verifikationsdatum weiterhin zu.

Die offizielle Video2-Seite berichtet einen Benchmark mit 5 Sekunden, 720p, 40 Schritten und dem 5B-Modell auf einer H100, einschließlich eines Ergebnisses von 13,06 Sekunden für die Sol Engine. Behandeln Sie dies als festgeschriebenen Benchmark-Kontext und nicht als Laufzeitschätzung für Consumer-GPUs.

## Architektur – Vollständige Details {#architecture-full-detail}

### Modellvarianten {#model-variants}

| Variante | Parameter | Tiefe | Hidden | Heads | FFN (2.5× MLP) |
|---------|--------|-------|--------|-------|----------------|
| Sana-0.6B | 590M | 28 Blöcke | 1152 | 16 | 2880 |
| Sana-1.6B | 1604M | 20 Blöcke | 2240 | 20 | 5600 |
| Sana-1.5 4.8B | 4800M | 60 Blöcke | 2240 | 20 | 5600 |

0.6B = tiefer, aber schmaler. 1.6B = flacher, aber breiter. 4.8B skaliert AUSSCHLIESSLICH die Tiefe (20→60); die Breite bleibt wie bei 1.6B.

### SanaBlock-Struktur (AdaLN-Zero) {#sanablock-structure-adaln-zero}

```bash
Input x → LayerNorm → modulate(shift1, scale1) → Linear Self-Attention (LiteLA)
        → LayerNorm → modulate(shift2, scale2) → Cross-Attention (standard, with text)
        → LayerNorm → modulate(shift3, scale3) → Mix-FFN (GLUMBConv)
Output x (residual at each stage, 6 modulation params per block via scale_shift_table)
```

### Lineare Attention (LiteLA mit ReLU-Kernel) {#linear-attention-litela-with-relu-kernel}

```python
# Standard quadratic: O(N^2)
# Attention = softmax(QK^T / sqrt(d)) * V

# SANA linear: O(N * d^2)
# phi(x) = ReLU(x)
# Shared terms: S = sum_j phi(K_j)^T * V_j   (shape d×d, computed ONCE)
#               Z = sum_j phi(K_j)^T          (shape d×1, computed ONCE)
# Output_i = phi(Q_i) * S / (phi(Q_i) * Z + eps)
```

**Kompromiss:** Lineare Attention allein verschlechtert die Qualität. Dies wird durch Mix-FFN mit 3×3-Depthwise-Convolution kompensiert, die lokale räumliche Informationen erfasst, die durch den ReLU-Kernel verloren gehen (kein Lokalitäts-Bias durch Softmax).

**Triton-Kernel-Fusion:** ReLU-Aktivierung, Präzisionskonvertierungen, Padding und Division werden in die Matmul integriert → ca. 10 % Geschwindigkeitsgewinn.

**Positionskodierung:** „NoPE“ (No Positional Embeddings) – die 3×3-Depthwise-Convolution in Mix-FFN kodiert die Position implizit. Alternativ wird RoPE mit `theta=10000, axes_dim=[0,16,16]` unterstützt.

### Mix-FFN (GLUMBConv) {#mix-ffn-glumbconv}

Ersetzt das Standard-MLP:
```text
Linear(d → d×2.5) → DW-Conv3×3 → SiLU → Gate (GLU) → Linear(d×1.25 → d)
```
Die 3×3-Depthwise-Convolution ist der Schlüssel dafür, dass lineare Attention funktioniert. Sie liefert ein lokales rezeptives Feld, das der lineare Attention mit ReLU fehlt.

### DC-AE (Deep Compression Autoencoder) – F32C32P1 {#dc-ae-deep-compression-autoencoder-f32c32p1}

**32× räumliche Kompression, 32 Latent-Kanäle, Patch-Größe 1.**

| Auflösung | SD/FLUX (F8, P2) Tokens | SANA (F32, P1) Tokens | Reduktion |
|-----------|-------------------------|------------------------|-----------|
| 512×512 | 1024 | **256** (16×16) | 4× |
| 1024×1024 | 4096 | **1024** (32×32) | 4× |
| 2048×2048 | 16384 | **4096** (64×64) | 4× |
| 4096×4096 | 65536 | **16384** (128×128) | 4× |

4× weniger Tokens + lineare Attention mit O(n) = **um Größenordnungen** schneller bei hoher Auflösung.

Rekonstruktionsqualität (ImageNet): rFID 0.34, PSNR 29.29, SSIM 0.84, LPIPS 0.05.

**Tiling wird unterstützt:** `pipe.vae.enable_tiling(tile_sample_min_height=1024, tile_sample_min_width=1024)` – ermöglicht 4K mit 22 GB VRAM.

Zwei Versionen: `dc-ae-f32c32-sana-1.0`, `dc-ae-f32c32-sana-1.1` (verbessert), `dc-ae-lite-f32c32` (schneller/kleiner).

### Textencoder: Gemma-2-2B-IT {#text-encoder-gemma-2-2b-it}

Decoder-only-LLM (nicht T5). 6× schneller als T5-XXL. Maximal 300 Tokens.

**Kritisch:** Die Ausgaben des Decoder-only-Modells haben eine um Größenordnungen größere Varianz als T5. Lösung: **RMSNorm** nach dem Encoder sowie eine lernbare Skalierung von 0.01 (`y_norm: true, y_norm_scale: 0.01`).

**Complex Human Instruction (CHI):** nutzt das In-Context-Learning von Gemma → +2.2 GenEval-Punkte.

## Training {#training}

### Verlustfunktion & Scheduler {#loss-scheduler}

[[flow-matching]]-Geschwindigkeitsvorhersage: `v_theta(x_t, t) = epsilon - x_0`. Zeitschritt-Sampling: Logit-Normal (Mittelwert=0.0, Std=1.0). Flow-Shift: 3.0.

### Optimizer: CAME {#optimizer-came}

```yaml
optimizer: CAMEWrapper
lr: 1e-4
betas: [0.9, 0.999, 0.9999]
epsilon: [1e-30, 1e-16]
weight_decay: 0.0
grad_clip: 0.1
warmup: 2000 steps, constant after
```

SANA 1.5 verwendet **CAME-8bit** – blockweise 8-Bit-Momente erster Ordnung, 32-Bit-Momente zweiter Ordnung. 25 % weniger Speicherbedarf gegenüber AdamW.

### Auflösungsplan {#resolution-schedule}

Überspringen Sie 256px komplett. Starten Sie bei 512px → Feinabstimmung auf 1024 → 2K → 4K.

### Multi-Caption-Labeling {#multi-caption-labeling}

4 VLMs erzeugen Beschreibungen (VILA-3B, VILA-13B, InternVL2-8B, InternVL2-26B). Ein CLIP-Score-Sampler wählt pro Iteration aus.

### SFT: 3M Samples, gefiltert nach CLIP > 25 aus dem 50M-Pre-Training-Set. {#sft-3m-samples-filtered-by-clip-25-from-50m-pre-training-set}

## Wichtigste Verbesserungen in SANA 1.5 {#sana-15-key-improvements}

1. **Depth-Growth-Paradigma (1.6B → 4.8B):** Entfernen der letzten 2 Blöcke des trainierten 1.6B-Modells → Hinzufügen von 40 neuen Blöcken mit Partial Preservation Init (Identitätsabbildungen) → 60 % weniger Trainingsschritte
2. **QK-Normalisierung:** RMSNorm auf Q und K für stabiles Training großer Modelle
3. **Depth Pruning:** Metrik zur Block-Wichtigkeit → mittlere Blöcke entfernen, Kopf und Ende behalten → schnelle Erholung mit ca. 100 Feinabstimmungsschritten
4. **Skalierung zur Inferenzzeit:** N Kandidaten generieren, den besten über VILA-Judge auswählen (feinabgestimmtes NVILA-2B). GenEval: 0.81 → **0.96** mit 2048 Kandidaten. 1.6B mit Skalierung **übertrifft** 4.8B ohne Skalierung.

## Benchmarks {#benchmarks}

| Modell | Parameter | FID↓ | CLIP↑ | GenEval↑ | Geschwindigkeit (A100) |
|-------|--------|------|-------|----------|-------------|
| FLUX-dev | 12.0B | 10.15 | 27.47 | 0.67 | 0.04 Bilder/s |
| SD3-medium | 2.0B | 11.92 | 27.83 | 0.62 | 0.28 Bilder/s |
| **Sana-0.6B** | 0.6B | **5.81** | 28.36 | 0.64 | **1.7 Bilder/s** |
| **Sana-1.6B** | 1.6B | **5.76** | 28.67 | 0.66 | **1.0 Bilder/s** |
| **Sana-1.5 1.6B** | 1.6B | 5.70 | 29.12 | **0.82** | 1.0 Bilder/s |
| **Sana-1.5 4.8B** | 4.8B | 5.99 | 29.23 | 0.81 | 0.26 Bilder/s |

Sana-1.6B ist **23× schneller** als FLUX-dev. Bei 4K: **106× schneller** (9.6 s gegenüber 469 s).

## SANA-Sprint (destilliert, 1–4 Schritte) {#sana-sprint-distilled-1-4-steps}

Hybride Destillation: sCM (kontinuierliche Konsistenz) + LADD (latente adversariale Verluste).

| Schritte | FID | GenEval | Latenz (H100) |
|-------|-----|---------|-----------------|
| 1 | 7.04 | 0.72 | **0.1 s** |
| 2 | 6.76 | — | 0.24 s |
| 4 | 6.48 | 0.76 | 0.32 s |

Übertrifft FLUX-schnell (7.94 FID) bei 10× höherer Geschwindigkeit. ICCV 2025 Highlight.

## SANA-Video- und World-Model-Zweige {#sana-video-and-world-model-branches}

### SANA-Video (Generation 2025) {#sana-video-2025-generation}

Der ursprüngliche Videozweig führte Block Causal Linear Attention und Causal Mix-FFN ein. Die berichteten Ergebnisse von 2B/720p/16 FPS gehören zu diesem Release und dürfen nicht auf Video2 oder SANA-WM übertragen werden.

Für [[temporal-tiling]] ist kausale Attention strukturell relevant für Tiles-als-Frames. Dies ist jedoch eine architektonische Analogie und kein unterstützter SANA-Workflow.

### SANA-WM (World Model 2026) {#sana-wm-2026-world-model}

SANA-WM ist ein interaktives 2.6B-World-Model und keine Umbenennung von SANA-Video. Das offizielle Projekt beschreibt 720p-Generierung, Sequenzen von bis zu einer Minute und 6-DoF-Kamerasteuerung. Prüfen Sie Controller-Format und Checkpoint-Lizenz gegen das genaue Release, bevor Sie es integrieren.

### SANA-Video2 (Generation 2026) {#sana-video2-2026-generation}

Video2 ist der aktuelle Generationszweig. Das offizielle Repository hat am 2026-08-19 Trainingscode, Inferenzcode, Architekturdetails und einen 5B-720p-Checkpoint ergänzt. Eine 14B-Variante wird beschrieben, ist im Repository aber kein lauffähiger öffentlicher Checkpoint.

Der Benchmark aus dem Paper auf der Projektseite und der Leitfaden zum veröffentlichten Checkpoint verwenden unterschiedliche Laufkonfigurationen:

| Kontext | Frames/Dauer | FPS | Schritte | Zweck |
|---|---|---:|---:|---|
| Benchmark auf H100 (Projektseite) | 5-Sekunden-Clip | Kein Standardwert des veröffentlichten Rezepts | 40 | Nur Vergleich Paper/Engine |
| Leitfaden zum öffentlichen 5B-Checkpoint | 193 Frames / ca. 8.04 Sekunden | 24 | 50 | Aktuelles Beispiel für den veröffentlichten Checkpoint |

Für eine reproduzierbare Auswertung des veröffentlichten Checkpoints gehen Sie vom öffentlichen Leitfaden aus und dokumentieren Sie:

```yaml
artifact: SANA-Video2-5B
revision: <immutable-checkpoint-or-repository-revision>
resolution: 720p
frames: 193
fps: 24
duration_seconds: 8.04
steps: 50
gpu: <exact-model>
engine: <official-or-baseline-runtime>
seed: <integer>
refiner_enabled: <true-or-false>
```

Übertragen Sie das 14B-Label nicht in dieses Rezept. Verwenden Sie 5 Sekunden/40 Schritte nur bei der Reproduktion des Paper-Benchmarks, nicht als Standard für den öffentlichen Checkpoint. Vergleichen Sie H100-Zeiten nicht mit einer lokalen GPU, ohne Frames/Dauer, Auflösung, Schritte, Laufzeit und Zustand des Refiners gleich gemessen zu haben.

## VRAM {#vram}

| Konfiguration | VRAM |
|--------|------|
| 0.6B 1024px bf16 | ~16 GB |
| 1.6B 1024px bf16 | ~16–24 GB |
| 4K mit VAE-Tiling | ~22 GB |
| 4K + 4-Bit-Quantisierung + Offload | **< 8 GB** |
| W8A8-quantisiert 1024px | Sehr niedrig, 0.37 s auf 4090 |

## Feinabstimmung / LoRA {#fine-tuning-lora}

Offizielle Unterstützung über diffusers `train_dreambooth_lora_sana.py`. Details zur vollständigen Trainingspipeline finden Sie unter [[diffusion-lora-training]].

**LoRA-Ziele:** `attn.to_k, attn.to_q, attn.to_v, attn.to_out.0` sowie optional FFN/MLP.

**Einstellungen:** LR 1e-4, 500 Schritte, Batch 1, Gradient Accumulation 4, bf16. Erfordert peft >= 0.14.0.

**Anforderungen an den Datensatz:**
- DreamBooth (Motiv): mindestens 3–5 Bilder
- Stil-/Domänen-LoRA: 20–30 Bilder empfohlen
- Format: Auflösung ab 1024x1024, ausführliche Beschreibungen mit seltenem Trigger-Token („sks“)

**Flags zur Speicheroptimierung:** `--offload` (CPU-Offload von Textencoder und VAE), `--cache_latents` (VAE-Latents vorberechnen), `--use_8bit_adam`.

**ControlNet** wird ebenfalls unterstützt – ControlNet-Transformer-Architektur für das SANA-Backbone.

### Selbstverfeinerung (img2img) {#self-refinement-img2img}

SANA-Sprint unterstützt img2img über `SanaSprintImg2ImgPipeline`:

```python
from diffusers import SanaSprintImg2ImgPipeline
import torch

pipe = SanaSprintImg2ImgPipeline.from_pretrained(
    "Efficient-Large-Model/Sana_Sprint_1.6B_1024px_diffusers",
    torch_dtype=torch.bfloat16
)
pipe.to("cuda")

# Multi-pass refinement (replaces SDXL refiner pattern)
refined = pipe(
    prompt="a high quality detailed photo",
    image=initial_image,
    strength=0.3,            # 0.3 = mild refinement, 0.7 = heavy change
    num_inference_steps=4    # Sprint is 1-4 steps
).images[0]
```

**Mechanik von Flow-Matching-img2img:** SANA verwendet Flow Matching, nicht DDPM. Der Parameter `strength` interpoliert zwischen dem kodierten Eingangsbild und reinem Rauschen: `x_t = (1-strength)*image_latent + strength*noise`. Das unterscheidet sich vom Rauschplan bei DDPM – es gibt keinen Schritt „Rauschen hinzufügen, dann entrauschen“, sondern eine direkte Interpolation.

**Multi-Pass-Rezept:**
```text
txt2img 1024px (strength=1.0) → img2img strength=0.3-0.4 → img2img strength=0.2
```

**Der SDXL-Refiner hat kein Flow-Matching-Äquivalent:** Der SDXL-Refiner nutzt Sampling mit hohen Zeitschritten, das DDPM-spezifisch ist. Die img2img-Funktion von SANA ist der funktionale Ersatz, arbeitet intern aber anders.

**DemoFusion ist mit SANA nicht kompatibel:** DemoFusion stützt sich auf UNet-Skip-Connections für den multiskaligen globalen Kontext. Die Transformer-Architektur von SANA besitzt diese nicht. Verwenden Sie stattdessen FreeScale oder APT für hochauflösendes Tiling.

Vollständige Details zu Flow-Matching-img2img finden Sie unter [[flow-matching]].

## Entwicklungsverlauf {#development-history}

| Datum | Zweig | Ereignis | Zeitlicher Status |
|---|---|---|---|
| 2024-10-22 | SANA-Bild | Repository/Projekt öffentlich sichtbar | Historische Entdeckung |
| 2024-11-21 | SANA-Bild | Training, Inferenz, Metrikcode und 1.6B-Modelle verfügbar | Aktuelle Grundlage |
| 2025-10-01 | SANA-Video | Preview gemeldet | Durch veröffentlichte Implementierung überholt |
| 2025-10-27 | SANA-Video | Offizielle Veröffentlichung | Historisch/aktuell für diesen Zweig |
| 2025-11-06 | SANA-Video | Diffusers-Integration laut Projekt gemeldet | Aktuelle Integrationshistorie |
| 2025-12-24 | SANA-Video | Verfügbarkeit von Code/Checkpoint gemeldet | Durch spätere Zweige überholt, beibehalten |
| 2026-03 | SANA-Bild/Video-Tooling | 720p-LTX-VAE-Pfad und Update des LTX2-Refiners auf 2K | Nur für diese Pipeline aktuell |
| 2026-05 | SANA-WM | 2.6B-World-Model-Zweig veröffentlicht | Aktueller Zweig |
| 2026-08-04 | SANA-Video2 | Ankündigung ohne Gewichte beobachtet | Für 5B am 2026-08-19 überholt |
| 2026-08-19 | SANA-Video2 | Code plus 5B-720p-Checkpoint veröffentlicht | Aktuell |

## Praktische Auswahl {#practical-selection}

- Verwenden Sie SANA/SANA 1.5 für effiziente Bildgenerierung und dokumentierte LoRA-Workflows für Bilder.
- Verwenden Sie Sprint nur, wenn das destillierte Verhalten mit ein bis vier Schritten ausdrücklich gewünscht ist; übernehmen Sie keine Standard-Schrittzahlen.
- Verwenden Sie SANA-Video2 5B für den aktuellen offiziellen, lauffähigen Video2-Pfad.
- Verwenden Sie SANA-WM nur für interaktive Experimente mit World Models und dessen eigenem Controller-Vertrag.
- Planen Sie kein 14B-Video2-Deployment, solange kein offizieller Checkpoint und keine Lizenz vorliegen.

## Forschungsabdeckung und offene Lücken {#research-coverage-and-open-gaps}

- Primäre englischsprachige Evidenz: offizielles Repository, offizielle Video2-Projektseite und Paper.
- Chinesische Suchspur: durchsucht, aber im begrenzten Durchlauf wurde keine qualifizierte chinesische Quelle aus erster Hand übernommen.
- Offene Nachweislücke: eine vollständig reproduzierbare Matrix für Consumer-GPUs, festgelegt auf Checkpoint-Hashes, Laufzeitversionen und Zustand des Refiners.
- Community-Leistungsberichte bleiben sekundär, bis sie mit denselben Einstellungen reproduziert wurden.

### Community-Berichte {#community-reports}

- [Issue #156](https://github.com/NVlabs/Sana/issues/156) berichtet von einem Community-Trainingspfad für 1.6B auf 24 GB mit Offload. Der Beitragende bezeichnete den Patch ausdrücklich als unübersichtlich; ein offizieller Mitwirkender verwies auf die CAME-8bit-Konfiguration des Projekts als bessere Richtung zur Speicherersparnis. Behandeln Sie das Issue als technischen Hinweis, nicht als fertiges Rezept.
- [Issue #297](https://github.com/NVlabs/Sana/issues/297) dokumentiert einen ungelösten Fall auf MacBook Pro M3/MPS, bei dem `Sana_600M_512px_diffusers` mit `float16` ein einheitlich graues Bild ohne Ausnahme erzeugte. Testen Sie `float32` als Diagnose, aber es liegt kein von Maintainern bestätigter Fix vor.
- Keines der beiden Issues betrifft den veröffentlichten Video2-5B-Checkpoint. Übertragen Sie deren Einstellungen für Bildmodelle nicht auf Video2.

## Fallstricke {#gotchas}

- **Problem:** „SANA-Video“ als einen laufend versionierten Checkpoint behandeln → **Lösung:** Zweig (`Video`, `WM` oder `Video2`), Modellgröße, Checkpoint-Revision und Veröffentlichungsdatum festhalten.
- **Problem:** Video2 14B auswählen, weil es in Architekturtabellen erscheint → **Lösung:** den veröffentlichten 5B-Checkpoint verwenden; 14B ist zum 2026-08-27 kein öffentlich lauffähiges Artefakt.
- **Problem:** die Aussage vom 4. August „keine Gewichte“ als aktuell wiederholen → **Lösung:** als durch die 5B-Veröffentlichung vom 19. August überholt kennzeichnen und als historischen Kontext beibehalten.
- **Problem:** H100-Latenzen oder alte 2B-Videobenchmarks verallgemeinern → **Lösung:** Hardware, Engine, Dauer, Auflösung, Schritte und Zweig in jedem Vergleich angeben.
- **Problem:** den 5-Sekunden/40-Schritte-Benchmark aus dem Paper als Rezept für den veröffentlichten Checkpoint verwenden → **Lösung:** vom öffentlichen Leitfaden mit 193 Frames, 24 FPS und 50 Schritten ausgehen, sofern nicht bewusst der Benchmark reproduziert wird.
- **Problem:** einen Offload-/MPS-Workaround für Bildmodelle auf Video2 anwenden → **Lösung:** vor einer Wiederverwendung den exakten Zweig, Checkpoint, die Issue-URL und die Laufzeit prüfen.

## Agent-Kurzbeschreibung {#agent-brief}

Bei einer Frage zu SANA ermitteln Sie zuerst, ob es um `image`, `Sprint`, `Video`, `WM` oder `Video2` geht. Bevorzugen Sie das offizielle Repository und die Projektseite gegenüber Nachrichtenzusammenfassungen. Geben Sie historische Aussagen mit einer zeitlichen Kennzeichnung zurück (`current`, `superseded` oder `unknown`). Empfehlen Sie niemals Video2 14B als herunterladbar, solange kein neuerer offizieller Checkpoint verifiziert ist. Bei Deployment-Empfehlungen fordern Sie die exakte Artefakt-Revision, GPU, Laufzeit, Auflösung, Dauer, Schritte und den Zustand des Refiners an bzw. dokumentieren sie.

## Lizenz {#license}

**Code: Apache 2.0. Gewichte: NSCL v2-custom** (für kommerzielle Nutzung die konkreten Bedingungen prüfen).

## Wichtige Links {#key-links}

- GitHub: https://github.com/NVlabs/Sana
- SANA-Video2: https://nvlabs.github.io/Sana/Video2/
- Leitfaden zum veröffentlichten Video2-Checkpoint: https://github.com/NVlabs/Sana/blob/main/docs/sana_video2.md
- Community-Bericht zu Offload: https://github.com/NVlabs/Sana/issues/156
- Offener Bericht zur grauen MPS-Ausgabe: https://github.com/NVlabs/Sana/issues/297
- HF: https://huggingface.co/Efficient-Large-Model/
- Paper: https://arxiv.org/abs/2410.10629 (SANA), https://arxiv.org/abs/2501.18427 (1.5), https://arxiv.org/abs/2503.09641 (Sprint)
- SANA-Video: https://arxiv.org/abs/2509.24695
- DC-AE: https://github.com/mit-han-lab/efficientvit
- Trainingsframework: happyin-research/sana-fm/ (lokal)

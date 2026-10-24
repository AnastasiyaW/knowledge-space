---
level: 3
source_sha256: 65109d82c9966f1136be32a3dd2f1ad946eef09216df34c935a7e1048fa41861
translation: machine
translated_at: '2026-10-24'
---
# TIPSv2: Text-Image Pretraining mit räumlicher Wahrnehmung {#tipsv2-text-image-pretraining-with-spatial-awareness}

Google-DeepMind-Modell für die dichte räumliche Merkmalsvorhersage (Tiefe, Oberflächennormalen, Segmentierung), das pro Patch Embeddings erzeugt, die mit Text-Embeddings kompatibel bleiben.

## Architektur {#architecture}

- **Vollständiger Name:** Text-Image Pretraining with Spatial awareness v2
- **Abgedeckte Variante:** B/14 — 86M Vision-Parameter + 110M Text-Parameter
- **Zentraler Unterschied zu CLIP:** CLIP erzeugt pro Bild einen globalen Vektor, TIPSv2 erzeugt eine **Feature-Map pro Patch** (dicht). Dadurch sind DPT-Decoder-Heads (Dense Prediction Transformer) einsetzbar.
- **Backbone:** ViT-B/14 mit Patch-Größe 14, trainiert mit Zielfunktionen für räumliche Wahrnehmung zusammen mit kontrastiver Text-Bild-Ausrichtung
- **Ausgabe:** Embeddings auf Patch-Ebene mit einem Raster von 14×14 Pixeln → direkte Eingabe für DPT-Heads bei pixelgenauen Aufgaben

## Unterstützte nachgelagerte Aufgaben {#supported-downstream-tasks}

```text
image → TIPSv2 backbone → patch features
                              │
                    ┌─────────┼──────────┐
                    ▼         ▼          ▼
              depth map   normals    segmentation mask
```

Alle drei Heads nutzen dasselbe eingefrorene oder feinabgestimmte Backbone. Ein Transfer zwischen Aufgaben ist möglich, weil die Repräsentation pro Patch nicht aufgabenspezifisch ist.

### Weitere Anwendungsfälle {#additional-use-cases}

- **Backbone für nachgelagerte Vision-Aufgaben** — Patch-Embeddings lassen sich als allgemeiner dichter visueller Feature-Extraktor verwenden, ähnlich wie DINOv2, wobei die Text-Ausrichtung erhalten bleibt
- **Multimodales Retrieval mit räumlicher Verankerung** — Dank der Kompatibilität des Text-Embedding-Raums ist ein Text-Bild-Matching auf Regionsebene ohne zusätzliches Alignment-Training möglich

## Verfügbarkeitsstatus (Stand April 2026) {#availability-status-as-of-april-2026}

| Ressource | Status |
|---|---|
| `google/tipsv2-b14` auf HuggingFace | **404 — nicht verfügbar** (veröffentlicht, dann zurückgezogen) |
| HF-Demo-Space `google/tipsv2-gpu-explorer` | **Funktioniert** (Zero GPU, interaktiv) |
| ModelScope- / Gitee-Spiegel | Nicht gefunden |
| arXiv-Paper | Unter TIPSv2 nicht gefunden; vermutlich Einreichung zur CVPR 2026 |
| TIPS-**v1**-Gewichte | **Verfügbar** — `google-deepmind/tips` auf GitHub |
| TIPS-v1-Paper | arXiv [2410.16512] |

Wahrscheinlicher Grund für die Nichtverfügbarkeit von v2: Die Gewichte wurden vor der Frist für die CVPR-2026-Endfassung veröffentlicht und dann wieder zurückgezogen.

## TIPS v1 als Ersatz {#tips-v1-as-fallback}

Das v1-Paper [2410.16512] beschreibt dasselbe Konzept des Pretrainings mit räumlicher Wahrnehmung. Verwenden Sie es, falls die v2-Gewichte weiterhin nicht verfügbar sind.

```bash
# Clone v1 code and weights
git clone https://github.com/google-deepmind/tips
cd tips
pip install -r requirements.txt
```

Zentrales Inferenzmuster aus dem v1-Codebase:

```python
import tips
import torch
from PIL import Image

model = tips.load_model("tips_b14")          # downloads ~350 MB checkpoint
model.eval()

img = Image.open("photo.jpg").convert("RGB")
inputs = tips.preprocess(img)                # returns dict with pixel_values tensor

with torch.no_grad():
    outputs = model(**inputs)

# patch_features: (1, num_patches, embed_dim)
patch_features = outputs.last_hidden_state
```

Der DPT-Head für die Tiefenschätzung benötigt einen zusätzlichen feinabgestimmten Decoder. Das v1-Repository enthält vortrainierte Heads für Tiefe und Normalen.

## Vergleich mit verwandten Modellen {#comparison-with-related-models}

| Modell | Ausgabetyp | Text-Ausrichtung | Tiefe | Normalen | Segmentierung |
|---|---|---|---|---|---|
| CLIP ViT-B/16 | globales Embedding | ja | nein | nein | nein |
| DINOv2 ViT-B/14 | Patch + global | nein | über Head | über Head | über Head |
| **TIPSv2 B/14** | **Patch (dense)** | **ja** | **ja** | **ja** | **ja** |
| Depth Anything v2 | Tiefenkarte | nein | ja | nein | nein |

Das Alleinstellungsmerkmal von TIPSv2 ist die Kombination aus dichten räumlichen Features **und** Kompatibilität mit Text-Embeddings. DINOv2 liefert für sich genommen bessere dichte Features, besitzt aber keine Text-Ausrichtung.

## Überblick über DPT-Heads {#dpt-head-overview}

Dense-Prediction-Transformer-Heads (DPT) übernehmen Patch-Tokens aus einem ViT-Backbone und skalieren sie über ein mehrstufiges Fusionsschema auf volle Auflösung hoch:

```text
patch tokens (e.g., 37×37 for 518×518 input at /14 stride)
        │
  Reassemble × 4 scales  ← extracts tokens at different depths of ViT
        │
  Fusion blocks (Conv + BN + ReLU)
        │
  Final head (Conv → output channels)
        │
  Dense output (depth / normals / segmentation logits)
```

Jeder ViT, der Patch-Tokens erzeugt, kann einen DPT-Head speisen. TIPSv2 verbessert die Qualität des Heads, weil es räumlich sensitive statt rein semantischer Features liefert.

## Stolpersteine {#gotchas}

- **HF-Gewichte 404:** `google/tipsv2-b14` löst seit April 2026 `RepositoryNotFoundError` aus. Weichen Sie auf die v1-Gewichte (`google-deepmind/tips`) aus oder nutzen Sie den Live-Demo-Space nur zum Experimentieren.
- **Globales vs. patchweises Pooling:** Wenn Sie TIPSv2-Patch-Features für das Bild-Retrieval auf einen einzelnen Vektor poolen, geht die räumliche Information verloren. Verwenden Sie für DPT-Heads die vollständigen Patch-Sequenzen statt gepoolter Vektoren.
- **Patch-Schrittweite vs. Eingabegröße:** Bei einer Schrittweite von 14 ergibt ein Bild mit 224×224 Pixeln 16×16 = 256 Tokens, ein Bild mit 518×518 Pixeln etwa 37×37 = 1369 Tokens. Der Speicherbedarf wächst quadratisch, daher sollten große Bilder mit Bedacht gebatcht werden.
- **Text-Kompatibilität bedeutet keine Zero-Shot-Tiefenschätzung:** Die Text-Bild-Ausrichtung dient dem Retrieval und der Verankerung, nicht dem Steuern der Tiefenausgabe per Prompt. Für die Tiefenschätzung ist weiterhin ein trainierter DPT-Head nötig.
- **Unbekannter Qualitätsunterschied zwischen v1 und v2:** Solange das v2-Paper im Begutachtungsverfahren ist, existiert kein veröffentlichter Benchmark, der v1 und v2 vergleicht. Betrachten Sie v1 als brauchbare Näherung, nicht als bestätigtes Äquivalent.

## Überwachung auf die v2-Veröffentlichung {#monitoring-for-v2-release}

```bash
# Poll HF API for model availability
python - <<'EOF'
import requests, json
r = requests.get("https://huggingface.co/api/models/google/tipsv2-b14")
print(r.status_code, json.loads(r.text).get("error", "available"))
EOF
```

Liefert das Modell den Status 200, erfolgt der Download mit:

```python
from transformers import AutoModel, AutoProcessor
model = AutoModel.from_pretrained("google/tipsv2-b14")
processor = AutoProcessor.from_pretrained("google/tipsv2-b14")
```

## Siehe auch {#see-also}

- [[cnn-computer-vision]]
- [[transfer-learning]]
- [[generative-models]]

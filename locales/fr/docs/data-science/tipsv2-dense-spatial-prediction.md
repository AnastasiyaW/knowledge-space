---
level: 3
source_sha256: 65109d82c9966f1136be32a3dd2f1ad946eef09216df34c935a7e1048fa41861
translation: machine
translated_at: '2026-10-24'
---
# TIPSv2 : pré-entraînement texte-image avec conscience spatiale {#tipsv2-text-image-pretraining-with-spatial-awareness}

Modèle de Google DeepMind pour la prédiction de caractéristiques spatiales denses (profondeur, normales de surface, segmentation) produisant des embeddings par patch compatibles avec les embeddings de texte.

## Architecture {#architecture}

- **Nom complet :** Text-Image Pretraining with Spatial awareness v2
- **Variante couverte :** B/14 — 86M paramètres visuels + 110M paramètres textuels
- **Différence majeure avec CLIP :** CLIP produit un vecteur global unique par image ; TIPSv2 produit une **carte de caractéristiques par patch** (dense), permettant l'utilisation de têtes DPT (Dense Prediction Transformer)
- **Backbone :** ViT-B/14 à taille de patch 14, entraîné avec des objectifs de conscience spatiale en parallèle de l'alignement contrastif texte-image
- **Sortie :** embeddings au niveau du patch avec un pas de 14×14 pixels → entrée directe des têtes DPT pour les tâches au niveau du pixel

## Tâches en aval prises en charge {#supported-downstream-tasks}

```text
image → TIPSv2 backbone → patch features
                              │
                    ┌─────────┼──────────┐
                    ▼         ▼          ▼
              depth map   normals    segmentation mask
```

Les trois têtes partagent le même backbone, gelé ou affiné. Le transfert entre tâches est possible car la représentation par patch n'est pas spécifique à une tâche.

### Cas d'usage supplémentaires {#additional-use-cases}

- **Backbone pour tâches de vision en aval** — les embeddings de patch peuvent être utilisés comme extracteur général de caractéristiques visuelles denses, à l'image de DINOv2 mais avec un alignement texte préservé
- **Recherche multimodale avec ancrage spatial** — la compatibilité de l'espace d'embeddings textuels permet la correspondance texte-image au niveau des régions sans entraînement d'alignement supplémentaire

## État de disponibilité (à partir d'avril 2026) {#availability-status-as-of-april-2026}

| Ressource | Statut |
|---|---|
| `google/tipsv2-b14` sur HuggingFace | **404 — indisponible** (publié puis retiré) |
| Démo HF Space `google/tipsv2-gpu-explorer` | **Fonctionnel** (Zero GPU, interactif) |
| Miroirs ModelScope / Gitee | Non trouvés |
| Article arxiv | Non trouvé sous le nom TIPSv2 ; soumission présumée à CVPR 2026 |
| Poids de TIPS **v1** | **Disponibles** — `google-deepmind/tips` sur GitHub |
| Article TIPS v1 | arxiv [2410.16512] |

Raison probable de l'indisponibilité de v2 : poids publiés avant la date limite de la version finale de CVPR 2026, puis retirés.

## TIPS v1 comme solution de repli {#tips-v1-as-fallback}

L'article v1 [2410.16512] couvre le même concept de pré-entraînement à conscience spatiale. Utilisez-le si les poids de v2 restent indisponibles.

```bash
# Clone v1 code and weights
git clone https://github.com/google-deepmind/tips
cd tips
pip install -r requirements.txt
```

Schéma d'inférence principal issu de la base de code v1 :

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

La tête DPT pour l'estimation de profondeur nécessite un décodeur affiné supplémentaire ; le dépôt v1 fournit des têtes pré-entraînées pour la profondeur et les normales.

## Comparaison avec les modèles apparentés {#comparison-with-related-models}

| Modèle | Type de sortie | Alignement texte | Profondeur | Normales | Segmentation |
|---|---|---|---|---|---|
| CLIP ViT-B/16 | embedding global | oui | non | non | non |
| DINOv2 ViT-B/14 | patch + global | non | via tête | via tête | via tête |
| **TIPSv2 B/14** | **patch (dense)** | **oui** | **oui** | **oui** | **oui** |
| Depth Anything v2 | carte de profondeur | non | oui | non | non |

Le point distinctif de TIPSv2 est la combinaison de caractéristiques spatiales denses **et** de la compatibilité avec les embeddings de texte. DINOv2 offre de meilleures caractéristiques denses isolément, mais n'a pas d'alignement texte.

## Présentation des têtes DPT {#dpt-head-overview}

Les têtes DPT (Dense Prediction Transformer) prennent les tokens de patch d'un backbone ViT et les suréchantillonnent à pleine résolution via un schéma de fusion multi-échelle :

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

Tout ViT produisant des tokens au niveau du patch peut alimenter une tête DPT ; TIPSv2 améliore la qualité de la tête en fournissant des caractéristiques spatialement conscientes plutôt que purement sémantiques.

## Pièges à éviter {#gotchas}

- **Poids HF en 404 :** `google/tipsv2-b14` lèvera `RepositoryNotFoundError` à partir d'avril 2026. Revenez aux poids v1 (`google-deepmind/tips`) ou utilisez la démo en direct uniquement pour l'expérimentation.
- **Pooling global vs. par patch :** si vous regroupez les caractéristiques de patch de TIPSv2 en un vecteur unique pour la recherche d'images, vous perdez l'information spatiale. Utilisez les séquences complètes de patchs comme entrée des têtes DPT, et non des vecteurs regroupés.
- **Pas de patch vs. taille d'entrée :** avec un pas de /14, une image 224×224 donne 16×16 = 256 tokens ; une image 518×518 donne ~37×37 = 1369 tokens. La mémoire croît quadratiquement — dimensionnez les lots d'images volumineuses avec soin.
- **Compatibilité texte ne signifie pas profondeur zero-shot :** l'alignement texte-image sert à la recherche et à l'ancrage, non à piloter la sortie de profondeur. L'estimation de profondeur nécessite toujours une tête DPT entraînée.
- **Écart de qualité v1 / v2 inconnu :** aucun benchmark publié comparant v1 et v2 n'est disponible tant que l'article v2 est en cours d'évaluation. Considérez v1 comme une approximation raisonnable, non comme un équivalent confirmé.

## Surveillance de la sortie de v2 {#monitoring-for-v2-release}

```bash
# Poll HF API for model availability
python - <<'EOF'
import requests, json
r = requests.get("https://huggingface.co/api/models/google/tipsv2-b14")
print(r.status_code, json.loads(r.text).get("error", "available"))
EOF
```

Lorsque le modèle renvoie 200, téléchargez-le via :

```python
from transformers import AutoModel, AutoProcessor
model = AutoModel.from_pretrained("google/tipsv2-b14")
processor = AutoProcessor.from_pretrained("google/tipsv2-b14")
```

## Voir aussi {#see-also}

- [[cnn-computer-vision]]
- [[transfer-learning]]
- [[generative-models]]

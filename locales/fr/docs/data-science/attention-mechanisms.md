---
title: "Mécanismes d'attention et Transformers pour la data science"
category: concepts
tags: [data-science, attention, transformer, self-attention, nlp, tabular]
level: 3
source_sha256: 50136f70d57e52e1f0fc089f334194cfccaf070e03d5b53a32bc6d3bb6a5aece
translation: machine
translated_at: '2026-10-24'
---
# Mécanismes d'attention et Transformers pour la data science {#attention-mechanisms-and-transformers-for-data-science}

L'attention permet aux modèles de se concentrer sur les parties pertinentes de l'entrée lors de la production de chaque élément de sortie. L'auto-attention (au sein d'une même séquence) est le cœur des Transformers. À l'origine utilisés en NLP, ils sont désormais appliqués aux données tabulaires, aux séries temporelles, à la vision et à l'apprentissage multimodal.

## Mécanisme d'auto-attention {#self-attention-mechanism}

Pour chaque élément, calculer le degré d'attention à accorder à chacun des autres éléments :

1. Projeter l'entrée dans les matrices Query (Q), Key (K) et Value (V)
2. Poids d'attention = softmax(Q * K^T / sqrt(d_k))
3. Sortie = somme pondérée de V

```python
import torch
import torch.nn as nn
import math

class SelfAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.qkv = nn.Linear(embed_dim, 3 * embed_dim)
        self.out = nn.Linear(embed_dim, embed_dim)

    def forward(self, x):
        B, N, C = x.shape
        qkv = self.qkv(x).reshape(B, N, 3, self.num_heads, self.head_dim)
        qkv = qkv.permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]

        # Scaled dot-product attention
        attn = (q @ k.transpose(-2, -1)) * (self.head_dim ** -0.5)
        attn = attn.softmax(dim=-1)

        x = (attn @ v).transpose(1, 2).reshape(B, N, C)
        return self.out(x)
```

**Attention multi-têtes** : exécuter en parallèle plusieurs têtes d'attention avec des projections apprises différentes. Chaque tête peut se concentrer sur des aspects différents de l'entrée.

## Bloc Transformer {#transformer-block}

```python
class TransformerBlock(nn.Module):
    def __init__(self, embed_dim, num_heads, mlp_ratio=4, dropout=0.1):
        super().__init__()
        self.norm1 = nn.LayerNorm(embed_dim)
        self.attn = SelfAttention(embed_dim, num_heads)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.mlp = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * mlp_ratio),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(embed_dim * mlp_ratio, embed_dim),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        x = x + self.attn(self.norm1(x))   # residual + pre-norm
        x = x + self.mlp(self.norm2(x))
        return x
```

## Modèles Transformers pour le NLP {#nlp-transformer-models}

### Encodeur seul (style BERT) {#encoder-only-bert-style}

Contexte bidirectionnel. Idéal pour la classification, la reconnaissance d'entités nommées (NER) et les embeddings.

```python
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

inputs = tokenizer("Machine learning is powerful", return_tensors="pt")
outputs = model(**inputs)
embeddings = outputs.last_hidden_state  # (batch, seq_len, 768)
cls_embedding = outputs.last_hidden_state[:, 0, :]  # [CLS] token
```

### Décodeur seul (style GPT) {#decoder-only-gpt-style}

Génération autorégressive. Masquage causal : chaque token ne s'intéresse qu'aux tokens précédents.

### Encodeur-décodeur (T5, BART) {#encoder-decoder-t5-bart}

Tâches seq2seq : traduction, résumé automatique, réponse à des questions.

## Transformers pour les données tabulaires {#transformers-for-tabular-data}

### TabTransformer {#tabtransformer}

Plonger les variables catégorielles en tant que tokens, puis appliquer des couches Transformer :

```python
# Conceptual TabTransformer
class TabTransformer(nn.Module):
    def __init__(self, cat_dims, num_continuous, num_classes, dim=32, depth=6):
        super().__init__()
        # Categorical embeddings
        self.cat_embeds = nn.ModuleList([
            nn.Embedding(n, dim) for n in cat_dims
        ])
        # Transformer on categorical features
        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=dim, nhead=8),
            num_layers=depth
        )
        # Combine with numerical features
        total_dim = len(cat_dims) * dim + num_continuous
        self.head = nn.Linear(total_dim, num_classes)

    def forward(self, x_cat, x_num):
        cat_embs = [emb(x_cat[:, i]) for i, emb in enumerate(self.cat_embeds)]
        cat_tensor = torch.stack(cat_embs, dim=1)
        cat_out = self.transformer(cat_tensor).flatten(1)
        combined = torch.cat([cat_out, x_num], dim=1)
        return self.head(combined)
```

### FT-Transformer {#ft-transformer}

État de l'art pour les données tabulaires. Traite TOUTES les variables (numériques et catégorielles) comme des tokens.

**Constat clé** : sur de nombreux benchmarks tabulaires, le gradient boosting surpasse encore les Transformers. FT-Transformer est compétitif, mais n'est pas systématiquement meilleur que XGBoost/CatBoost.

## Transformers pour les séries temporelles {#transformers-for-time-series}

```python
# Informer-style time series forecasting (simplified)
class TimeSeriesTransformer(nn.Module):
    def __init__(self, input_dim, d_model, nhead, num_layers, pred_len):
        super().__init__()
        self.input_proj = nn.Linear(input_dim, d_model)
        self.pos_encoding = PositionalEncoding(d_model)
        self.encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model, nhead, dim_feedforward=d_model*4),
            num_layers=num_layers
        )
        self.decoder = nn.Linear(d_model, pred_len)

    def forward(self, x):
        x = self.input_proj(x)
        x = self.pos_encoding(x)
        x = self.encoder(x)
        return self.decoder(x[:, -1, :])  # predict from last token
```

## Encodage positionnel {#positional-encoding}

Les Transformers n'ont pas de notion d'ordre intrinsèque. Il faut ajouter une information de position :

- **Sinusoïdal** : fixe, fonctionne bien pour des longueurs de séquence modérées
- **Appris** : embeddings entraînables par position
- **Rotatif (RoPE)** : position relative, extrapole à des séquences plus longues
- **ALiBi** : biais d'attention basé sur la distance, sans paramètre supplémentaire

## Pièges à éviter {#gotchas}

- **Mémoire quadratique en fonction de la longueur de séquence** : l'auto-attention est en O(n^2) en mémoire et en calcul. Pour des séquences de plus de 2048 tokens, utiliser des variantes d'attention efficaces (Flash Attention, attention linéaire) ou découper l'entrée en morceaux
- **Les Transformers nécessitent plus de données que les CNN/arbres** : sans grands jeux de données ni pré-entraînement, les Transformers sous-performent les architectures plus simples. Pour des données tabulaires de moins de 10K échantillons, le gradient boosting gagne presque toujours. Utiliser des modèles pré-entraînés lorsque c'est possible
- **Le warmup du taux d'apprentissage est critique** : les Transformers sont sensibles au taux d'apprentissage initial. Pratique standard : warmup linéaire sur les 5 à 10 % premiers pas, puis décroissance cosinus ou linéaire. Sans warmup, l'entraînement diverge souvent

## Voir aussi {#see-also}

- [[neural-networks]]
- [[nlp-text-processing]]
- [[rnn-sequences]]
- [[time-series-analysis]]

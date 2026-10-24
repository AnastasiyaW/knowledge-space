---
title: "Aufmerksamkeitsmechanismen und Transformer für Data Science"
category: concepts
tags: [data-science, attention, transformer, self-attention, nlp, tabular]
level: 3
source_sha256: 50136f70d57e52e1f0fc089f334194cfccaf070e03d5b53a32bc6d3bb6a5aece
translation: machine
translated_at: '2026-10-24'
---
# Aufmerksamkeitsmechanismen und Transformer für Data Science {#attention-mechanisms-and-transformers-for-data-science}

Aufmerksamkeit (Attention) ermöglicht es Modellen, bei der Erzeugung jedes Ausgabeelements auf die relevanten Teile der Eingabe zu fokussieren. Self-Attention (innerhalb derselben Sequenz) ist der Kern von Transformern. Ursprünglich für NLP entwickelt, werden sie inzwischen auch auf tabellarische Daten, Zeitreihen, Bildverarbeitung und multimodales Lernen angewendet.

## Self-Attention-Mechanismus {#self-attention-mechanism}

Für jedes Element wird berechnet, wie stark auf jedes andere Element geachtet werden soll:

1. Eingabe in die Matrizen Query (Q), Key (K) und Value (V) projizieren
2. Attention-Gewichte = softmax(Q * K^T / sqrt(d_k))
3. Ausgabe = gewichtete Summe von V

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

**Multi-Head-Attention**: Mehrere Attention-Heads werden parallel mit unterschiedlichen, gelernten Projektionen ausgeführt. Jeder Head kann auf unterschiedliche Aspekte der Eingabe achten.

## Transformer-Block {#transformer-block}

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

## NLP-Transformer-Modelle {#nlp-transformer-models}

### Nur Encoder (BERT-Stil) {#encoder-only-bert-style}

Bidirektionaler Kontext. Am besten geeignet für Klassifikation, NER und Embeddings.

```python
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

inputs = tokenizer("Machine learning is powerful", return_tensors="pt")
outputs = model(**inputs)
embeddings = outputs.last_hidden_state  # (batch, seq_len, 768)
cls_embedding = outputs.last_hidden_state[:, 0, :]  # [CLS] token
```

### Nur Decoder (GPT-Stil) {#decoder-only-gpt-style}

Autoregressive Generierung. Kausales Masking: Jedes Token achtet nur auf vorherige Tokens.

### Encoder-Decoder (T5, BART) {#encoder-decoder-t5-bart}

Seq2seq-Aufgaben: Übersetzung, Zusammenfassung, Fragebeantwortung.

## Transformer für tabellarische Daten {#transformers-for-tabular-data}

### TabTransformer {#tabtransformer}

Kategoriale Merkmale werden als Tokens eingebettet, anschließend werden Transformer-Schichten angewendet:

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

State of the Art für tabellarische Daten. Behandelt ALLE Merkmale (numerisch und kategorisch) als Tokens.

**Wichtige Erkenntnis**: Bei vielen tabellarischen Benchmarks schlagen Gradient-Boosting-Verfahren Transformer weiterhin. Der FT-Transformer ist konkurrenzfähig, aber nicht durchgängig besser als XGBoost/CatBoost.

## Transformer für Zeitreihen {#transformers-for-time-series}

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

## Positionskodierung {#positional-encoding}

Transformer besitzen keine inhärente Vorstellung von Reihenfolge. Daher werden Positionsinformationen hinzugefügt:

- **Sinusförmig**: fest, funktioniert gut für moderate Sequenzlängen
- **Gelernt**: trainierbare Embeddings pro Position
- **Rotary (RoPE)**: relative Position, extrapoliert auf längere Sequenzen
- **ALiBi**: distanzbasierter Attention-Bias, ohne zusätzliche Parameter

## Stolperfallen {#gotchas}

- **Quadratischer Speicherbedarf in der Sequenzlänge**: Self-Attention ist in Speicher und Rechenaufwand O(n^2). Für Sequenzen mit mehr als 2048 Tokens sollten effiziente Attention-Varianten (Flash Attention, lineare Attention) verwendet oder die Eingabe in Abschnitte zerlegt werden
- **Transformer benötigen mehr Daten als CNNs/Bäume**: Ohne große Datensätze oder Pretraining unterperformen Transformer einfacheren Architekturen. Für tabellarische Daten mit weniger als 10K Samples gewinnt Gradient Boosting nahezu immer. Nach Möglichkeit vortrainierte Modelle verwenden
- **Learning-Rate-Warmup ist entscheidend**: Transformer reagieren empfindlich auf die initiale Lernrate. Üblich ist ein lineares Warmup über die ersten 5–10 % der Schritte, danach ein Cosine- oder linearer Decay. Ohne Warmup divergiert das Training häufig

## Siehe auch {#see-also}

- [[neural-networks]]
- [[nlp-text-processing]]
- [[rnn-sequences]]
- [[time-series-analysis]]

---
title: Attention Mechanisms and Transformers for Data Science
category: concepts
tags: [data-science, attention, transformer, self-attention, nlp, tabular]
---

# Attention Mechanisms and Transformers for Data Science

Attention allows models to focus on relevant parts of the input when producing each output element. Self-attention (within same sequence) is the core of Transformers. Originally NLP, now applied to tabular data, time series, vision, and multi-modal learning.

## Self-Attention Mechanism

For each element, compute how much attention to pay to every other element:

1. Project input into Query (Q), Key (K), Value (V) matrices
2. Attention weights = softmax(Q * K^T / sqrt(d_k))
3. Output = weighted sum of V

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

**Multi-head attention**: run multiple attention heads in parallel with different learned projections. Each head can attend to different aspects of the input.

## Transformer Block

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

## NLP Transformer Models

### Encoder-Only (BERT-style)

Bidirectional context. Best for classification, NER, embeddings.

```python
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

inputs = tokenizer("Machine learning is powerful", return_tensors="pt")
outputs = model(**inputs)
embeddings = outputs.last_hidden_state  # (batch, seq_len, 768)
cls_embedding = outputs.last_hidden_state[:, 0, :]  # [CLS] token
```

### Decoder-Only (GPT-style)

Autoregressive generation. Causal masking - each token only attends to previous tokens.

### Encoder-Decoder (T5, BART)

Seq2seq tasks: translation, summarization, question answering.

## Transformers for Tabular Data

### TabTransformer

Embed categorical features as tokens, apply transformer layers:

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

### FT-Transformer

State-of-art for tabular. Treats ALL features (numerical + categorical) as tokens.

**Key finding**: on many tabular benchmarks, gradient boosting still beats transformers. FT-Transformer is competitive but not consistently better than XGBoost/CatBoost.

## Transformers for Time Series

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

## Positional Encoding

Transformers have no inherent notion of order. Add position information:

- **Sinusoidal**: fixed, works well for moderate sequence lengths
- **Learned**: trainable embeddings per position
- **Rotary (RoPE)**: relative position, extrapolates to longer sequences
- **ALiBi**: attention bias based on distance, no extra parameters

## Gotchas

- **Quadratic memory in sequence length**: self-attention is O(n^2) in memory and compute. For sequences > 2048 tokens, use efficient attention variants (Flash Attention, linear attention) or chunk the input
- **Transformers need more data than CNNs/trees**: without large datasets or pretraining, transformers underperform simpler architectures. For tabular data with < 10K samples, gradient boosting almost always wins. Use pretrained models when possible
- **Learning rate warmup is critical**: transformers are sensitive to initial learning rate. Standard practice: linear warmup for first 5-10% of steps, then cosine or linear decay. Without warmup, training often diverges

## See Also

- [[neural-networks]]
- [[nlp-text-processing]]
- [[rnn-sequences]]
- [[time-series-analysis]]

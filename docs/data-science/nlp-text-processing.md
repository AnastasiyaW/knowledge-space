---
title: NLP and Text Processing
category: models
tags: [data-science, nlp, text, transformers, bert, embeddings]
---

# NLP and Text Processing

From bag-of-words to transformers - NLP has evolved from manual feature engineering to pre-trained language models. Modern NLP: fine-tune a pre-trained model, don't build from scratch.

## Text Preprocessing Pipeline

### Tokenization
```python
# Simple
tokens = text.split()

# NLTK
from nltk.tokenize import word_tokenize
tokens = word_tokenize(text)

# Subword (BPE/WordPiece) - used by modern models
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
tokens = tokenizer.tokenize(text)
```

### Cleaning
```python
import re
text = text.lower()
text = re.sub(r'[^a-zA-Z\s]', '', text)  # remove non-alpha
```

### Stop Words and Lemmatization
```python
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english'))
tokens = [w for w in tokens if w not in stop_words]

lemmatizer = WordNetLemmatizer()
lemmatizer.lemmatize('running', pos='v')  # 'run'
```

**Stemming** (crude suffix removal) vs **Lemmatization** (dictionary-based). Lemmatization is more accurate: "better" -> "good" (lemma), "better" -> "better" (stem fails).

## Text Vectorization

### Bag of Words (BoW)
```python
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_features=5000)
X = vectorizer.fit_transform(texts)  # sparse matrix
```

### TF-IDF
Weight words by importance: high TF-IDF = word is distinctive for this document.

TF(t,d) = count(t in d) / total_words(d)
IDF(t) = log(total_docs / docs_containing(t))
TF-IDF = TF * IDF

```python
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
X = tfidf.fit_transform(texts)
```

### Word Embeddings
Dense vector representations. Similar words have similar vectors.

```python
import gensim.downloader as api
model = api.load('word2vec-google-news-300')
vector = model['king']  # 300-dim
model.most_similar('king')
# king - man + woman ~ queen
```

- **Word2Vec**: CBOW (predict word from context) or Skip-gram (predict context from word)
- **GloVe**: trained on global co-occurrence statistics

## Sequence Models

### RNN / LSTM / GRU
Process tokens sequentially, maintaining hidden state.

- **Simple RNN**: vanishing gradients for long sequences
- **LSTM**: forget/input/output gates. Handles ~200-500 tokens
- **GRU**: simplified LSTM with two gates. Similar performance, fewer parameters
- **Bidirectional**: process forward AND backward, concatenate

```python
import torch.nn as nn
lstm = nn.LSTM(input_size=300, hidden_size=128, num_layers=2,
               bidirectional=True, batch_first=True)
```

## Transformer Architecture

Replaced RNNs. Key innovation: self-attention captures any-distance dependencies in one step.

### Self-Attention
For each token, compute attention weights to ALL other tokens.

Q, K, V = linear projections of input
Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V

**Multi-Head Attention**: parallel attention with different projections. Each head captures different relationship types.

### Components
- **Positional Encoding**: inject position information (no inherent order)
- **Layer Normalization**: stabilize training
- **Feed-Forward Network**: per-position MLP after attention
- **Residual Connections**: around every sub-layer

## BERT

Pre-trained bidirectional encoder. Fine-tune for downstream tasks.

**Pre-training objectives:**
1. Masked Language Model (MLM): predict 15% masked tokens
2. Next Sentence Prediction (NSP): predict if B follows A

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = 'bert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

inputs = tokenizer("Great movie!", return_tensors="pt",
                   padding=True, truncation=True, max_length=512)

# Fine-tuning with Trainer
from transformers import Trainer, TrainingArguments
args = TrainingArguments(output_dir='./results', num_train_epochs=3,
                         per_device_train_batch_size=16, learning_rate=2e-5)
trainer = Trainer(model=model, args=args, train_dataset=train_ds, eval_dataset=eval_ds)
trainer.train()
```

### BERT Variants
- **DistilBERT**: 6 layers, 40% smaller, 60% faster, 97% performance
- **RoBERTa**: better pre-training (more data, no NSP)
- **ALBERT**: parameter sharing, smaller model
- **XLNet**: permutation-based bidirectional context

## Fundamental NLP Terminology

| Term | Definition |
|------|-----------|
| **Token** | General unit of text - can be a word, subword, punctuation, or character |
| **Vocabulary** | Set of all unique tokens the model knows. Typically 10K-100K+ tokens |
| **Corpus** | Dataset of text documents used for training |
| **N-gram** | Sequence of N consecutive tokens. Unigram (1), bigram (2), trigram (3) |
| **Sentence tokenization** | Splitting text into sentences (NLTK `sent_tokenize`) |
| **Word tokenization** | Splitting sentence into words/tokens |
| **Subword tokenization** | BPE/WordPiece splits rare words into known subunits |

**Character vs Word models**: word-level models have richer semantics but sparse coverage. Character-level models handle any text but need more context to be meaningful. Subword tokenization is the standard compromise used by all modern transformers.

## Sequence Data Taxonomy

Different NLP tasks have different input/output shapes:

| Task | Input (X) | Output (Y) | Example |
|------|-----------|------------|---------|
| Sentiment analysis | Sequence | Single label | "Great movie!" -> 5 stars |
| NER | Sequence | Sequence (same length) | "Harry Potter met..." -> [PER, PER, O, ...] |
| Machine translation | Sequence | Sequence (diff length) | French sentence -> English sentence |
| Speech recognition | Audio sequence | Text sequence | Waveform -> "the quick brown fox" |
| Music generation | Empty/seed | Sequence | Genre ID -> musical notes |
| Text summarization | Sequence | Shorter sequence | Full article -> 3-sentence summary |

## Common NLP Tasks

- **Text Classification**: sentiment, spam, topic categorization
- **NER** (Named Entity Recognition): extract persons, organizations, locations
- **Question Answering**: extract answer span from context
- **Machine Translation**: sequence-to-sequence with attention
- **Summarization**: extractive (select sentences) or abstractive (generate). See [[text-summarization]]
- **Text Generation**: GPT-family autoregressive models
- **Language Modeling**: predict next token given context. See [[probabilistic-language-models]]

## Practical Tips

1. Start with pre-trained models - almost always better than from-scratch
2. BERT fine-tuning LR: 2e-5 to 5e-5 (much lower than training from scratch)
3. Max sequence: BERT = 512 tokens. Truncate or chunk longer texts
4. Tokenizer must match model (BERT tokenizer with BERT model)
5. For simple tasks + small data: TF-IDF + logistic regression is surprisingly competitive
6. Use HuggingFace Transformers library for unified API

## Gotchas
- Tokenizer mismatch crashes silently (wrong embeddings)
- Subword tokenization means token count != word count
- BERT is encoder-only (classification, NER), GPT is decoder-only (generation)
- Fine-tuning on tiny datasets (< 1000 samples) may not improve over TF-IDF + classical ML
- Multilingual models (mBERT, XLM-R) work but worse than language-specific models

## See Also
- [[neural-networks]] - general deep learning
- [[transfer-learning]] - pre-training and fine-tuning
- [[feature-engineering]] - text-based feature engineering
- [[model-evaluation]] - NLP-specific evaluation metrics
- [[text-summarization]] - extractive and abstractive summarization
- [[probabilistic-language-models]] - n-grams, Markov chains, cipher decryption

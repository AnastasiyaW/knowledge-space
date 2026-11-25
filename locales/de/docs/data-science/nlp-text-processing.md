---
title: "NLP und Textverarbeitung"
category: models
tags: [data-science, nlp, text, transformers, bert, embeddings]
level: 3
source_sha256: 543a8be9ee73db3628383d0ba1410b7e24e5f5a8cbaba2be6d684f28b370339d
translation: machine
translated_at: '2026-10-24'
---
# NLP und Textverarbeitung {#nlp-and-text-processing}

Von Bag-of-Words bis zu Transformern: NLP hat sich von manuellem Feature Engineering zu vortrainierten Sprachmodellen entwickelt. Modernes NLP heißt: ein vortrainiertes Modell feinabstimmen (Fine-Tuning), nicht von Grund auf neu bauen.

## Pipeline zur Textvorverarbeitung {#text-preprocessing-pipeline}

### Tokenisierung {#tokenization}
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

### Bereinigung {#cleaning}
```python
import re
text = text.lower()
text = re.sub(r'[^a-zA-Z\s]', '', text)  # remove non-alpha
```

### Stoppwörter und Lemmatisierung {#stop-words-and-lemmatization}
```python
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english'))
tokens = [w for w in tokens if w not in stop_words]

lemmatizer = WordNetLemmatizer()
lemmatizer.lemmatize('running', pos='v')  # 'run'
```

**Stemming** (grobes Entfernen von Suffixen) vs. **Lemmatisierung** (wörterbuchbasiert). Lemmatisierung ist genauer: „better“ -> „good“ (Lemma), „better“ -> „better“ (Stemming versagt).

## Textvektorisierung {#text-vectorization}

### Bag of Words (BoW) {#bag-of-words-bow}
```python
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_features=5000)
X = vectorizer.fit_transform(texts)  # sparse matrix
```

### TF-IDF {#tf-idf}
Gewichtet Wörter nach ihrer Bedeutung: hoher TF-IDF-Wert = Wort ist für dieses Dokument charakteristisch.

TF(t,d) = count(t in d) / total_words(d)
IDF(t) = log(total_docs / docs_containing(t))
TF-IDF = TF * IDF

```python
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
X = tfidf.fit_transform(texts)
```

### Wort-Embeddings {#word-embeddings}
Dichte Vektorrepräsentationen. Ähnliche Wörter haben ähnliche Vektoren.

```python
import gensim.downloader as api
model = api.load('word2vec-google-news-300')
vector = model['king']  # 300-dim
model.most_similar('king')
# king - man + woman ~ queen
```

- **Word2Vec**: CBOW (Wort aus Kontext vorhersagen) oder Skip-gram (Kontext aus Wort vorhersagen)
- **GloVe**: trainiert auf globalen Ko-Okkurrenzstatistiken

## Sequenzmodelle {#sequence-models}

### RNN / LSTM / GRU {#rnn-lstm-gru}
Verarbeiten Tokens sequenziell und halten dabei einen versteckten Zustand (Hidden State).

- **Einfaches RNN**: verschwindende Gradienten bei langen Sequenzen
- **LSTM**: Forget-, Input- und Output-Gates. Verarbeitet ca. 200–500 Tokens
- **GRU**: vereinfachtes LSTM mit zwei Gates. Ähnliche Leistung, weniger Parameter
- **Bidirektional**: verarbeitet vorwärts UND rückwärts und verkettet die Ergebnisse

```python
import torch.nn as nn
lstm = nn.LSTM(input_size=300, hidden_size=128, num_layers=2,
               bidirectional=True, batch_first=True)
```

## Transformer-Architektur {#transformer-architecture}

Ersetzten die RNNs. Die zentrale Neuerung: Self-Attention erfasst Abhängigkeiten über beliebige Distanzen in einem Schritt.

### Self-Attention {#self-attention}
Für jedes Token werden Attention-Gewichte zu ALLEN anderen Tokens berechnet.

Q, K, V = lineare Projektionen der Eingabe
Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V

**Multi-Head Attention**: parallele Attention mit unterschiedlichen Projektionen. Jeder Head erfasst andere Arten von Beziehungen.

### Komponenten {#components}
- **Positional Encoding**: fügt Positionsinformation hinzu (keine inhärente Reihenfolge)
- **Layer Normalization**: stabilisiert das Training
- **Feed-Forward-Netzwerk**: positionsweises MLP nach der Attention
- **Residualverbindungen**: um jede Teilschicht

## BERT {#bert}

Vortrainierter bidirektionaler Encoder. Wird für nachgelagerte Aufgaben feinabgestimmt.

**Pre-Training-Ziele:**
1. Masked Language Model (MLM): 15 % maskierte Tokens vorhersagen
2. Next Sentence Prediction (NSP): vorhersagen, ob B auf A folgt

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

### BERT-Varianten {#bert-variants}
- **DistilBERT**: 6 Schichten, 40 % kleiner, 60 % schneller, 97 % der Leistung
- **RoBERTa**: besseres Pre-Training (mehr Daten, kein NSP)
- **ALBERT**: Parameter-Sharing, kleineres Modell
- **XLNet**: permutationsbasierter bidirektionaler Kontext

## Grundlegende NLP-Terminologie {#fundamental-nlp-terminology}

| Begriff | Definition |
|------|-----------|
| **Token** | Allgemeine Texteinheit – kann ein Wort, Subwort, Satzzeichen oder Zeichen sein |
| **Vokabular** | Menge aller eindeutigen Tokens, die das Modell kennt. Typischerweise 10K–100K+ Tokens |
| **Korpus** | Datensatz aus Textdokumenten für das Training |
| **N-Gramm** | Folge von N aufeinanderfolgenden Tokens. Unigramm (1), Bigramm (2), Trigramm (3) |
| **Satztokenisierung** | Zerlegen des Textes in Sätze (NLTK `sent_tokenize`) |
| **Worttokenisierung** | Zerlegen eines Satzes in Wörter/Tokens |
| **Subwort-Tokenisierung** | BPE/WordPiece zerlegt seltene Wörter in bekannte Teileinheiten |

**Zeichen- vs. Wortmodelle**: Wortbasierte Modelle haben reichhaltigere Semantik, aber eine dünne Abdeckung. Zeichenbasierte Modelle verarbeiten jeden Text, benötigen aber mehr Kontext, um aussagekräftig zu sein. Die Subwort-Tokenisierung ist der Standardkompromiss, den alle modernen Transformer verwenden.

## Taxonomie der Sequenzdaten {#sequence-data-taxonomy}

Verschiedene NLP-Aufgaben haben unterschiedliche Ein- und Ausgabeformen:

| Aufgabe | Eingabe (X) | Ausgabe (Y) | Beispiel |
|------|-----------|------------|---------|
| Sentimentanalyse | Sequenz | Einzelnes Label | „Toller Film!“ -> 5 Sterne |
| NER | Sequenz | Sequenz (gleiche Länge) | „Harry Potter met...“ -> [PER, PER, O, ...] |
| Maschinelle Übersetzung | Sequenz | Sequenz (andere Länge) | Französischer Satz -> englischer Satz |
| Spracherkennung | Audiosequenz | Textsequenz | Wellenform -> „the quick brown fox“ |
| Musikgenerierung | Leer/Seed | Sequenz | Genre-ID -> Noten |
| Textzusammenfassung | Sequenz | Kürzere Sequenz | Vollständiger Artikel -> Zusammenfassung in 3 Sätzen |

## Häufige NLP-Aufgaben {#common-nlp-tasks}

- **Textklassifikation**: Sentiment, Spam, Themenkategorisierung
- **NER** (Named Entity Recognition): Personen, Organisationen, Orte extrahieren
- **Question Answering**: Antwortspanne aus dem Kontext extrahieren
- **Maschinelle Übersetzung**: Sequence-to-Sequence mit Attention
- **Zusammenfassung**: extraktiv (Sätze auswählen) oder abstraktiv (generieren). Siehe [[text-summarization]]
- **Textgenerierung**: autoregressive Modelle der GPT-Familie
- **Sprachmodellierung**: nächstes Token aus dem Kontext vorhersagen. Siehe [[probabilistic-language-models]]

## Praktische Tipps {#practical-tips}

1. Mit vortrainierten Modellen beginnen – fast immer besser als Training von Grund auf
2. Lernrate für BERT-Fine-Tuning: 2e-5 bis 5e-5 (deutlich niedriger als beim Training von Grund auf)
3. Maximale Sequenzlänge: BERT = 512 Tokens. Längere Texte kürzen oder in Abschnitte zerlegen
4. Tokenizer muss zum Modell passen (BERT-Tokenizer mit BERT-Modell)
5. Bei einfachen Aufgaben und wenig Daten: TF-IDF + logistische Regression ist überraschend konkurrenzfähig
6. Für eine einheitliche API die HuggingFace-Transformers-Bibliothek verwenden

## Stolpersteine {#gotchas}
- Ein nicht passender Tokenizer führt stillschweigend zu Fehlern (falsche Embeddings)
- Subwort-Tokenisierung bedeutet: Anzahl der Tokens ≠ Anzahl der Wörter
- BERT ist ein reiner Encoder (Klassifikation, NER), GPT ist ein reiner Decoder (Generierung)
- Fine-Tuning auf winzigen Datensätzen (< 1000 Beispiele) bringt gegenüber TF-IDF + klassischem ML unter Umständen keine Verbesserung
- Mehrsprachige Modelle (mBERT, XLM-R) funktionieren, sind aber schwächer als sprachspezifische Modelle

## Siehe auch {#see-also}
- [[neural-networks]] – allgemeines Deep Learning
- [[transfer-learning]] – Pre-Training und Fine-Tuning
- [[feature-engineering]] – textbasiertes Feature Engineering
- [[model-evaluation]] – NLP-spezifische Evaluationsmetriken
- [[text-summarization]] – extraktive und abstraktive Zusammenfassung
- [[probabilistic-language-models]] – N-Gramme, Markov-Ketten, Chiffrierentschlüsselung

---
title: "NLP et traitement de texte"
category: models
tags: [data-science, nlp, text, transformers, bert, embeddings]
level: 3
source_sha256: 543a8be9ee73db3628383d0ba1410b7e24e5f5a8cbaba2be6d684f28b370339d
translation: machine
translated_at: '2026-10-24'
---
# NLP et traitement de texte {#nlp-and-text-processing}

Du sac de mots aux transformers, le NLP est passé de l'ingénierie manuelle des caractéristiques aux modèles de langage pré-entraînés. NLP moderne : affiner (fine-tuner) un modèle pré-entraîné, ne pas construire from scratch.

## Pipeline de prétraitement du texte {#text-preprocessing-pipeline}

### Tokenisation {#tokenization}
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

### Nettoyage {#cleaning}
```python
import re
text = text.lower()
text = re.sub(r'[^a-zA-Z\s]', '', text)  # remove non-alpha
```

### Mots vides et lemmatisation {#stop-words-and-lemmatization}
```python
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english'))
tokens = [w for w in tokens if w not in stop_words]

lemmatizer = WordNetLemmatizer()
lemmatizer.lemmatize('running', pos='v')  # 'run'
```

**Stemming** (suppression grossière des suffixes) vs **lemmatisation** (basée sur un dictionnaire). La lemmatisation est plus précise : « better » -> « good » (lemme), « better » -> « better » (le stemming échoue).

## Vectorisation du texte {#text-vectorization}

### Sac de mots (BoW) {#bag-of-words-bow}
```python
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_features=5000)
X = vectorizer.fit_transform(texts)  # sparse matrix
```

### TF-IDF {#tf-idf}
Pondère les mots selon leur importance : un TF-IDF élevé signifie que le mot est distinctif pour ce document.

TF(t,d) = nombre(t dans d) / total_mots(d)
IDF(t) = log(total_documents / documents_contenant(t))
TF-IDF = TF * IDF

```python
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
X = tfidf.fit_transform(texts)
```

### Embeddings de mots {#word-embeddings}
Représentations vectorielles denses. Des mots similaires ont des vecteurs similaires.

```python
import gensim.downloader as api
model = api.load('word2vec-google-news-300')
vector = model['king']  # 300-dim
model.most_similar('king')
# king - man + woman ~ queen
```

- **Word2Vec** : CBOW (prédit le mot à partir du contexte) ou Skip-gram (prédit le contexte à partir du mot)
- **GloVe** : entraîné sur les statistiques globales de cooccurrence

## Modèles de séquences {#sequence-models}

### RNN / LSTM / GRU {#rnn-lstm-gru}
Traitent les tokens séquentiellement en maintenant un état caché.

- **RNN simple** : gradients évanescents pour les longues séquences
- **LSTM** : portes d'oubli, d'entrée et de sortie. Gère environ 200 à 500 tokens
- **GRU** : LSTM simplifié à deux portes. Performances similaires, moins de paramètres
- **Bidirectionnel** : traite en sens avant ET arrière, puis concatène

```python
import torch.nn as nn
lstm = nn.LSTM(input_size=300, hidden_size=128, num_layers=2,
               bidirectional=True, batch_first=True)
```

## Architecture Transformer {#transformer-architecture}

Ont remplacé les RNN. Innovation clé : l'auto-attention capture les dépendances à n'importe quelle distance en une seule étape.

### Auto-attention {#self-attention}
Pour chaque token, calcule les poids d'attention vers TOUS les autres tokens.

Q, K, V = projections linéaires de l'entrée
Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V

**Attention multi-têtes** : attention parallèle avec des projections différentes. Chaque tête capture un type de relation différent.

### Composants {#components}
- **Encodage positionnel** : injecte l'information de position (pas d'ordre intrinsèque)
- **Normalisation de couche** : stabilise l'entraînement
- **Réseau feed-forward** : MLP appliqué à chaque position après l'attention
- **Connexions résiduelles** : autour de chaque sous-couche

## BERT {#bert}

Encodeur bidirectionnel pré-entraîné. À affiner pour les tâches en aval.

**Objectifs de pré-entraînement :**
1. Modèle de langage masqué (MLM) : prédire 15 % des tokens masqués
2. Prédiction de la phrase suivante (NSP) : prédire si B suit A

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

### Variantes de BERT {#bert-variants}
- **DistilBERT** : 6 couches, 40 % plus petit, 60 % plus rapide, 97 % des performances
- **RoBERTa** : meilleur pré-entraînement (plus de données, sans NSP)
- **ALBERT** : partage de paramètres, modèle plus petit
- **XLNet** : contexte bidirectionnel basé sur les permutations

## Terminologie fondamentale du NLP {#fundamental-nlp-terminology}

| Terme | Définition |
|-------|-----------|
| **Token** | Unité générale de texte : peut être un mot, un sous-mot, une ponctuation ou un caractère |
| **Vocabulaire** | Ensemble de tous les tokens uniques connus du modèle. Généralement 10K à 100K+ tokens |
| **Corpus** | Jeu de données de documents texte utilisé pour l'entraînement |
| **N-gramme** | Séquence de N tokens consécutifs. Unigramme (1), bigramme (2), trigramme (3) |
| **Tokenisation en phrases** | Découpage du texte en phrases (`sent_tokenize` de NLTK) |
| **Tokenisation en mots** | Découpage d'une phrase en mots/tokens |
| **Tokenisation en sous-mots** | BPE/WordPiece découpe les mots rares en sous-unités connues |

**Modèles au niveau caractère vs mot** : les modèles au niveau mot ont une sémantique plus riche mais une couverture creuse. Les modèles au niveau caractère gèrent tout texte mais ont besoin de plus de contexte pour être signifiants. La tokenisation en sous-mots est le compromis standard utilisé par tous les transformers modernes.

## Taxonomie des données de séquences {#sequence-data-taxonomy}

Les différentes tâches de NLP ont des formes d'entrée/sortie différentes :

| Tâche | Entrée (X) | Sortie (Y) | Exemple |
|-------|-----------|------------|---------|
| Analyse de sentiment | Séquence | Étiquette unique | « Great movie! » -> 5 étoiles |
| NER | Séquence | Séquence (même longueur) | « Harry Potter met... » -> [PER, PER, O, ...] |
| Traduction automatique | Séquence | Séquence (longueur différente) | Phrase française -> phrase anglaise |
| Reconnaissance vocale | Séquence audio | Séquence de texte | Forme d'onde -> « the quick brown fox » |
| Génération de musique | Vide/graine | Séquence | ID de genre -> notes de musique |
| Résumé automatique | Séquence | Séquence plus courte | Article complet -> résumé de 3 phrases |

## Tâches courantes du NLP {#common-nlp-tasks}

- **Classification de texte** : sentiment, spam, catégorisation par thème
- **NER** (reconnaissance d'entités nommées) : extraire personnes, organisations, lieux
- **Questions-réponses** : extraire l'empan de réponse à partir du contexte
- **Traduction automatique** : séquence à séquence avec attention
- **Résumé** : extractif (sélection de phrases) ou abstractif (génération). Voir [[text-summarization]]
- **Génération de texte** : modèles autorégressifs de la famille GPT
- **Modélisation du langage** : prédire le token suivant à partir du contexte. Voir [[probabilistic-language-models]]

## Conseils pratiques {#practical-tips}

1. Commencer par des modèles pré-entraînés : presque toujours meilleurs qu'un entraînement from scratch
2. Taux d'apprentissage pour le fine-tuning de BERT : 2e-5 à 5e-5 (bien inférieur à un entraînement from scratch)
3. Longueur maximale de séquence : BERT = 512 tokens. Tronquer ou découper les textes plus longs
4. Le tokenizer doit correspondre au modèle (tokenizer BERT avec modèle BERT)
5. Pour les tâches simples avec peu de données : TF-IDF + régression logistique est étonnamment compétitif
6. Utiliser la bibliothèque HuggingFace Transformers pour une API unifiée

## Pièges courants {#gotchas}
- Un tokenizer incompatible échoue silencieusement (embeddings incorrects)
- La tokenisation en sous-mots signifie que le nombre de tokens différe du nombre de mots
- BERT n'a que l'encodeur (classification, NER), GPT n'a que le décodeur (génération)
- Le fine-tuning sur des jeux de données très petits (< 1000 échantillons) peut ne pas améliorer TF-IDF + ML classique
- Les modèles multilingues (mBERT, XLM-R) fonctionnent mais sont moins bons que les modèles spécifiques à une langue

## Voir aussi {#see-also}
- [[neural-networks]] - apprentissage profond général
- [[transfer-learning]] - pré-entraînement et fine-tuning
- [[feature-engineering]] - ingénierie de caractéristiques à partir de texte
- [[model-evaluation]] - métriques d'évaluation spécifiques au NLP
- [[text-summarization]] - résumé extractif et abstractif
- [[probabilistic-language-models]] - n-grammes, chaînes de Markov, déchiffrement de chiffres

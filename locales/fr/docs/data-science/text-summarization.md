---
title: "Résumé automatique de texte"
description: "Techniques de résumé extractif et abstractif utilisant le scoring TF-IDF et les modèles transformers"
level: 4
source_sha256: 08186e83314c09af32c4c1cec4fe7ef3e4f032392779d1b8919d6df03dd7f6b4
translation: machine
translated_at: '2026-10-24'
---
# Résumé automatique de texte {#text-summarization}

Génération automatique de versions condensées de documents. Deux approches fondamentales : l'extractif (sélectionner des phrases existantes) et l'abstractif (générer un nouveau texte). Les méthodes extractives ne nécessitent aucune donnée d'entraînement et fonctionnent à partir d'un seul document.

## Extractif vs abstractif {#extractive-vs-abstractive}

| Approche | Méthode | Avantages | Inconvénients |
|----------|---------|-----------|---------------|
| **Extractive** | Sélectionner les phrases du document les mieux scorées | Simple, aucune donnée d'entraînement, fidèle à la source | Limitée aux phrases existantes, peut manquer de cohérence |
| **Abstractive** | Générer un nouveau texte exprimant les idées principales | Plus naturelle, capable de paraphraser | Nécessite des modèles seq2seq/transformer, peut halluciner |

## Scoring des phrases par TF-IDF {#tf-idf-sentence-scoring}

La méthode extractive la plus simple : scorer les phrases selon l'importance de leurs mots.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import nltk

def summarize_tfidf(text, top_n=3):
    # Step 1: Split into sentences
    sentences = nltk.sent_tokenize(text)

    # Step 2: Build TF-IDF matrix (sentences = documents)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Step 3: Score each sentence = mean of non-zero TF-IDF values
    scores = []
    for i in range(tfidf_matrix.shape[0]):
        row = tfidf_matrix[i].toarray().flatten()
        non_zero = row[row > 0]
        score = non_zero.mean() if len(non_zero) > 0 else 0
        scores.append(score)

    # Step 4: Select top sentences (maintain original order)
    ranked_idx = np.argsort(scores)[-top_n:]
    ranked_idx = sorted(ranked_idx)  # preserve document order

    return ' '.join([sentences[i] for i in ranked_idx])
```

**Pourquoi la moyenne des valeurs non nulles et non la somme ?**
- La somme favorise les phrases longues (plus de termes = somme plus élevée)
- La moyenne normalise en fonction de la longueur de la phrase
- Valeurs non nulles uniquement : la matrice TF-IDF est très creuse. Inclure les zéros diluerait les scores significatifs avec des termes à valeur nulle (absents)

**Pourquoi pas la moyenne de tout le vecteur ?**
- Les phrases au vocabulaire riche obtiendraient un score faible (les nombreux zéros diluent la moyenne)
- On souhaite la phrase contenant en moyenne les mots les plus importants, et non le vocabulaire le plus diversifié

## TextRank (PageRank appliqué aux phrases) {#textrank-pagerank-for-sentences}

Traite les phrases comme des nœuds d'un graphe. Poids d'une arête = similarité entre phrases. Les phrases les mieux scorées sont celles qui ressemblent à de nombreuses autres phrases importantes.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk

def textrank_summarize(text, top_n=3, damping=0.85, iterations=50):
    sentences = nltk.sent_tokenize(text)
    n = len(sentences)

    # Build similarity matrix
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(sentences)
    sim_matrix = cosine_similarity(tfidf)

    # Normalize rows (transition probabilities)
    for i in range(n):
        row_sum = sim_matrix[i].sum()
        if row_sum > 0:
            sim_matrix[i] /= row_sum

    # Power iteration (PageRank)
    scores = np.ones(n) / n
    for _ in range(iterations):
        scores = (1 - damping) / n + damping * sim_matrix.T @ scores

    # Top sentences in original order
    top_idx = sorted(np.argsort(scores)[-top_n:])
    return ' '.join([sentences[i] for i in top_idx])
```

TextRank est basé sur le PageRank de Google : une phrase est importante si elle est similaire à de nombreuses autres phrases importantes (définition récursive résolue par calcul de vecteur propre / itération de puissance).

## Stratégies de sélection {#selection-strategies}

Après le scoring, plusieurs façons de choisir les phrases qui apparaîtront dans le résumé :

| Stratégie | Description | Cas d'usage |
|-----------|-------------|-------------|
| Top-N phrases | Prendre les N phrases les mieux scorées | Résumés de longueur fixe |
| Top-N mots/caractères | Prendre des phrases jusqu'à atteindre un budget de mots/caractères | Extraits de moteurs de recherche |
| Pourcentage | Top X % des phrases | Proportionnel à la longueur du document |
| Seuil | Phrases dont le score dépasse moyenne * facteur | Longueur variable, s'adapte au contenu |

## Bibliothèques {#libraries}

```python
# sumy: multiple algorithms
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

parser = PlaintextParser.from_string(text, Tokenizer("english"))
summarizer = TextRankSummarizer()
summary = summarizer(parser.document, sentences_count=3)

# gensim (older versions)
from gensim.summarization import summarize  # deprecated in gensim 4+
summary = summarize(text, word_count=100)
```

## Pièges à éviter {#gotchas}

- **Les résumés extractifs peuvent manquer de cohérence.** Les phrases sélectionnées peuvent faire référence à des entités introduites dans des phrases ignorées. Un post-traitement (résolution des pronoms) peut aider, mais ajoute de la complexité.
- **Le scoring TF-IDF nécessite un nombre suffisant de phrases.** En dessous de 5 à 6 phrases, la composante IDF devient instable. Pour des textes très courts, la longueur des phrases combinée au recouvrement de mots-clés donne de meilleurs résultats.
- **TextRank peut sélectionner des phrases redondantes.** Deux phrases très similaires peuvent toutes deux obtenir un score élevé. Appliquer MMR (Maximal Marginal Relevance) pour pénaliser la sélection de phrases trop proches de celles déjà retenues.

## Références croisées {#cross-references}

- [[nlp-text-processing]] - tokenisation, fondamentaux de TF-IDF
- [[attention-mechanisms]] - le résumé abstractif utilise l'attention
- [[rnn-sequences]] - modèles abstractifs seq2seq

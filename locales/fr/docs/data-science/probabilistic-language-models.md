---
title: "Modèles de langage probabilistes"
description: "Modèles n-grammes, techniques de lissage et évaluation par perplexité pour la génération de texte et les fondements du TAL"
level: 3
source_sha256: 6d700379aa37a3a7e90e9c100a55b7f513f602fd9ab1d3b2e70a005899808a16
translation: machine
translated_at: '2026-10-24'
---
# Modèles de langage probabilistes {#probabilistic-language-models}

Modèles statistiques qui attribuent des probabilités à des séquences de mots. Fondement de la génération de texte, de la correction orthographique, de la reconnaissance vocale et du décryptage de chiffrements. Comprendre les modèles n-grammes est un préalable pour apprécier pourquoi les transformers ont été transformateurs.

## Modèles n-grammes {#n-gram-models}

Un modèle de langage n-gramme estime la probabilité du mot suivant étant donnés les (n-1) mots précédents :

- **Unigramme** : P(w) - fréquence du mot, sans contexte
- **Bigramme** : P(w_i | w_{i-1}) - un mot de contexte
- **Trigramme** : P(w_i | w_{i-2}, w_{i-1}) - deux mots de contexte

```python
from collections import Counter, defaultdict

def build_bigram_model(corpus):
    """Build bigram probabilities from tokenized corpus."""
    bigram_counts = Counter()
    unigram_counts = Counter()

    for sentence in corpus:
        tokens = sentence.lower().split()
        for i in range(len(tokens)):
            unigram_counts[tokens[i]] += 1
            if i > 0:
                bigram_counts[(tokens[i-1], tokens[i])] += 1

    # P(w2 | w1) = count(w1, w2) / count(w1)
    model = defaultdict(dict)
    for (w1, w2), count in bigram_counts.items():
        model[w1][w2] = count / unigram_counts[w1]

    return model
```

## Probabilité d'une phrase {#sentence-probability}

La probabilité d'une phrase est le produit des probabilités conditionnelles :

```bash
P("the cat sat") = P(the) * P(cat|the) * P(sat|cat)
```

En pratique, on utilise les log-probabilités pour éviter le sous-dépassement de capacité (underflow) :

```python
import math

def sentence_log_prob(sentence, model):
    tokens = sentence.lower().split()
    log_prob = 0
    for i in range(1, len(tokens)):
        prev, curr = tokens[i-1], tokens[i]
        prob = model.get(prev, {}).get(curr, 1e-10)  # smoothing
        log_prob += math.log(prob)
    return log_prob
```

Plus la log-probabilité est élevée, plus la phrase a de chances d'être du véritable anglais. C'est l'idée centrale utilisée dans le décryptage de chiffrements et la détection de la reformulation automatique d'articles.

## Décryptage de chiffrements à l'aide de modèles de langage {#cipher-decryption-with-language-models}

Un chiffrement par substitution remplace chaque lettre par une autre. Pour le casser sans la clé :

1. Construire un modèle de langage de la langue cible (bigrammes ou trigrammes au niveau des caractères)
2. Utiliser un algorithme génétique/évolutionnaire pour faire évoluer des clés de déchiffrement candidates
3. Évaluer chaque candidat par la probabilité que le modèle de langage attribue au texte déchiffré
4. Sélectionner et muter les meilleurs candidats, puis recommencer

```python
import random
import string

def fitness(decrypted_text, language_model):
    """Score how 'English-like' the decrypted text is."""
    return sentence_log_prob(decrypted_text, language_model)

def mutate(key):
    """Swap two random letter mappings."""
    key = list(key)
    i, j = random.sample(range(26), 2)
    key[i], key[j] = key[j], key[i]
    return ''.join(key)

# Evolutionary loop
population = [random_key() for _ in range(pool_size)]
for epoch in range(num_epochs):
    scored = [(fitness(decrypt(cipher, k), lm), k) for k in population]
    scored.sort(reverse=True)
    parents = [k for _, k in scored[:top_n]]
    population = [mutate(random.choice(parents)) for _ in range(pool_size)]
```

L'algorithme génétique explore l'espace des clés (26! permutations) grâce à la mutation et à la sélection guidées par le score du modèle de langage.

## Reformulation automatique d'articles et détection {#article-spinning-and-detection}

La reformulation automatique d'articles remplace des mots par des synonymes afin de produire un contenu « unique ». La vérification du contexte fondée sur les trigrammes permet de repérer les mauvais remplacements :

| Original | Remplacement naïf | Problème |
|----------|-----------|---------|
| quantum **gate** | quantum **door** | « gate » = porte logique, et non porte physique |
| complex **Hilbert space** | complicated **Hilbert space** | « complex » = nombres complexes, et non difficulté |

Le simple remplacement de synonymes sans tenir compte du contexte échoue, car de nombreux mots ont des sens propres à un domaine. Les modèles sensibles au contexte (apprentissage profond) donnent de meilleurs résultats, mais même une vérification au niveau des trigrammes permet d'attraper les erreurs les plus grossières.

## Des modèles de Markov à PageRank {#markov-models-to-pagerank}

Les modèles de langage n-grammes sont des chaînes de Markov : l'état suivant ne dépend que des N-1 états précédents. Ce même principe sous-tend :

- **PageRank** : pages web comme états, liens comme transitions. Distribution stationnaire = importance des pages
- **TextRank** : phrases comme états, similarité comme probabilité de transition
- **Modèles de Markov cachés (HMM)** : pour la reconnaissance vocale, l'étiquetage morphosyntaxique (POS tagging) et l'analyse de séquences biologiques

## Contexte historique {#historical-context}

- Années 1900 : Andreï Markov applique les chaînes de Markov à la succession des voyelles et des consonnes dans le texte russe
- 1948 : Claude Shannon utilise les modèles de Markov pour la génération de texte dans son article fondateur sur la théorie de l'information
- Années 2000 : les HMM dominent la reconnaissance vocale jusqu'à l'avènement de l'apprentissage profond
- Aujourd'hui : les transformers ont remplacé les n-grammes pour la plupart des tâches de TAL, mais les modèles n-grammes restent utiles pour :
  - La prédiction de frappe au clavier (mobile)
  - La correction orthographique
  - La détection de la langue
  - Les environnements à faibles ressources

## Pièges à éviter {#gotchas}

- **Le lissage est indispensable.** Les n-grammes jamais observés reçoivent une probabilité nulle, ce qui rend nulle la probabilité de la phrase entière. Le lissage de Laplace (ajout de 1), Kneser-Ney ou le backoff sont les solutions standard.
- **Les modèles au niveau des caractères sont meilleurs pour le décryptage de chiffrements** que les modèles au niveau des mots. Les modèles au niveau des mots ont une couverture clairsemée ; les modèles bigrammes/trigrammes de caractères capturent la structure de la langue de manière plus robuste pour cette tâche.
- **La reformulation automatique d'articles EST détectable.** Même une simple analyse bigramme signale les combinaisons de mots peu naturelles. Les outils de détection du plagiat plus sophistiqués combinent similarité documentaire et analyse de perplexité.

## Renvois {#cross-references}

- [[nlp-text-processing]] - tokenisation, TF-IDF, prétraitement du texte
- [[text-summarization]] - TextRank utilise un score de type chaîne de Markov
- [[bayesian-methods]] - fondements probabilistes
- [[monte-carlo-simulation]] - échantillonnage à partir de distributions de probabilité

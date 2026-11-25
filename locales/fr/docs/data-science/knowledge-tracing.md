---
title: "Suivi des connaissances (Knowledge Tracing)"
category: techniques
tags: [knowledge-tracing, learner-modeling, adaptive-learning, spaced-repetition, education-ai, knowledge-graph]
level: 3
source_sha256: 7173517e48300e2d723245cfbc274add01abc5ea13db25097f15855843d29ec0
translation: machine
translated_at: '2026-10-24'
---
# Knowledge Tracing {#knowledge-tracing}

Le Knowledge Tracing (KT) modélise la probabilité qu'un apprenant réponde correctement à une question, à partir de son historique d'interactions. Il constitue un composant central des systèmes d'apprentissage adaptatif, qui décident quoi enseigner ensuite et quand réviser.

## Points clés {#key-facts}

- Les modèles KT prennent en entrée des séquences de paires (question, correct/incorrect) et prédisent P(correct) pour la question suivante
- Évolution : BKT (1995) -> DKT (2015) -> SAKT (2019) -> AKT (2020) -> simpleKT (2023) -> modèles de pointe (2025)
- simpleKT (ICLR 2023) est une baseline transformer simplifiée qui surpasse la plupart des modèles complexes, difficile à dépasser
- pyKT est la bibliothèque de référence : plus de 10 modèles, plus de 7 jeux de données, maintenue activement
- FSRS-7 est l'ordonnanceur de répétition espacée à l'état de l'art, intégré à Anki 23.10+, avec des implémentations en JS/Go/Rust/Python
- L'architecture d'apprentissage adaptatif en 4 couches (modèle du domaine, modèle de l'apprenant, modèle de tutorat, interface) constitue le cadre de référence

## Évolution des modèles {#model-evolution}

### BKT (Bayesian Knowledge Tracing) {#bkt-bayesian-knowledge-tracing}

Modèle de Markov caché avec un état de maîtrise binaire par compétence. Quatre paramètres par compétence : P(init), P(learn), P(guess), P(slip).

```text
State: UNLEARNED -> LEARNED (transition with P(learn))

Observation model:
  If LEARNED:   P(correct) = 1 - P(slip)
  If UNLEARNED: P(correct) = P(guess)

After each observation, update P(LEARNED) via Bayes' rule.
Mastery threshold: typically P(LEARNED) > 0.95
```

Limites : maîtrise binaire (pas de connaissance partielle), compétences indépendantes (pas de transfert), absence d'oubli.

### DKT (Deep Knowledge Tracing, 2015) {#dkt-deep-knowledge-tracing-2015}

RNN/LSTM appliqué à la séquence complète des interactions. Apprend implicitement un état de connaissance latent.

```python
# DKT input encoding
# Each timestep: one-hot of (question_id, correctness)
# For Q questions: input_dim = 2 * Q
# x_t = one_hot(q_t + Q * a_t) where a_t in {0, 1}

import torch.nn as nn

class DKT(nn.Module):
    def __init__(self, n_questions, hidden_dim=100):
        super().__init__()
        self.input_dim = 2 * n_questions
        self.rnn = nn.LSTM(self.input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, n_questions)

    def forward(self, x):
        # x: (batch, seq_len, 2*n_questions)
        h, _ = self.rnn(x)
        # h: (batch, seq_len, hidden_dim)
        return torch.sigmoid(self.fc(h))
        # output: (batch, seq_len, n_questions) = P(correct) per question
```

Amélioration par rapport au BKT : capture les dépendances complexes entre compétences, les connaissances partielles et les motifs temporels. En revanche, il fonctionne comme une boîte noire, sans état de connaissance interprétable.

### SAKT (Self-Attentive KT, 2019) {#sakt-self-attentive-kt-2019}

Remplace le RNN par une auto-attention. Le modèle porte son attention sélectivement sur les interactions passées pertinentes, au lieu de compresser tout l'historique dans un état caché.

```text
Key idea:
  Query: current question embedding
  Keys/Values: past interaction embeddings (question + response)
  
  Attention scores = which past interactions are relevant
  to predicting the current question
  
  Advantage: handles long sequences better than LSTM
  (no vanishing gradient over hundreds of interactions)
```

### AKT (Attentive KT, 2020) {#akt-attentive-kt-2020}

Ajoute une attention contextuelle et une décroissance exponentielle pour modéliser l'oubli. Prend explicitement en compte la similarité entre questions.

```text
Innovations over SAKT:
  1. Monotonic attention - context-aware, distinguishes 
     "mastered then forgot" from "never learned"
  2. Rasch model integration - question difficulty as explicit parameter
  3. Exponential forgetting factor - recent interactions weighted higher
  4. Question similarity - attention weighted by how similar 
     past questions are to the current one
```

### simpleKT (ICLR 2023) {#simplekt-iclr-2023}

Baseline transformer simplifiée, avec une difficulté propre à chaque question inspirée du modèle de Rasch. Difficile à battre malgré sa simplicité.

```text
Architecture:
  1. Question embedding + difficulty parameter (Rasch-like)
  2. Interaction embedding = question_emb + correctness_emb
  3. Standard transformer encoder over interaction sequence
  4. Linear prediction head -> P(correct)

Why it wins: proper question difficulty modeling + clean architecture
eliminates noise that complex models add. 
Essential baseline for any KT research.
```

### Modèles de pointe 2025 {#2025-frontier-models}

| Modèle | Innovation | Architecture |
|--------|-----------|-------------|
| DKT2 | xLSTM + sortie IRT | KT profond interprétable |
| HCGKT | Graphe hiérarchique + apprentissage contrastif | Convolutions sur graphes |
| LefoKT | Découple l'oubli de la pertinence | Attention à oubli relatif |
| UKT | Connaissance représentée par des distributions de probabilité | Attention de Wasserstein |
| ReKT | État de connaissance 3D (thème/point/domaine) | FRU : Forget-Response-Update |
| DyGKT | Graphes de prérequis dynamiques | GNN pour la structure de prérequis |

## Architecture d'apprentissage adaptatif {#adaptive-learning-architecture}

Architecture standard en 4 couches pour la construction de systèmes éducatifs adaptatifs :

```text
Layer 1: Domain Model
  Knowledge graph / concept map / prerequisite structure
  Nodes: concepts/skills
  Edges: prerequisites, similarity, co-occurrence
  
Layer 2: Student Model
  Per-learner state: proficiency per concept, learning style,
  cognitive load, forgetting curve, behavioral patterns
  Updated after every interaction via KT model
  
Layer 3: Tutoring Model
  Pedagogical decisions: what next? how to present? when to review?
  Inputs: student model state + domain model structure
  Uses: FSRS for review scheduling, i+1 for difficulty selection
  
Layer 4: Interface Layer
  Interaction design, exercise rendering, feedback presentation
```

## Répétition espacée avec FSRS-7 {#spaced-repetition-with-fsrs-7}

FSRS (Free Spaced Repetition Scheduler) est l'algorithme de référence pour planifier les révisions. Il se fonde sur la probabilité d'oubli prédite, plutôt que sur des intervalles fixes.

```text
FSRS-7 key properties:
  - Predicts P(recall) at any point in time
  - Supports fractional interval lengths
  - 4 core parameters per item: difficulty, stability, 
    elapsed days, scheduled days
  - Backed by academic research, integrated into Anki 23.10+
  
Implementations: JS, Go, Rust, Python
Benchmark: github.com/open-spaced-repetition/srs-benchmark
```

## Compression du contexte de l'apprenant {#student-context-compression}

Encodage efficace de l'état de l'apprenant pour les systèmes de tutorat basés sur des LLM :

```text
Tier 1 - Always in context (~200-500 tokens):
  Proficiency vector (concept -> score, last 10-20 concepts)
  Active lesson context
  Last 3-5 interaction summaries
  Active misconceptions

Tier 2 - Summarized (~500-1000 tokens):
  Session summaries (last 5 sessions)
  Error pattern clusters
  Learning pace indicators

Tier 3 - Retrieved on demand (RAG):
  Full interaction history
  Detailed error logs
  Historical proficiency curves

Placement in LLM context ("Lost in the Middle" mitigation):
  START: student proficiency data (critical)
  MIDDLE: background summaries (least critical)
  END: recent interactions (high attention)
```

## Bibliothèque pyKT {#pykt-library}

La bibliothèque Python de référence pour la recherche et le déploiement en Knowledge Tracing.

```python
# pyKT: 3-step model training
# Step 1: Prepare dataset
# Supports: ASSISTments, EdNet, Junyi, Statics, NIPS34, etc.

# Step 2: Train model
# python train.py --dataset_name assist2015 --model_name simpleKT \
#   --emb_size 64 --learning_rate 0.001 --seed 42

# Step 3: Evaluate
# Metrics: AUC, accuracy, RMSE
# Cross-validation with temporal split (no future leakage)
```

Modèles disponibles : DKT, DKVMN, SAKT, AKT, simpleKT, CL4KT, LPKT, HawkesKT, et d'autres.

## Plateformes open source {#open-source-platforms}

- **adaptive-knowledge-graph** : graphes de connaissances + LLM locaux + suivi bayésien des compétences, RAG respectueux de la vie privée avec recherche augmentée par le graphe, modélisation de la maîtrise par IRT/BKT
- **OATutor** : React + Firebase, BKT pour la maîtrise des compétences, testé en conditions réelles en classe
- **pyKT** : bibliothèque KT de référence, plus de 10 modèles, plus de 7 jeux de données standardisés

## Pièges à éviter {#gotchas}

- **simpleKT est étonnamment difficile à battre** : de nombreux articles revendiquent des gains par rapport à DKT/SAKT, mais ne surpassent plus simpleKT lorsqu'il est correctement réglé. Incluez-le systématiquement comme baseline. Le paramètre de difficulté inspiré de Rasch porte l'essentiel de la performance
- **Fuite de données temporelles dans l'évaluation** : les découpages train/test aléatoires laissent fuiter de l'information future (les interactions d'une session ultérieure se retrouvent dans l'entraînement). Utilisez toujours des découpages temporels : entraînement sur les interactions antérieures à T, test sur celles postérieures à T
- **La qualité du graphe de connaissances conditionne tout** : le modèle du domaine (structure de prérequis) est généralement rédigé à la main, ce qui coûte cher. Les erreurs de prérequis se propagent dans le modèle de tutorat. La construction automatique de graphes de connaissances à partir des données d'exercices est un sujet de recherche actif, mais pas encore fiable
- **L'oubli est asymétrique** : les compétences acquises par un rappel effortful s'oublient plus lentement que celles acquises par relecture ou par indices. Les modèles KT qui traitent toutes les bonnes réponses de la même manière passent à côté de ce phénomène. AKT et LefoKT le prennent partiellement en compte

## Voir aussi {#see-also}

- [[bayesian-methods]] : fondement des modèles BKT et IRT
- [[rnn-sequences]] : architecture LSTM utilisée dans DKT
- [[attention-mechanisms]] : auto-attention utilisée dans SAKT, AKT, simpleKT
- [[graph-neural-networks]] : GNN utilisés dans DyGKT et HCGKT
- [[recommender-systems]] : les idées de filtrage collaboratif s'appliquent à la recommandation d'exercices

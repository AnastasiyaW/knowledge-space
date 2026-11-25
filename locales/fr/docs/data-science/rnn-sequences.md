---
title: "RNN et modèles de séquences"
category: models
tags: [data-science, deep-learning, rnn, lstm, gru, time-series]
level: 3
source_sha256: 9def0a42ebabec3afbd88898976ba52f0c485c56c8b9fa9c67a2399177a7ec9a
translation: machine
translated_at: '2026-10-24'
---
# RNN et modèles de séquences {#rnns-and-sequence-models}

Les réseaux de neurones récurrents (RNN) traitent des données séquentielles en maintenant un état caché à travers les pas de temps. Bien qu'ils aient été largement supplantés par les transformers pour le TAL, ils restent pertinents pour les séries temporelles et les applications de streaming.

## RNN simple {#simple-rnn}

Traite un élément à la fois : h_t = tanh(W_hh * h_(t-1) + W_xh * x_t + b)

**Défaut fatal** : disparition du gradient. Pour des séquences de plus de ~20 tokens, les gradients diminuent exponentiellement lors de la rétropropagation à travers le temps (BPTT). Le réseau ne peut pas apprendre les dépendances à longue portée.

### Pourquoi la disparition du gradient se produit {#why-vanishing-gradients-happen}

La prédiction de sortie y_hat(T) est une fonction composée de toutes les entrées x_1...x_T. La matrice de poids W_xh intervient, multipliée par chaque entrée à chaque pas de temps. Lors du calcul du gradient de W_xh par la règle de la chaîne, on obtient un produit de nombreuses dérivées. Si les valeurs propres de W_hh sont inférieures à 1, le produit diminue exponentiellement (disparition). Si elles sont supérieures à 1, il explose (explosion du gradient). Cela signifie que l'influence des premières entrées sur la sortie finale devient négligeable : le réseau « oublie » les premiers tokens.

**Les explosions de gradient** se maîtrisent par écrêtage du gradient (gradient clipping). **La disparition du gradient** est le problème le plus difficile : c'est précisément ce que les LSTM et les GRU ont été conçus pour résoudre.

## LSTM (Long Short-Term Memory) {#lstm-long-short-term-memory}

Résout la disparition du gradient grâce à un état de cellule qui utilise des mises à jour **additives** (et non multiplicatives), ce qui permet aux gradients de circuler à travers le temps sans disparaître :

- **Porte d'oubli** : ce qu'il faut supprimer de l'état de cellule. f_t = sigma(W_f * [h_(t-1), x_t] + b_f)
- **Porte d'entrée** : ce qu'il faut stocker comme nouvelle information. i_t = sigma(W_i * [h_(t-1), x_t] + b_i)
- **Porte de sortie** : ce qu'il faut produire en sortie. o_t = sigma(W_o * [h_(t-1), x_t] + b_o)
- **État de cellule** : chemin de mémoire à long terme avec mises à jour additives (les gradients circulent librement)

Gère efficacement des séquences d'environ 200 à 500 tokens.

```python
import torch.nn as nn

lstm = nn.LSTM(
    input_size=300,      # input feature dimension
    hidden_size=128,     # hidden state dimension
    num_layers=2,        # stacked LSTM layers
    bidirectional=True,  # process forward AND backward
    batch_first=True,    # input shape: (batch, seq, features)
    dropout=0.2          # between layers
)
```

## GRU (Gated Recurrent Unit) {#gru-gated-recurrent-unit}

Version simplifiée du LSTM avec deux portes au lieu de trois :
- **Porte de mise à jour** : combine les portes d'oubli et d'entrée
- **Porte de réinitialisation** : contrôle la quantité de passé à ignorer

Performances similaires à celles du LSTM, moins de paramètres, légèrement plus rapide.

```python
gru = nn.GRU(input_size=300, hidden_size=128, num_layers=2,
             bidirectional=True, batch_first=True)
```

## Bidirectionnel {#bidirectional}

Traite la séquence dans les deux sens (avant ET arrière), puis concatène les états cachés. Capture à la fois le contexte gauche et le contexte droit.

La dimension de sortie double : hidden_size * 2 pour un modèle bidirectionnel.

**À utiliser pour** : la classification, l'étiquetage, tout cas où la séquence complète est disponible.
**À éviter pour** : la génération (impossible de consulter les tokens futurs pendant la génération).

## Séries temporelles avec les RNN {#time-series-with-rnns}

### Schéma de prévision {#forecasting-pattern}
```python
class TimeSeriesLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=1):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])  # use last time step
```

### Modèles AR (AutoRegressive) {#ar-autoregressive-models}
y_t = phi_1 * y_(t-1) + phi_2 * y_(t-2) + ... + phi_p * y_(t-p)

Les caractéristiques sont extraites automatiquement à partir des retards : aucune ingénierie manuelle des variables cibles n'est nécessaire.

## Catégories de données séquentielles {#sequence-data-categories}

Les différentes tâches sur séquences ont des formes d'entrées/sorties différentes :

| Catégorie | Entrée | Sortie | Exemples |
|----------|-------|--------|----------|
| Plusieurs-vers-un | Séquence | Valeur unique | Analyse de sentiment, reconnaissance d'activité |
| Un-vers-plusieurs | Valeur unique | Séquence | Génération musicale, légendage d'images |
| Plusieurs-vers-plusieurs (égales) | Séquence | Séquence de même longueur | NER, étiquetage morphosyntaxique (POS) |
| Plusieurs-vers-plusieurs (inégales) | Séquence | Séquence de longueur différente | Traduction, résumé automatique |

Note : le cas « un-vers-plusieurs » peut avoir une entrée vide ou nulle (par ex. génération musicale inconditionnelle) ou une valeur d'amorçage (identifiant de genre, premières notes).

## Séquence à séquence {#sequence-to-sequence}

L'encodeur traite la séquence d'entrée → vecteur de contexte → le décodeur génère la séquence de sortie.

**Applications** : traduction automatique, résumé automatique, chatbots.

**Mécanisme d'attention** : le décodeur porte son attention sur tous les états cachés de l'encodeur, et non seulement sur le dernier. Il résout le goulot d'étranglement informationnel du vecteur de contexte de taille fixe.

## Entraînement des RNN : batchs et longueur de séquence {#training-rnns-batching-and-sequence-length}

### Génération des batchs d'entraînement {#generating-training-batches}

Pour les modèles de langage au niveau caractère ou mot, le texte complet doit être découpé en paires entrée/cible qui se chevauchent :

```python
def generate_batches(encoded_text, seq_length, batch_size):
    """Slice encoded text into (input, target) pairs for RNN training."""
    total_chars = len(encoded_text)
    chars_per_batch = total_chars // batch_size

    for i in range(0, chars_per_batch - seq_length, seq_length):
        x = encoded_text[i:i + seq_length]       # input sequence
        y = encoded_text[i + 1:i + seq_length + 1]  # target = shifted by 1
        yield x, y
```

**Paramètres clés à régler** :

- **Longueur de séquence** : minimum ~100 caractères/tokens. Plus long = plus de contexte, mais entraînement plus lent et plus de mémoire
- **Taille de batch** : typiquement 64 à 128. Des batchs plus grands = gradients plus stables, mais risque de converger vers des minima plus pointus
- **Époques** : dépend de la taille du jeu de données et de la capacité du modèle. Surveiller la perte et arrêter lorsque la perte de validation stagne

### Boucle d'entraînement (PyTorch) {#training-loop-pattern-pytorch}

```python
model.train()
if model.use_gpu:
    model.cuda()

for epoch in range(n_epochs):
    hidden = model.init_hidden(batch_size)
    for x_batch, y_batch in generate_batches(data, seq_len, batch_size):
        hidden = tuple(h.detach() for h in hidden)  # detach to prevent BPTT through entire history
        model.zero_grad()
        output, hidden = model(x_batch, hidden)
        loss = criterion(output, y_batch.view(-1))
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5)
        optimizer.step()
```

**Critique** : `hidden.detach()` à chaque frontière de batch empêche la rétropropagation sur l'historique complet de la séquence (ce qui serait prohibitif en mémoire). C'est la BPTT tronquée.

## Pièges {#gotchas}
- Les RNN sont séquentiels par nature : impossible de paralléliser sur les pas de temps (entraînement lent)
- LSTM et GRU aident, mais ne résolvent pas complètement les dépendances à longue portée pour des séquences très longues
- Pour la plupart des tâches de TAL, les transformers surpassent nettement les RNN
- L'écrêtage du gradient est souvent nécessaire : `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`
- Les séquences de longueur variable nécessitent du padding et du masquage
- **Détachement de l'état caché** : oublier de détacher l'état caché entre les batchs provoque une erreur OOM, car le graphe de calcul croît sans limite
- **Longueur de séquence vs mémoire** : doubler la longueur de séquence double à peu près l'utilisation mémoire et le temps d'entraînement par batch

## Voir aussi {#see-also}
- [[nlp-text-processing]] - les transformers ont largement remplacé les RNN pour le TAL
- [[neural-networks]] - fondements généraux de l'apprentissage profond
- [[time-series-analysis]] - méthodes statistiques pour les séries temporelles

---
title: "Réseaux de neurones et apprentissage profond"
category: models
tags: [data-science, deep-learning, neural-networks, pytorch, keras]
level: 3
source_sha256: e35ab490e6f2c2f8a8752360f2943215accebb3a34f5fec2e66fd3706363d2fb
translation: machine
translated_at: '2026-10-24'
---
# Réseaux de neurones et apprentissage profond {#neural-networks-and-deep-learning}

L'apprentissage profond apprend automatiquement les caractéristiques à partir des données brutes. Il excelle pour les images, le texte, l'audio et les séquences, lorsque l'ingénierie manuelle des caractéristiques est impraticable.

## Briques de base {#building-blocks}

### Couche dense (entièrement connectée) {#dense-fully-connected-layer}
Chaque entrée est connectée à chaque sortie : y = Wx + b

### Fonctions d'activation {#activation-functions}

| Fonction | Formule | Plage | Cas d'usage |
|----------|---------|-------|-------------|
| ReLU | max(0, x) | [0, inf) | Valeur par défaut pour les couches cachées |
| LeakyReLU | max(0.01x, x) | (-inf, inf) | Corrige le problème des neurones morts |
| Sigmoid | 1/(1+e^(-x)) | (0, 1) | Sortie pour la classification binaire |
| Tanh | (e^x-e^(-x))/(e^x+e^(-x)) | (-1, 1) | Alternative centrée sur zéro |
| Softmax | e^(x_i) / sum(e^(x_j)) | (0, 1), sum=1 | Sortie pour la classification multiclasse |

Sans fonctions d'activation, empiler des couches linéaires revient à une seule couche linéaire.

## Entraînement {#training}

### Fonctions de perte {#loss-functions}
- **Binary Cross-Entropy** : L = -[y*log(p) + (1-y)*log(1-p)]
- **Categorical Cross-Entropy** : L = -sum(y_i * log(p_i))
- **MSE** : pour la régression

### Boucle d'entraînement (PyTorch) {#training-loop-pytorch}
```python
for epoch in range(num_epochs):
    for batch_x, batch_y in dataloader:
        predictions = model(batch_x)       # forward pass
        loss = criterion(predictions, batch_y)
        optimizer.zero_grad()               # clear gradients
        loss.backward()                     # backpropagation
        optimizer.step()                    # update weights
```

### Optimiseurs {#optimizers}
- **SGD** : w -= lr * gradient. Simple, performant avec le momentum
- **Adam** : taux d'apprentissage adaptatif par paramètre. Choix par défaut pour la plupart des tâches
- **Taux d'apprentissage** : l'hyperparamètre le plus important. Essayer 1e-3, 3e-4, 1e-4

## Régularisation {#regularization}

- **Dropout** : mettre aléatoirement à zéro une fraction des neurones pendant l'entraînement (typiquement : 0,2 à 0,5)
- **Batch Normalization** : normaliser les entrées de chaque couche au sein du mini-lot. Permet d'utiliser des taux d'apprentissage plus élevés
- **Early Stopping** : surveiller la perte de validation et arrêter lorsqu'elle augmente
- **Augmentation de données** : transformations aléatoires (retournement, rotation, recadrage pour les images)
- **Weight Decay** : régularisation L2 sous forme de paramètre de l'optimiseur

## Exemple PyTorch {#pytorch-example}

```python
import torch
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = SimpleNet()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```

## Exemple Keras/TensorFlow {#kerastensorflow-example}

```python
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)
```

## Hyperparamètres {#hyperparameters}

| Paramètre | Plage typique | Remarques |
|-----------|--------------|-----------|
| Taux d'apprentissage | 1e-4 à 1e-2 | Le plus important : à régler en premier |
| Taille de lot | 32, 64, 128, 256 | Plus grand = plus rapide, plus petit = meilleure généralisation |
| Couches/unités | Dépend de la tâche | Commencer petit, augmenter en cas de sous-apprentissage |
| Taux de dropout | 0,1 à 0,5 | Plus élevé pour les grands modèles |
| Initialisation des poids | He (ReLU), Xavier (tanh/sigmoid) | Généralement gérée par le framework |
| Époques | Utiliser l'early stopping | Ne pas fixer un nombre |

## ANN pour la prévision de séries temporelles {#anns-for-time-series-forecasting}

Les réseaux à propagation avant peuvent prédire des séries temporelles en utilisant des caractéristiques de retards glissants comme entrées.

### Modèle : ANN autorégressif {#pattern-autoregressive-ann}

```python
import numpy as np
from tensorflow import keras

# Create supervised dataset from time series
def create_dataset(series, window_size):
    X, y = [], []
    for i in range(len(series) - window_size):
        X.append(series[i:i + window_size])
        y.append(series[i + window_size])
    return np.array(X), np.array(y)

X_train, y_train = create_dataset(train_series, window_size=20)

model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(20,)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1)
])
model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)
```

### Rendements boursiers ou cours boursiers {#stock-returns-vs-stock-prices}

**Point clé** : utiliser les rendements (ou les rendements logarithmiques), et non les cours bruts. Les ANN ne peuvent pas extrapoler au-delà de la plage d'entraînement : si les cours étaient compris entre 100 et 200 pendant l'entraînement, le réseau ne peut pas prédire 250. Les rendements sont stationnaires et bornés, ce qui en fait des cibles adaptées pour les ANN.

```python
# Log returns: better for neural networks
returns = np.log(prices / prices.shift(1)).dropna()

# Predict returns, then convert back to prices
predicted_return = model.predict(X_test)
predicted_price = last_price * np.exp(predicted_return)
```

### Réseaux à entrées multiples {#multi-input-networks}

Combiner des séries temporelles avec des caractéristiques tabulaires (par exemple, données de capteurs + statistiques descriptives pour la reconnaissance d'activité humaine, HAR) :

```python
# Functional API for multiple inputs
ts_input = keras.Input(shape=(128, 9), name='timeseries')
flat = keras.layers.Flatten()(ts_input)
x = keras.layers.Dense(64, activation='relu')(flat)

tab_input = keras.Input(shape=(num_features,), name='tabular')
y = keras.layers.Dense(32, activation='relu')(tab_input)

combined = keras.layers.Concatenate()([x, y])
output = keras.layers.Dense(6, activation='softmax')(combined)

model = keras.Model(inputs=[ts_input, tab_input], outputs=output)
```

## Pièges à éviter {#gotchas}
- **Disparition du gradient** : réseaux profonds avec sigmoid/tanh. Remède : utiliser ReLU, des connexions résiduelles, BatchNorm
- **Explosion du gradient** : le clipping de gradient aide. Fréquent dans les RNN
- **Neurones ReLU morts** : entrées négatives -> gradient nul à jamais. Remède : LeakyReLU
- Les réseaux de neurones nécessitent BEAUCOUP plus de données que les modèles à base d'arbres pour les données tabulaires
- Toujours normaliser les entrées (StandardScaler ou équivalent)
- Un GPU est pratiquement indispensable pour les modèles non triviaux
- **Fenêtrage des séries temporelles** : la taille de la fenêtre est un hyperparamètre critique. Trop petite = contexte insuffisant, trop grande = bruit. Commencer par une longueur de cycle propre au domaine
- **Les cours boursiers ne sont PAS des cibles adaptées pour les ANN** : utiliser les rendements à la place (limite d'extrapolation)
- **Les modèles à entrées multiples nécessitent l'API fonctionnelle** : `Sequential` ne supporte qu'une seule entrée et une seule sortie

## Voir aussi {#see-also}
- [[cnn-computer-vision]] - réseaux convolutifs pour les images et les séries temporelles
- [[rnn-sequences]] - réseaux récurrents pour les séquences
- [[time-series-analysis]] - modèles classiques de séries temporelles
- [[nlp-text-processing]] - NLP avec les transformers
- [[math-for-ml]] - calcul différentiel pour la rétropropagation
- [[transfer-learning]] - utilisation de modèles pré-entraînés

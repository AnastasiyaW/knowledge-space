---
title: "Neuronale Netze und Deep Learning"
category: models
tags: [data-science, deep-learning, neural-networks, pytorch, keras]
level: 3
source_sha256: e35ab490e6f2c2f8a8752360f2943215accebb3a34f5fec2e66fd3706363d2fb
translation: machine
translated_at: '2026-10-24'
---
# Neuronale Netze und Deep Learning {#neural-networks-and-deep-learning}

Deep Learning lernt Merkmale automatisch aus Rohdaten. Es eignet sich hervorragend für Bilder, Text, Audio und Sequenzen, bei denen manuelles Feature Engineering nicht praktikabel ist.

## Bausteine {#building-blocks}

### Dense-Schicht (vollständig verbunden) {#dense-fully-connected-layer}
Jede Eingabe ist mit jeder Ausgabe verbunden: y = Wx + b

### Aktivierungsfunktionen {#activation-functions}

| Funktion | Formel | Wertebereich | Anwendungsfall |
|----------|--------|--------------|----------------|
| ReLU | max(0, x) | [0, inf) | Standard für versteckte Schichten |
| LeakyReLU | max(0.01x, x) | (-inf, inf) | Behebt das Problem toter Neuronen |
| Sigmoid | 1/(1+e^(-x)) | (0, 1) | Ausgabe für binäre Klassifikation |
| Tanh | (e^x-e^(-x))/(e^x+e^(-x)) | (-1, 1) | Zentrierte Alternative zu Sigmoid |
| Softmax | e^(x_i) / sum(e^(x_j)) | (0, 1), sum=1 | Ausgabe für Mehrklassen-Klassifikation |

Ohne Aktivierungsfunktionen ergibt das Stapeln linearer Schichten wieder genau eine lineare Schicht.

## Training {#training}

### Verlustfunktionen {#loss-functions}
- **Binary Cross-Entropy**: L = -[y*log(p) + (1-y)*log(1-p)]
- **Categorical Cross-Entropy**: L = -sum(y_i * log(p_i))
- **MSE**: für Regression

### Trainingsschleife (PyTorch) {#training-loop-pytorch}
```python
for epoch in range(num_epochs):
    for batch_x, batch_y in dataloader:
        predictions = model(batch_x)       # forward pass
        loss = criterion(predictions, batch_y)
        optimizer.zero_grad()               # clear gradients
        loss.backward()                     # backpropagation
        optimizer.step()                    # update weights
```

### Optimierer {#optimizers}
- **SGD**: w -= lr * gradient. Einfach, gut mit Momentum
- **Adam**: adaptive Lernraten pro Parameter. Standardwahl für die meisten Aufgaben
- **Lernrate**: wichtigster Hyperparameter. Probieren Sie 1e-3, 3e-4, 1e-4

## Regularisierung {#regularization}

- **Dropout**: Während des Trainings wird zufällig ein Anteil der Neuronen auf null gesetzt (typisch: 0,2–0,5)
- **Batch Normalization**: normalisiert die Eingaben einer Schicht innerhalb des Mini-Batches. Ermöglicht höhere Lernraten
- **Early Stopping**: Validierungsverlust überwachen und das Training beenden, sobald er wieder steigt
- **Data Augmentation**: zufällige Transformationen (Spiegeln, Rotieren, Zuschneiden bei Bildern)
- **Weight Decay**: L2-Regularisierung als Optimiererparameter

## PyTorch-Beispiel {#pytorch-example}

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

## Keras/TensorFlow-Beispiel {#kerastensorflow-example}

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

## Hyperparameter {#hyperparameters}

| Parameter | Typischer Bereich | Hinweise |
|-----------|-------------------|----------|
| Lernrate | 1e-4 bis 1e-2 | Am wichtigsten – zuerst abstimmen |
| Batch-Größe | 32, 64, 128, 256 | Größer = schneller, kleiner = bessere Generalisierung |
| Schichten/Einheiten | Aufgabenabhängig | Klein anfangen, erhöhen bei Underfitting |
| Dropout-Rate | 0,1–0,5 | Höher bei größeren Modellen |
| Gewichtsinitialisierung | He (ReLU), Xavier (tanh/sigmoid) | Wird meist vom Framework übernommen |
| Epochen | Early Stopping verwenden | Keine feste Zahl vorgeben |

## ANNs für Zeitreihenprognosen {#anns-for-time-series-forecasting}

Feedforward-Netze können Zeitreihen vorhersagen, indem sie gefensterte Lag-Merkmale als Eingabe verwenden.

### Muster: autoregressives ANN {#pattern-autoregressive-ann}

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

### Aktienrenditen vs. Aktienkurse {#stock-returns-vs-stock-prices}

**Zentrale Erkenntnis**: Verwenden Sie Renditen (oder logarithmische Renditen), nicht die Rohkurse. ANNs können nicht über den Trainingsbereich hinaus extrapolieren – lagen die Kurse im Training zwischen 100 und 200, kann das Netz 250 nicht vorhersagen. Renditen sind stationär und beschränkt und eignen sich daher als Zielgrößen für ANNs.

```python
# Log returns: better for neural networks
returns = np.log(prices / prices.shift(1)).dropna()

# Predict returns, then convert back to prices
predicted_return = model.predict(X_test)
predicted_price = last_price * np.exp(predicted_return)
```

### Netze mit mehreren Eingaben {#multi-input-networks}

Zeitreihen lassen sich mit tabellarischen Merkmalen kombinieren (z. B. Sensordaten + statistische Kennzahlen für HAR):

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

## Stolpersteine {#gotchas}
- **Verschwindende Gradienten**: tiefe Netze mit Sigmoid/Tanh. Abhilfe: ReLU, Skip-Verbindungen, BatchNorm verwenden
- **Explodierende Gradienten**: Gradient Clipping hilft. Häufig bei RNNs
- **Tote ReLU-Neuronen**: Negative Eingaben ergeben dauerhaft den Gradienten null. Abhilfe: LeakyReLU
- Neuronale Netze benötigen für tabellarische Daten DEUTLICH mehr Daten als baumbasierte Modelle
- Eingaben immer normalisieren (StandardScaler o. ä.)
- Für nicht-triviale Modelle ist eine GPU praktisch zwingend erforderlich
- **Fensterung bei Zeitreihen**: Die Fenstergröße ist ein kritischer Hyperparameter. Zu klein = unzureichender Kontext, zu groß = Rauschen. Mit einer domänenspezifischen Zykluslänge beginnen
- **Aktienkurse sind NICHT geeignet als ANN-Zielgrößen** – stattdessen Renditen verwenden (Extrapolationsgrenze)
- **Modelle mit mehreren Eingaben erfordern die funktionale API** – `Sequential` unterstützt nur eine Ein- und Ausgabe

## Siehe auch {#see-also}
- [[cnn-computer-vision]] - Faltungsnetze für Bilder und Zeitreihen
- [[rnn-sequences]] - rekurrente Netze für Sequenzen
- [[time-series-analysis]] - klassische Zeitreihenmodelle
- [[nlp-text-processing]] - NLP mit Transformern
- [[math-for-ml]] - Analysis für Backpropagation
- [[transfer-learning]] - Verwendung vortrainierter Modelle

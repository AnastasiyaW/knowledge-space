---
title: "RNNs und Sequenzmodelle"
category: models
tags: [data-science, deep-learning, rnn, lstm, gru, time-series]
level: 3
source_sha256: 9def0a42ebabec3afbd88898976ba52f0c485c56c8b9fa9c67a2399177a7ec9a
translation: machine
translated_at: '2026-10-24'
---
# RNNs und Sequenzmodelle {#rnns-and-sequence-models}

Rekurrente neuronale Netze (RNNs) verarbeiten sequentielle Daten, indem sie einen verborgenen Zustand über die Zeitschritte hinweg speichern. Für NLP wurden sie weitgehend von Transformern abgelöst, sie sind jedoch weiterhin relevant für Zeitreihen und Streaming-Anwendungen.

## Einfaches RNN {#simple-rnn}

Verarbeitet jeweils ein Element: h_t = tanh(W_hh * h_(t-1) + W_xh * x_t + b)

**Entscheidender Nachteil**: verschwindende Gradienten. Bei Sequenzen mit mehr als ca. 20 Tokens schrumpfen die Gradienten bei der Backpropagation through Time (BPTT) exponentiell. Langreichweitige Abhängigkeiten können so nicht gelernt werden.

### Warum verschwindende Gradienten auftreten {#why-vanishing-gradients-happen}

Die Ausgabevorhersage y_hat(T) ist eine zusammengesetzte Funktion aller Eingaben x_1...x_T. Die Gewichtsmatrix W_xh wird bei jedem Zeitschritt mit jeder Eingabe multipliziert. Beim Berechnen des Gradienten von W_xh über die Kettenregel entsteht daher ein Produkt aus vielen Ableitungen. Liegen die Eigenwerte von W_hh unter 1, schrumpft das Produkt exponentiell (verschwindend). Liegen sie über 1, explodiert es (explodierende Gradienten). Das bedeutet: Der Einfluss früher Eingaben auf die finale Ausgabe wird vernachlässigbar, das Netz "vergisst" frühe Tokens.

**Explodierende Gradienten** lassen sich mit Gradient Clipping gut beherrschen. **Verschwindende Gradienten** sind das schwierigere Problem – genau dafür wurden LSTM und GRU entwickelt.

## LSTM (Long Short-Term Memory) {#lstm-long-short-term-memory}

Löst das Problem der verschwindenden Gradienten mit einem Zellzustand, der **additive** (nicht multiplikative) Updates verwendet. Dadurch können Gradienten ohne Verschwinden durch die Zeit fließen:

- **Forget Gate**: legt fest, was aus dem Zellzustand verworfen wird. f_t = sigma(W_f * [h_(t-1), x_t] + b_f)
- **Input Gate**: legt fest, welche neuen Informationen gespeichert werden. i_t = sigma(W_i * [h_(t-1), x_t] + b_i)
- **Output Gate**: legt fest, was ausgegeben wird. o_t = sigma(W_o * [h_(t-1), x_t] + b_o)
- **Zellzustand**: Pfad für das Langzeitgedächtnis mit additiven Updates (Gradienten fließen ungehindert)

Verarbeitet Sequenzen mit ca. 200–500 Tokens effektiv.

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

Vereinfachtes LSTM mit zwei statt drei Gates:
- **Update Gate**: kombiniert Forget- und Input-Gate
- **Reset Gate**: steuert, wie viel der Vergangenheit ignoriert wird

Ähnliche Leistung wie LSTM, weniger Parameter und etwas schneller.

```python
gru = nn.GRU(input_size=300, hidden_size=128, num_layers=2,
             bidirectional=True, batch_first=True)
```

## Bidirektional {#bidirectional}

Die Sequenz wird vorwärts UND rückwärts verarbeitet, die verborgenen Zustände werden konkateniert. So werden sowohl linker als auch rechter Kontext erfasst.

Die Ausgabedimension verdoppelt sich: hidden_size * 2 bei bidirektionalen Modellen.

**Verwenden für**: Klassifikation, Tagging und alles, bei dem die vollständige Sequenz vorliegt.
**Nicht verwenden für**: Generierung (während der Generierung sind zukünftige Tokens nicht verfügbar).

## Zeitreihen mit RNNs {#time-series-with-rnns}

### Prognosemuster {#forecasting-pattern}
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

### AR-Modelle (AutoRegressive) {#ar-autoregressive-models}
y_t = phi_1 * y_(t-1) + phi_2 * y_(t-2) + ... + phi_p * y_(t-p)

Features werden automatisch aus den Lags extrahiert – manuelles Feature Engineering für die Zielvariable entfällt.

## Kategorien sequentieller Daten {#sequence-data-categories}

Verschiedene Sequenzaufgaben haben unterschiedliche Ein- und Ausgabeformen:

| Kategorie | Eingabe | Ausgabe | Beispiele |
|----------|-------|--------|----------|
| Viele-zu-eins | Sequenz | Einzelner Wert | Sentimentanalyse, Aktivitätserkennung |
| Eins-zu-viele | Einzelner Wert | Sequenz | Musikgenerierung, Bildbeschreibung |
| Viele-zu-viele (gleich lang) | Sequenz | Sequenz gleicher Länge | NER, POS-Tagging |
| Viele-zu-viele (ungleich lang) | Sequenz | Sequenz anderer Länge | Übersetzung, Zusammenfassung |

Hinweis: "Eins-zu-viele" kann eine leere bzw. Null-Eingabe haben (z. B. unbedingte Musikgenerierung) oder einen Seed-Wert (Genre-ID, erste Noten).

## Sequence-to-Sequence {#sequence-to-sequence}

Der Encoder verarbeitet die Eingabesequenz -> Kontextvektor -> der Decoder erzeugt die Ausgabesequenz.

**Anwendungen**: maschinelle Übersetzung, Zusammenfassung, Chatbots.

**Attention-Mechanismus**: Der Decoder berücksichtigt alle verborgenen Zustände des Encoders statt nur des letzten. Dadurch wird der Informationsengpass eines Kontextvektors fester Größe gelöst.

## Training von RNNs: Batching und Sequenzlänge {#training-rnns-batching-and-sequence-length}

### Erzeugen von Trainingsbatches {#generating-training-batches}

Bei Sprachmodellen auf Zeichen- oder Wortebene muss der vollständige Text in überlappende Eingabe-/Zielpaare zerschnitten werden:

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

**Wichtige Parameter**:

- **Sequenzlänge**: mindestens ca. 100 Zeichen/Tokens. Längere Sequenzen bieten mehr Kontext, verlangsamen aber das Training und benötigen mehr Speicher
- **Batchgröße**: typischerweise 64–128. Größere Batches liefern stabilere Gradienten, können aber in schärfere Minima konvergieren
- **Epochen**: abhängig von Datensatzgröße und Modellkapazität. Den Loss überwachen – stoppen, sobald der Validation Loss stagniert

### Trainingsschleife (PyTorch) {#training-loop-pattern-pytorch}

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

**Kritisch**: `hidden.detach()` an jeder Batchgrenze verhindert die Backpropagation über die gesamte Sequenzhistorie (was speichertechnisch nicht praktikabel wäre). Dies ist Truncated BPTT.

## Stolperfallen {#gotchas}
- RNNs sind von Natur aus sequentiell – eine Parallelisierung über Zeitschritte hinweg ist nicht möglich (langsames Training)
- LSTM/GRU helfen, lösen aber langreichweitige Abhängigkeiten bei sehr langen Sequenzen nicht vollständig
- Für die meisten NLP-Aufgaben übertreffen Transformer RNNs deutlich
- Gradient Clipping ist häufig notwendig: `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`
- Sequenzen variabler Länge benötigen Padding und Masking
- **Detach des verborgenen Zustands**: Wird der Hidden State zwischen Batches nicht detacht, wächst der Berechnungsgraph unbegrenzt und führt zu OOM-Fehlern
- **Sequenzlänge vs. Speicher**: Eine Verdopplung der Sequenzlänge verdoppelt etwa den Speicherbedarf und die Trainingszeit pro Batch

## Siehe auch {#see-also}
- [[nlp-text-processing]] - Transformer haben RNNs für NLP weitgehend abgelöst
- [[neural-networks]] - allgemeine Grundlagen des Deep Learning
- [[time-series-analysis]] - statistische Methoden für Zeitreihen

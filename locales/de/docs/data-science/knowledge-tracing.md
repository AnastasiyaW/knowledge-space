---
title: "Knowledge Tracing"
category: techniques
tags: [knowledge-tracing, learner-modeling, adaptive-learning, spaced-repetition, education-ai, knowledge-graph]
level: 3
source_sha256: 7173517e48300e2d723245cfbc274add01abc5ea13db25097f15855843d29ec0
translation: machine
translated_at: '2026-10-24'
---
# Knowledge Tracing {#knowledge-tracing}

Knowledge Tracing (KT) modelliert die Wahrscheinlichkeit, mit der eine lernende Person eine Frage richtig beantwortet, auf Grundlage ihres bisherigen Interaktionsverlaufs. Sie ist eine zentrale Komponente adaptiver Lernsysteme, die entscheiden, was als Nächstes gelehrt wird und wann wiederholt werden sollte.

## Kernfakten {#key-facts}

- KT-Modelle nehmen Sequenzen von (Frage, richtig/falsch)-Paaren entgegen und sagen P(richtig) für die nächste Frage voraus
- Entwicklung: BKT (1995) -> DKT (2015) -> SAKT (2019) -> AKT (2020) -> simpleKT (2023) -> Frontier-Modelle (2025)
- simpleKT (ICLR 2023) ist ein vereinfachter Transformer-Baseline, der die meisten komplexen Modelle schlägt – schwer zu übertreffen
- pyKT ist die Standardbibliothek: über 10 Modelle, über 7 Datensätze, aktiv gepflegt
- FSRS-7 ist der SOTA-Scheduler für Spaced Repetition – integriert in Anki 23.10+, Implementierungen in JS/Go/Rust/Python
- Die vierschichtige Architektur adaptiven Lernens (Domänenmodell, Lernendenmodell, Tutoring-Modell, Benutzeroberfläche) ist das Standardframework

## Modellentwicklung {#model-evolution}

### BKT (Bayesian Knowledge Tracing) {#bkt-bayesian-knowledge-tracing}

Hidden-Markov-Modell mit einem binären Beherrschungszustand pro Fertigkeit. Vier Parameter pro Fertigkeit: P(init), P(learn), P(guess), P(slip).

```text
State: UNLEARNED -> LEARNED (transition with P(learn))

Observation model:
  If LEARNED:   P(correct) = 1 - P(slip)
  If UNLEARNED: P(correct) = P(guess)

After each observation, update P(LEARNED) via Bayes' rule.
Mastery threshold: typically P(LEARNED) > 0.95
```

Einschränkungen: binäre Beherrschung (kein partielles Wissen), unabhängige Fertigkeiten (kein Transfer), kein Vergessen.

### DKT (Deep Knowledge Tracing, 2015) {#dkt-deep-knowledge-tracing-2015}

RNN/LSTM über die gesamte Interaktionssequenz. Lernt den latenten Wissenszustand implizit.

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

Verbesserung gegenüber BKT: erfasst komplexe Abhängigkeiten zwischen Fertigkeiten, partielles Wissen und zeitliche Muster. Allerdings wirkt es als Black Box – es gibt keinen interpretierbaren Wissenszustand.

### SAKT (Self-Attentive KT, 2019) {#sakt-self-attentive-kt-2019}

Ersetzt das RNN durch Self-Attention. Die Methode richtet die Aufmerksamkeit selektiv auf relevante vergangene Interaktionen, statt alles in einen verborgenen Zustand zu komprimieren.

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

Ergänzt kontextuelle Aufmerksamkeit und exponentiellen Zerfall für das Vergessen. Berücksichtigt die Ähnlichkeit von Fragen explizit.

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

Vereinfachter Transformer-Baseline mit fragespezifischer Schwierigkeit, inspiriert vom Rasch-Modell. Trotz seiner Einfachheit schwer zu schlagen.

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

### Frontier-Modelle 2025 {#2025-frontier-models}

| Modell | Innovation | Architektur |
|--------|-----------|-------------|
| DKT2 | xLSTM + IRT-Ausgabe | Interpretierbares Deep KT |
| HCGKT | Hierarchischer Graph + kontrastives Lernen | Graph-Faltungen |
| LefoKT | Entkoppelt Vergessen von Relevanz | Relative Vergessens-Aufmerksamkeit |
| UKT | Wissen als Wahrscheinlichkeitsverteilungen | Wasserstein-Attention |
| ReKT | 3D-Wissenszustand (Thema/Punkt/Domäne) | FRU: Forget-Response-Update |
| DyGKT | Dynamische Voraussetzungsgraphen | GNNs für die Voraussetzungsstruktur |

## Architektur adaptiven Lernens {#adaptive-learning-architecture}

Standardarchitektur mit vier Schichten für den Aufbau adaptiver Bildungssysteme:

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

## Spaced Repetition mit FSRS-7 {#spaced-repetition-with-fsrs-7}

FSRS (Free Spaced Repetition Scheduler) ist der SOTA-Algorithmus zur Planung von Wiederholungen. Er basiert auf der vorhergesagten Vergesswahrscheinlichkeit statt auf festen Intervallen.

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

## Kompression des Lernendenkontexts {#student-context-compression}

Effiziente Kodierung des Lernendenzustands für LLM-basierte Tutoring-Systeme:

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

## pyKT-Bibliothek {#pykt-library}

Die Standard-Python-Bibliothek für Forschung und Einsatz im Bereich Knowledge Tracing.

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

Verfügbare Modelle: DKT, DKVMN, SAKT, AKT, simpleKT, CL4KT, LPKT, HawkesKT und weitere.

## Open-Source-Plattformen {#open-source-platforms}

- **adaptive-knowledge-graph** – Wissensgraphen + lokale LLMs + Bayes'sches Fertigkeits-Tracking, datenschutzorientiertes RAG mit KG-gestütztem Retrieval, IRT/BKT-Modellierung der Beherrschung
- **OATutor** – React + Firebase, BKT zur Fertigkeitsbeherrschung, praxiserprobt in Klassenzimmern
- **pyKT** – Standard-KT-Bibliothek, über 10 Modelle, über 7 standardisierte Datensätze

## Stolperfallen {#gotchas}

- **simpleKT ist täuschend schwer zu schlagen** – viele Arbeiten behaupten Verbesserungen gegenüber DKT/SAKT, übertreffen simpleKT aber nicht, wenn sie sorgfältig abgestimmt werden. Es sollte immer als Baseline verwendet werden. Der Rasch-inspirierte Schwierigkeitsparameter der Fragen trägt den größten Teil der Leistung
- **Zeitliches Datenleck bei der Evaluation** – zufällige Train/Test-Splits leaken Zukunftsinformationen (Interaktionen der Lernenden aus späteren Sitzungen landen im Training). Immer zeitliche Splits verwenden: auf Interaktionen vor dem Zeitpunkt T trainieren, auf Interaktionen nach T testen
- **Die Qualität des Wissensgraphen begrenzt alles** – das Domänenmodell (Voraussetzungsstruktur) wird typischerweise manuell erstellt und ist aufwendig. Fehler in den Voraussetzungen pflanzen sich über das Tutoring-Modell fort. Die automatisierte Konstruktion von KGs aus Übungsdaten ist ein aktives Forschungsfeld, aber noch nicht zuverlässig
- **Vergessen ist asymmetrisch** – Fertigkeiten, die durch anstrengenden Abruf gelernt wurden, werden langsamer vergessen als solche, die durch wiederholtes Lesen oder Hinweise erworben wurden. KT-Modelle, die alle richtigen Antworten gleich behandeln, übersehen dies. AKT und LefoKT adressieren das teilweise

## Siehe auch {#see-also}

- [[bayesian-methods]] – Grundlage für BKT- und IRT-Modelle
- [[rnn-sequences]] – LSTM-Architektur, die in DKT verwendet wird
- [[attention-mechanisms]] – Self-Attention, verwendet in SAKT, AKT, simpleKT
- [[graph-neural-networks]] – GNNs, verwendet in DyGKT und HCGKT
- [[recommender-systems]] – ähnliche kollaborative Filterideen gelten für die Empfehlung von Übungen

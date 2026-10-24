---
title: "Verstärkendes Lernen"
category: concepts
tags: [data-science, reinforcement-learning, q-learning, policy-gradient, deep-rl]
level: 3
source_sha256: 4760c5e520d6c1508c2e8daa601e70e2706e28f67e6ac7226eaafa9b219f991e
translation: machine
translated_at: '2026-10-24'
---
# Verstärkendes Lernen {#reinforcement-learning}

Ein Agent lernt durch Interaktion mit einer Umgebung, indem er Belohnungen bzw. Strafen erhält und eine Policy optimiert, um die kumulative Belohnung zu maximieren. Anders als beim überwachten Lernen gibt es keine gelabelten Beispiele – der Agent entdeckt optimales Verhalten durch Versuch und Irrtum.

## Kernkonzepte {#core-concepts}

- **Agent**: der Lernende bzw. Entscheidungsträger
- **Umgebung (Environment)**: alles außerhalb des Agenten
- **Zustand (s)**: Repräsentation der aktuellen Situation
- **Aktion (a)**: was der Agent tun kann
- **Belohnung (r)**: skalares Feedbacksignal
- **Policy (pi)**: Abbildung von Zuständen auf Aktionen
- **Wertfunktion V(s)**: erwartete kumulative Belohnung ab Zustand s
- **Q-Funktion Q(s,a)**: erwartete kumulative Belohnung, wenn Aktion a in Zustand s ausgeführt wird
- **Diskontierungsfaktor (gamma)**: 0–1, wie stark zukünftige im Vergleich zu unmittelbaren Belohnungen gewichtet werden

**Zielkonflikt zwischen Exploration und Exploitation**: Der Agent muss abwägen zwischen dem Ausprobieren neuer Aktionen (Exploration) und der Nutzung bekannter guter Aktionen (Exploitation). Epsilon-Greedy ist die einfachste Strategie: Mit Wahrscheinlichkeit epsilon wird eine zufällige Aktion gewählt, andernfalls die bisher beste bekannte Aktion.

## Markov-Entscheidungsprozess (MDP) {#markov-decision-process-mdp}

Formaler Rahmen: (S, A, P, R, gamma), wobei P die Übergangswahrscheinlichkeit und R die Belohnungsfunktion ist.

**Markov-Eigenschaft**: Die Zukunft hängt nur vom aktuellen Zustand ab, nicht von der Historie. Ist sie verletzt, muss der Zustand erweitert werden (Frame Stacking, rekurrente Netze).

**Bellman-Gleichung** setzt den Wert eines Zustands in Beziehung zu den Werten der Folgezustände:
V(s) = max_a [R(s,a) + gamma * sum P(s'|s,a) * V(s')]

## Tabellarische Verfahren {#tabular-methods}

### Q-Learning (Off-Policy) {#q-learning-off-policy}

Lernt Q-Werte direkt. Off-Policy: Es kann aus Daten gelernt werden, die von einer beliebigen Policy erzeugt wurden.

```python
import numpy as np

# Q-table: states x actions
Q = np.zeros((n_states, n_actions))
alpha = 0.1   # learning rate
gamma = 0.99  # discount
epsilon = 0.1 # exploration

for episode in range(n_episodes):
    state = env.reset()
    done = False
    while not done:
        # Epsilon-greedy action selection
        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state])

        next_state, reward, done, _ = env.step(action)

        # Q-learning update (uses max over next actions)
        Q[state, action] += alpha * (
            reward + gamma * np.max(Q[next_state]) - Q[state, action]
        )
        state = next_state
```

### SARSA (On-Policy) {#sarsa-on-policy}

Das Update verwendet die tatsächlich ausgeführte Aktion und nicht das gierige Maximum:

```python
# SARSA update
next_action = epsilon_greedy(Q[next_state], epsilon)
Q[state, action] += alpha * (
    reward + gamma * Q[next_state, next_action] - Q[state, action]
)
```

SARSA ist konservativer – es berücksichtigt in seinen Schätzungen die Exploration.

## Deep RL {#deep-rl}

Wenn der Zustandsraum für Tabellen zu groß ist (Bilder, kontinuierliche Werte), werden neuronale Netze eingesetzt, um Wert- bzw. Policy-Funktionen zu approximieren.

### Deep Q-Network (DQN) {#deep-q-network-dqn}

Ein neuronales Netz approximiert Q(s,a). Zentrale Tricks für Stabilität:

```python
import torch
import torch.nn as nn

class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim)
        )

    def forward(self, x):
        return self.net(x)

# Two networks: online + target (updated periodically)
online_net = DQN(state_dim, action_dim)
target_net = DQN(state_dim, action_dim)
target_net.load_state_dict(online_net.state_dict())

# Experience replay buffer
from collections import deque
replay_buffer = deque(maxlen=100000)

# Training step
batch = random.sample(replay_buffer, batch_size)
states, actions, rewards, next_states, dones = zip(*batch)

current_q = online_net(states).gather(1, actions)
with torch.no_grad():
    next_q = target_net(next_states).max(1)[0]
    target_q = rewards + gamma * next_q * (1 - dones)

loss = nn.MSELoss()(current_q.squeeze(), target_q)
```

**Experience Replay**: Übergänge werden gespeichert und zufällige Mini-Batches daraus gezogen. Dies bricht die Korrelation zwischen aufeinanderfolgenden Samples auf.

**Target Network**: separates Netz zur Berechnung der Zielwerte, das alle N Schritte aktualisiert wird. Verhindert das Problem des sich bewegenden Ziels.

### Policy-Gradient-Verfahren {#policy-gradient-methods}

Die Policy wird direkt optimiert, ohne eine Wertfunktion zu lernen.

**REINFORCE**: einfachstes Policy-Gradient-Verfahren. Hohe Varianz, langsame Konvergenz.

**Actor-Critic**: Actor (Policy-Netz) und Critic (Wertnetz). Der Critic reduziert die Varianz des Policy-Gradienten.

**PPO (Proximal Policy Optimization)**: derzeit populärster moderner Algorithmus. Begrenzt (clippt) Policy-Updates, um zu große Änderungen zu verhindern.

```python
# PPO clipped objective (pseudocode)
ratio = new_policy(action|state) / old_policy(action|state)
advantage = rewards_to_go - value_estimate

clipped_ratio = torch.clamp(ratio, 1 - epsilon, 1 + epsilon)
loss = -torch.min(ratio * advantage, clipped_ratio * advantage).mean()
```

## RL in der Finanzwelt {#rl-for-finance}

- **Portfoliooptimierung**: Aktionen = Allokationen von Vermögenswerten, Belohnung = risikoadjustierte Renditen
- **Order Execution**: Minimierung des Marktein­flusses bei der Ausführung großer Orders
- **Market Making**: Festlegung von Bid/Ask-Spreads, Belohnung = Gewinn abzüglich Inventarrisiko
- **Herausforderung**: nicht-stationäre Umgebung, partielle Beobachtbarkeit, geringes Signal-Rausch-Verhältnis

## Reward Shaping {#reward-shaping}

Das Entwerfen von Belohnungsfunktionen ist der schwierigste Teil des RL.

- **Spärliche Belohnungen (Sparse Rewards)**: nur am Episodenende (Gewinn/Verlust). Schwer zu lernen – es werden Explorationsboni benötigt
- **Dichte Belohnungen (Dense Rewards)**: kontinuierliches Feedback. Einfacher zu lernen, kann jedoch Reward Hacking verursachen
- **Reward Shaping**: Hinzufügen von Zwischenbelohnungen, ohne die optimale Policy zu verändern. Muss die potenzialbasierte Bedingung erfüllen
- **Neugiergetriebene Exploration**: intrinsische Belohnung für neuartige Zustände (Vorhersagefehler als Belohnung)

## Stolperfallen {#gotchas}

- **Reward Hacking**: Der Agent findet unbeabsichtigte Abkürzungen. Ist die Belohnung „nicht abstürzen", könnte der Agent lernen, sich gar nicht zu bewegen. Das gelernte Verhalten muss stets auf die beabsichtigte Absicht geprüft werden, nicht nur auf das Belohnungssignal
- **Katastrophales Vergessen bei DQN**: Ohne Experience Replay overfittet das Netz auf die jüngsten Erfahrungen und vergisst frühere Erkenntnisse. Die Puffergröße ist entscheidend – zu klein führt zu Verlust an Vielfalt, zu groß verschwendet Speicher
- **Hyperparameter-Sensitivität**: RL reagiert bekanntermaßen empfindlich auf Lernrate, Epsilon-Schedule, Gamma und Netzarchitektur. Kleine Änderungen können zum vollständigen Scheitern führen. Zuerst immer eine Grid Search auf einfachen Umgebungen durchführen
- **Sample-Ineffizienz**: Deep RL benötigt Millionen von Interaktionen mit der Umgebung. Sim-to-Real-Transfer (Training im Simulator, Einsatz in der realen Welt) ist gängige Praxis, die Domänenlücke ist jedoch ein echtes Problem

## Siehe auch {#see-also}

- [[neural-networks]]
- [[model-evaluation]]
- [[ml-system-design]]

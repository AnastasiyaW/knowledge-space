---
title: "Apprentissage par renforcement"
category: concepts
tags: [data-science, reinforcement-learning, q-learning, policy-gradient, deep-rl]
level: 3
source_sha256: 4760c5e520d6c1508c2e8daa601e70e2706e28f67e6ac7226eaafa9b219f991e
translation: machine
translated_at: '2026-10-24'
---
# Apprentissage par renforcement {#reinforcement-learning}

L'agent apprend en interagissant avec un environnement, en recevant des récompenses ou des pénalités, et en optimisant une politique afin de maximiser la récompense cumulée. Contrairement à l'apprentissage supervisé, il n'existe pas d'exemples étiquetés : l'agent découvre le comportement optimal par essais et erreurs.

## Concepts fondamentaux {#core-concepts}

- **Agent** : l'apprenant et décideur
- **Environnement** : tout ce qui est extérieur à l'agent
- **État (s)** : représentation de la situation courante
- **Action (a)** : ce que l'agent peut faire
- **Récompense (r)** : signal de retour scalaire
- **Politique (pi)** : application des états vers les actions
- **Fonction de valeur V(s)** : récompense cumulée espérée à partir de l'état s
- **Fonction Q Q(s,a)** : récompense cumulée espérée en exécutant l'action a dans l'état s
- **Facteur d'actualisation (gamma)** : compris entre 0 et 1, indique le poids accordé aux récompenses futures par rapport aux récompenses immédiates

**Compromis exploration vs exploitation** : l'agent doit équilibrer l'essai de nouvelles actions (explorer) et l'utilisation d'actions connues comme bonnes (exploiter). L'epsilon-greedy est la stratégie la plus simple : une action aléatoire avec une probabilité epsilon, sinon la meilleure action connue.

## Processus de décision markovien (MDP) {#markov-decision-process-mdp}

Cadre formel : (S, A, P, R, gamma), où P est la probabilité de transition et R la fonction de récompense.

**Propriété de Markov** : le futur ne dépend que de l'état courant, et non de l'historique. Si elle n'est pas vérifiée, il faut enrichir l'état (empilement de trames, réseaux récurrents).

**Équation de Bellman** : elle relie la valeur d'un état aux valeurs des états successeurs :
V(s) = max_a [R(s,a) + gamma * somme P(s'|s,a) * V(s')]

## Méthodes tabulaires {#tabular-methods}

### Q-Learning (hors politique) {#q-learning-off-policy}

Apprend directement les valeurs Q. Hors politique : il peut apprendre à partir de données générées par n'importe quelle politique.

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

### SARSA (sur politique) {#sarsa-on-policy}

La mise à jour utilise l'action effectivement exécutée, et non le maximum glouton :

```python
# SARSA update
next_action = epsilon_greedy(Q[next_state], epsilon)
Q[state, action] += alpha * (
    reward + gamma * Q[next_state, next_action] - Q[state, action]
)
```

SARSA est plus conservateur : il tient compte de l'exploration dans ses estimations.

## Apprentissage profond par renforcement (Deep RL) {#deep-rl}

Lorsque l'espace des états est trop grand pour des tables (images, espaces continus), on utilise des réseaux de neurones pour approximer les fonctions de valeur ou de politique.

### Deep Q-Network (DQN) {#deep-q-network-dqn}

Un réseau de neurones approxime Q(s,a). Astuces clés pour la stabilité :

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

**Rejeu d'expérience** : stocker les transitions et échantillonner des mini-lots aléatoires. Cela rompt la corrélation entre échantillons consécutifs.

**Réseau cible** : réseau distinct servant au calcul des cibles, mis à jour toutes les N étapes. Cela évite le problème de la cible mouvante.

### Méthodes de gradient de politique {#policy-gradient-methods}

Optimisent directement la politique, sans apprendre de fonction de valeur.

**REINFORCE** : gradient de politique le plus simple. Variance élevée, convergence lente.

**Acteur-critique** : acteur (réseau de politique) + critique (réseau de valeur). Le critique réduit la variance du gradient de politique.

**PPO (Proximal Policy Optimization)** : algorithme moderne le plus populaire. Il borne les mises à jour de la politique pour éviter des changements trop importants.

```python
# PPO clipped objective (pseudocode)
ratio = new_policy(action|state) / old_policy(action|state)
advantage = rewards_to_go - value_estimate

clipped_ratio = torch.clamp(ratio, 1 - epsilon, 1 + epsilon)
loss = -torch.min(ratio * advantage, clipped_ratio * advantage).mean()
```

## RL appliqué à la finance {#rl-for-finance}

- **Optimisation de portefeuille** : actions = allocations d'actifs, récompense = rendements ajustés du risque
- **Exécution d'ordres** : minimiser l'impact de marché lors de l'exécution d'ordres importants
- **Tenue de marché (market making)** : fixer les écarts achat/vente, récompense = profit moins risque d'inventaire
- **Difficulté** : environnement non stationnaire, observabilité partielle, faible rapport signal/bruit

## Façonnage de la récompense (reward shaping) {#reward-shaping}

La conception des fonctions de récompense est la partie la plus difficile du RL.

- **Récompenses éparses** : uniquement en fin d'épisode (gain ou perte). Difficiles à apprendre : il faut des bonus d'exploration
- **Récompenses denses** : retour continu. Plus faciles à apprendre, mais peuvent provoquer un détournement de la récompense (reward hacking)
- **Façonnage de la récompense** : ajouter des récompenses intermédiaires sans modifier la politique optimale. Doit satisfaire la condition basée sur le potentiel
- **Exploration guidée par la curiosité** : récompense intrinsèque pour les états nouveaux (erreur de prédiction utilisée comme récompense)

## Pièges courants {#gotchas}

- **Détournement de la récompense (reward hacking)** : l'agent trouve des raccourcis non prévus. Si la récompense est « ne pas s'écraser », l'agent peut apprendre à ne pas bouger du tout. Vérifier systématiquement que le comportement appris correspond à l'intention, et non seulement au signal de récompense
- **Oubli catastrophique dans DQN** : sans rejeu d'expérience, le réseau sur-apprend l'expérience récente et oublie les enseignements antérieurs. La taille du tampon est déterminante : trop petite, elle perd en diversité ; trop grande, elle gaspille de la mémoire
- **Sensibilité aux hyperparamètres** : le RL est notoirement sensible au taux d'apprentissage, au calendrier d'epsilon, à gamma et à l'architecture du réseau. De faibles variations peuvent entraîner un échec total. Toujours commencer par une recherche sur grille dans des environnements simples
- **Inefficacité d'échantillonnage** : le Deep RL nécessite des millions d'interactions avec l'environnement. Le transfert simulation-réel (entraînement en simulateur, déploiement dans le monde réel) est une pratique courante, mais l'écart entre les domaines constitue un problème réel

## Voir aussi {#see-also}

- [[neural-networks]]
- [[model-evaluation]]
- [[ml-system-design]]

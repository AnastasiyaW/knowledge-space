---
title: "Réseaux de neurones sur graphes"
category: concepts
tags: [data-science, gnn, graph-learning, pytorch-geometric, node-classification, link-prediction]
level: 3
source_sha256: 693490068475266785987183d1baa91493a480247d408950620812b1c41edc6a
translation: machine
translated_at: '2026-10-24'
---
# Réseaux de neurones sur graphes {#graph-neural-networks}

Les GNN opèrent sur des données structurées en graphes, où des entités (nœuds) entretiennent des relations (arêtes). Réseaux sociaux, molécules, réseaux de citations, graphes de connaissances, systèmes de recommandation : tous se représentent naturellement sous forme de graphes. Les réseaux de neurones standard ne savent pas gérer des voisinages de taille variable ni l'invariance par permutation.

## Concepts fondamentaux {#core-concepts}

- **Caractéristiques des nœuds** : vecteurs d'attributs par nœud (profil utilisateur, type d'atome)
- **Caractéristiques des arêtes** : vecteurs d'attributs par arête (type de relation, type de liaison)
- **Matrice d'adjacence A** : encode la structure du graphe (N×N pour N nœuds)
- **Message passing** : les nœuds agrègent itérativement l'information de leurs voisins

**Idée clé** : les GNN apprennent les représentations des nœuds en agrégeant les caractéristiques de leurs voisinages locaux. Après k couches, la représentation de chaque nœud intègre l'information de ses voisins à k sauts.

## Cadre du message passing {#message-passing-framework}

Chaque couche GNN suit le schéma : agréger les voisins -> combiner avec soi-même -> mettre à jour.

```python
# Pseudocode for one GNN layer
def gnn_layer(node_features, adjacency):
    messages = {}
    for node in graph.nodes:
        # 1. Aggregate: collect messages from neighbors
        neighbor_msgs = [node_features[n] for n in neighbors(node)]
        aggregated = AGGREGATE(neighbor_msgs)  # sum, mean, max

        # 2. Update: combine with own features
        messages[node] = UPDATE(node_features[node], aggregated)
    return messages
```

## Architectures GNN {#gnn-architectures}

### GCN (Graph Convolutional Network) {#gcn-graph-convolutional-network}

Basé sur la spectrale. Normalisation symétrique de la matrice d'adjacence.

```python
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class GCN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index)
        return x

model = GCN(dataset.num_features, 64, dataset.num_classes)
```

### GAT (Graph Attention Network) {#gat-graph-attention-network}

Poids d'attention apprenables pour l'agrégation des voisins :

```python
from torch_geometric.nn import GATConv

class GAT(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, heads=8):
        super().__init__()
        self.conv1 = GATConv(in_channels, hidden_channels, heads=heads, dropout=0.6)
        self.conv2 = GATConv(hidden_channels * heads, out_channels, heads=1, dropout=0.6)

    def forward(self, x, edge_index):
        x = F.elu(self.conv1(x, edge_index))
        x = self.conv2(x, edge_index)
        return x
```

### GraphSAGE {#graphsage}

Inductif : peut généraliser à des nœuds non vus (contrairement aux GCN/GAT transductifs).

```python
from torch_geometric.nn import SAGEConv

class GraphSAGE(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        x = self.conv2(x, edge_index)
        return x
```

## Tâches {#tasks}

### Classification de nœuds {#node-classification}

Prédire l'étiquette de chaque nœud (par ex. catégorie d'utilisateur dans un réseau social) :

```python
from torch_geometric.datasets import Planetoid

dataset = Planetoid(root='/data', name='Cora')
data = dataset[0]

model = GCN(dataset.num_features, 64, dataset.num_classes)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

for epoch in range(200):
    model.train()
    optimizer.zero_grad()
    out = model(data.x, data.edge_index)
    loss = F.cross_entropy(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()
```

### Prédiction de liens {#link-prediction}

Prédire si une arête doit exister entre deux nœuds (par ex. recommandation d'amis) :

```python
from torch_geometric.utils import negative_sampling

def link_prediction_loss(model, data, pos_edge_index):
    z = model(data.x, data.edge_index)  # node embeddings

    # Positive edges
    pos_score = (z[pos_edge_index[0]] * z[pos_edge_index[1]]).sum(dim=1)

    # Negative sampling
    neg_edge_index = negative_sampling(
        edge_index=data.edge_index,
        num_nodes=data.num_nodes,
        num_neg_samples=pos_edge_index.size(1)
    )
    neg_score = (z[neg_edge_index[0]] * z[neg_edge_index[1]]).sum(dim=1)

    loss = F.binary_cross_entropy_with_logits(
        torch.cat([pos_score, neg_score]),
        torch.cat([torch.ones_like(pos_score), torch.zeros_like(neg_score)])
    )
    return loss
```

### Classification de graphes {#graph-classification}

Prédire l'étiquette de l'ensemble du graphe (par ex. toxicité d'une molécule) :

```python
from torch_geometric.nn import global_mean_pool

class GraphClassifier(torch.nn.Module):
    def __init__(self, in_channels, hidden, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden)
        self.conv2 = GCNConv(hidden, hidden)
        self.lin = torch.nn.Linear(hidden, out_channels)

    def forward(self, x, edge_index, batch):
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        x = global_mean_pool(x, batch)  # aggregate all nodes per graph
        return self.lin(x)
```

## Mini-batch pour les grands graphes {#mini-batching-for-large-graphs}

L'entraînement sur le graphe complet ne passe pas à l'échelle. Utiliser l'échantillonnage de voisinage :

```python
from torch_geometric.loader import NeighborLoader

loader = NeighborLoader(
    data,
    num_neighbors=[25, 10],  # sample 25 1-hop, 10 2-hop neighbors
    batch_size=256,
    input_nodes=data.train_mask,
)

for batch in loader:
    out = model(batch.x, batch.edge_index)
    loss = F.cross_entropy(out[:batch.batch_size], batch.y[:batch.batch_size])
```

## Pièges courants {#gotchas}

- **Sur-lissage avec des GNN profonds** : au-delà de 4 à 6 couches, toutes les représentations de nœuds convergent vers un même vecteur. Les nœuds deviennent indiscernables. Utiliser des connexions résiduelles (skip connections), DropEdge, ou limiter la profondeur à 2-3 couches pour la plupart des tâches
- **Scalabilité** : le GCN en batch complet nécessite la matrice d'adjacence entière en mémoire. Pour des graphes de l'ordre du million de nœuds, utiliser l'entraînement en mini-batch (NeighborLoader, ClusterLoader) ou des modèles simplifiés (SGC supprime les non-linéarités et s'exécute aussi vite qu'une régression logistique)
- **Les graphes hétérogènes nécessitent un traitement spécifique** : si les nœuds ou les arêtes ont différents types (utilisateur-achète-produit vs utilisateur-suit-utilisateur), les GNN standard perdent l'information de type. Utiliser `HeteroConv` ou le GCN relationnel (R-GCN), qui maintient des matrices de poids distinctes par type de relation

## Voir aussi {#see-also}

- [[neural-networks]]
- [[attention-mechanisms]]
- [[recommender-systems]]

---
title: "Graph Neural Networks"
category: concepts
tags: [data-science, gnn, graph-learning, pytorch-geometric, node-classification, link-prediction]
level: 3
source_sha256: 693490068475266785987183d1baa91493a480247d408950620812b1c41edc6a
translation: machine
translated_at: '2026-10-24'
---
# Graph Neural Networks {#graph-neural-networks}

GNNs arbeiten auf graphstrukturierten Daten, bei denen Entitäten (Knoten) untereinander Beziehungen (Kanten) haben. Soziale Netzwerke, Moleküle, Zitationsnetzwerke, Wissensgraphen, Empfehlungssysteme - all diese Daten lassen sich natürlich als Graphen darstellen. Standardmäßige neuronale Netze können jedoch weder Nachbarschaften variabler Größe verarbeiten noch Permutationsinvarianz abbilden.

## Kernkonzepte {#core-concepts}

- **Knotenmerkmale (Node Features)**: Attributvektoren pro Knoten (Nutzerprofil, Atomtyp)
- **Kantenmerkmale (Edge Features)**: Attributvektoren pro Kante (Beziehungstyp, Bindungstyp)
- **Adjazenzmatrix A**: kodiert die Graphstruktur (N×N für N Knoten)
- **Message Passing**: Knoten aggregieren iterativ Informationen von ihren Nachbarn

**Zentrale Erkenntnis**: GNNs lernen Knotenrepräsentationen, indem sie Merkmale aus lokalen Nachbarschaften aggregieren. Nach k Schichten erfasst die Repräsentation eines Knotens Informationen aus seinen k-Hop-Nachbarn.

## Message-Passing-Framework {#message-passing-framework}

Jede GNN-Schicht folgt dem Schema: Nachbarn aggregieren -> mit dem eigenen Knoten kombinieren -> aktualisieren.

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

## GNN-Architekturen {#gnn-architectures}

### GCN (Graph Convolutional Network) {#gcn-graph-convolutional-network}

Spektral basiert. Symmetrische Normalisierung der Adjazenzmatrix.

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

Lernbare Attention-Gewichte für die Nachbarschaftsaggregation:

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

Induktiv: kann auf ungesehene Knoten generalisieren (im Gegensatz zu transduktiven GCN/GAT).

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

## Aufgaben {#tasks}

### Knotenklassifikation {#node-classification}

Vorhersage des Labels für jeden Knoten (z. B. Nutzerkategorie in einem sozialen Netzwerk):

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

### Link Prediction {#link-prediction}

Vorhersage, ob zwischen zwei Knoten eine Kante bestehen sollte (z. B. Freundschaftsempfehlung):

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

### Graphklassifikation {#graph-classification}

Vorhersage eines Labels für den gesamten Graphen (z. B. Toxizität eines Moleküls):

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

## Mini-Batching für große Graphen {#mini-batching-for-large-graphs}

Training auf dem vollständigen Graphen skaliert nicht. Stattdessen Neighborhood Sampling verwenden:

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

## Stolperfallen {#gotchas}

- **Over-Smoothing bei tiefen GNNs**: Nach 4-6 Schichten konvergieren alle Knotenrepräsentationen zum selben Vektor. Die Knoten werden ununterscheidbar. Abhilfe schaffen Skip-Connections (Residual), DropEdge oder eine Begrenzung auf 2-3 Schichten für die meisten Aufgaben
- **Skalierbarkeit**: Full-Batch-GCN benötigt die gesamte Adjazenzmatrix im Speicher. Bei Graphen mit Millionen von Knoten sollten Mini-Batch-Training (NeighborLoader, ClusterLoader) oder vereinfachte Modelle verwendet werden (SGC entfernt die Nichtlinearitäten und läuft so schnell wie logistische Regression)
- **Heterogene Graphen erfordern spezielle Behandlung**: Haben Knoten oder Kanten unterschiedliche Typen (Nutzer-kauft-Produkt vs. Nutzer-folgt-Nutzer), verlieren Standard-GNNs die Typinformation. Verwenden Sie `HeteroConv` oder Relational GCN (R-GCN), die für jeden Beziehungstyp eigene Gewichtsmatrizen beibehalten

## Siehe auch {#see-also}

- [[neural-networks]]
- [[attention-mechanisms]]
- [[recommender-systems]]

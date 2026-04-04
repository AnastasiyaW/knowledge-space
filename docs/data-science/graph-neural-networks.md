---
title: Graph Neural Networks
category: concepts
tags: [data-science, gnn, graph-learning, pytorch-geometric, node-classification, link-prediction]
---

# Graph Neural Networks

GNNs operate on graph-structured data where entities (nodes) have relationships (edges). Social networks, molecules, citation networks, knowledge graphs, recommendation systems - all naturally represented as graphs. Standard neural networks cannot handle variable-size neighborhoods and permutation invariance.

## Core Concepts

- **Node features**: attribute vectors per node (user profile, atom type)
- **Edge features**: attribute vectors per edge (relationship type, bond type)
- **Adjacency matrix A**: encodes graph structure (NxN for N nodes)
- **Message passing**: nodes aggregate information from neighbors iteratively

**Key insight**: GNNs learn node representations by aggregating features from local neighborhoods. After k layers, each node's representation captures information from k-hop neighbors.

## Message Passing Framework

Every GNN layer follows: aggregate neighbors -> combine with self -> update.

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

## GNN Architectures

### GCN (Graph Convolutional Network)

Spectral-based. Symmetric normalization of adjacency.

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

### GAT (Graph Attention Network)

Learnable attention weights for neighbor aggregation:

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

### GraphSAGE

Inductive: can generalize to unseen nodes (unlike transductive GCN/GAT).

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

## Tasks

### Node Classification

Predict label for each node (e.g., user category in social network):

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

### Link Prediction

Predict if edge should exist between two nodes (e.g., friend recommendation):

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

### Graph Classification

Predict label for entire graph (e.g., molecule toxicity):

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

## Mini-Batching for Large Graphs

Full-graph training doesn't scale. Use neighborhood sampling:

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

## Gotchas

- **Over-smoothing with deep GNNs**: after 4-6 layers, all node representations converge to same vector. Nodes become indistinguishable. Use skip connections (residual), DropEdge, or limit depth to 2-3 layers for most tasks
- **Scalability**: full-batch GCN requires entire adjacency matrix in memory. For million-node graphs, use mini-batch training (NeighborLoader, ClusterLoader) or simplified models (SGC strips nonlinearities, runs as fast as logistic regression)
- **Heterogeneous graphs need special handling**: if nodes/edges have different types (user-buys-product vs user-follows-user), standard GNNs lose type information. Use `HeteroConv` or Relational GCN (R-GCN) that maintain separate weight matrices per relation type

## See Also

- [[neural-networks]]
- [[attention-mechanisms]]
- [[recommender-systems]]

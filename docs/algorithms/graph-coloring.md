---
title: Graph Coloring
category: algorithms
tags: [algorithms, graphs, coloring, chromatic-number, bipartite, NP-complete, scheduling]
---

# Graph Coloring

Graph coloring assigns colors to vertices such that no two adjacent vertices share a color. The chromatic number chi(G) is the minimum colors needed. 2-coloring (bipartiteness) is polynomial; k-coloring for k >= 3 is NP-complete.

## Key Facts

- **Chromatic number chi(G)**: minimum colors for valid coloring
- **2-colorable** iff bipartite iff no odd-length cycles - checkable in O(|V| + |E|)
- **k-colorable (k >= 3)**: NP-complete
- Greedy coloring uses at most Delta+1 colors (Delta = max degree)
- **Brooks' theorem**: chi(G) <= Delta for connected graphs that aren't complete or odd cycles
- **Vizing's theorem** (edge coloring): chi'(G) is either Delta or Delta+1

## Applications

- **Resource scheduling**: overlapping tasks as edges, colors = resources (min cars, rooms, etc.)
- **Register allocation** in compilers
- **Frequency assignment** in wireless networks
- **Exam scheduling**: conflicting exams need different time slots
- **Sudoku**: 9-coloring of constraint graph (81 vertices, edges for same row/col/box)

## Patterns

### Bipartite Check (2-Coloring) - O(|V| + |E|)

```python
from collections import deque

def is_bipartite(graph):
    color = {}
    for start in graph.adj_list:
        if start in color:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbor in graph.adj_list[vertex]:
                if neighbor not in color:
                    color[neighbor] = 1 - color[vertex]  # alternate
                    queue.append(neighbor)
                elif color[neighbor] == color[vertex]:
                    return False  # odd cycle found
    return True
```

### Greedy Coloring

```python
def greedy_coloring(graph, order=None):
    if order is None:
        order = list(graph.adj_list.keys())
    colors = {}
    for vertex in order:
        neighbor_colors = {colors[n] for n in graph.adj_list[vertex] if n in colors}
        color = 0
        while color in neighbor_colors:
            color += 1
        colors[vertex] = color
    return colors, max(colors.values()) + 1
```

Result depends on vertex order. Does NOT guarantee chromatic number.

### Welsh-Powell Heuristic

Order vertices by decreasing degree before greedy coloring. Often produces good (not optimal) results.

```python
def welsh_powell(graph):
    order = sorted(graph.adj_list,
                   key=lambda v: len(graph.adj_list[v]), reverse=True)
    return greedy_coloring(graph, order)
```

### Exact k-Coloring (Backtracking)

```python
def color_graph(graph, k):
    colors = {}

    def backtrack(vertex_list, idx):
        if idx == len(vertex_list):
            return True
        vertex = vertex_list[idx]
        for color in range(k):
            neighbor_colors = {colors.get(n) for n in graph.adj_list[vertex]}
            if color not in neighbor_colors:
                colors[vertex] = color
                if backtrack(vertex_list, idx + 1):
                    return True
                del colors[vertex]
        return False

    vertices = list(graph.adj_list.keys())
    if backtrack(vertices, 0):
        return colors
    return None  # not k-colorable
```

## Related Concepts

| Concept | Definition |
|---------|-----------|
| Clique | Subset of all pairwise adjacent vertices |
| Independence set | Subset with no two adjacent vertices |
| Clique number omega(G) | Size of largest clique. omega(G) <= chi(G) |
| Perfect graph | omega(G) = chi(G). Includes bipartite, chordal graphs |
| Edge coloring | Color edges, no two sharing a vertex same color |

## Gotchas

- Complete graph K_n needs exactly n colors
- Even cycle: chi = 2; Odd cycle: chi = 3
- Greedy coloring result depends entirely on vertex processing order
- Bipartite check handles disconnected graphs: must try starting from each uncolored vertex
- Edge coloring is different from vertex coloring: Vizing's theorem bounds it

## See Also

- [[network-flow]] - bipartite matching related to bipartite coloring
- [[eulerian-hamiltonian-paths]] - odd cycles appear in both contexts
- [[complexity-classes]] - k-coloring (k >= 3) is NP-complete

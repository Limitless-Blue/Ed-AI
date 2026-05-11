# Graphs

## Table of Contents
1. [Introduction to Graphs](#introduction-to-graphs)
   1. [Definitions and Basic Terminology](#definitions-and-basic-terminology)
   2. [Directed vs. Undirected Graphs](#directed-vs-undirected-graphs)
   3. [Weighted vs. Unweighted Graphs](#weighted-vs-unweighted-graphs)
2. [Graph Representation](#graph-representation)
   1. [Adjacency Matrix](#adjacency-matrix)
   2. [Adjacency List](#adjacency-list)

---

## Introduction to Graphs

Graphs are one of the most versatile and widely used data structures. They model relationships between objects and consist of two primary components: vertices (or nodes) and edges (connections between vertices).

### Definitions and Basic Terminology

- **Vertex (Node)**: A fundamental unit of a graph that can represent any entity, such as a person, city, or website.
- **Edge (Link)**: A connection between two vertices. It can represent any type of relationship, such as friendship, route, or hyperlink.
- **Degree**: The number of edges incident on a vertex. In directed graphs, we differentiate between in-degree and out-degree.
- **Path**: A sequence of vertices connected by edges.
- **Cycle**: A path that starts and ends at the same vertex without repeating any vertices (except the starting/ending one).
- **Connected Graph**: A graph where there is a path between every pair of vertices.
- **Disconnected Graph**: A graph where at least one pair of vertices is not connected by any path.

### Directed vs. Undirected Graphs

#### Undirected Graph:
An **undirected graph** has edges that do not have a direction. If there is an edge between vertices `A` and `B`, it can be traversed in both directions.

**Example:**

```
A ---- B
 \    /
  C -- D
```

In this undirected graph, edges are bidirectional, such as from `A` to `B` or from `B` to `A`.

**Properties:**
- The edge between two vertices can be traveled in either direction.
- The degree of a vertex is the total number of edges connected to it.

#### Directed Graph (Digraph):
A **directed graph** has edges with directions. Each edge points from one vertex to another and cannot be traversed in the opposite direction unless explicitly defined.

**Example:**

```
A → B
↑   ↓
C ← D
```

In this directed graph, the edges have directions, meaning that `A → B` does not imply `B → A`.

**Properties:**
- Each edge has a direction (from one vertex to another).
- Vertices have an in-degree (number of incoming edges) and out-degree (number of outgoing edges).

### Weighted vs. Unweighted Graphs

#### Unweighted Graph:
An **unweighted graph** has edges that represent connections without any additional information about the "cost" or "distance" between nodes.

**Example:**

```
A -- B -- C
```

#### Weighted Graph:
A **weighted graph** associates a numerical value (weight) with each edge. The weight might represent distance, time, cost, or any other metric.

**Example:**

```
A --5-- B
 |      |
 3      2
 |      |
 C --7-- D
```

In the above weighted graph, the numbers on the edges represent weights. For example, the weight between `A` and `B` is 5, and between `A` and `C` is 3.

---

## Graph Representation

There are two popular ways to represent graphs in computer memory: using an adjacency matrix or an adjacency list.

### Adjacency Matrix

An **adjacency matrix** is a 2D array where each element represents the presence (or weight) of an edge between two vertices. For an unweighted graph, we can represent edges using `0` (no edge) and `1` (edge exists). For weighted graphs, the edge weight can be stored in the matrix.

#### Example:

Consider the following graph:

```
A -- B -- C
     |
     D
```

Vertices: `A = 0`, `B = 1`, `C = 2`, `D = 3`

Adjacency matrix (unweighted):
```
   A  B  C  D
A  0  1  0  0
B  1  0  1  1
C  0  1  0  0
D  0  1  0  0
```

In this matrix:
- The value at `[0][1]` is `1`, representing the edge between `A` and `B`.
- The value at `[1][3]` is `1`, representing the edge between `B` and `D`.

For a **weighted graph**, the adjacency matrix contains weights instead of `1` for edges.

#### Python Implementation:

```python
# Adjacency Matrix representation
graph = [
    [0, 1, 0, 0],  # A
    [1, 0, 1, 1],  # B
    [0, 1, 0, 0],  # C
    [0, 1, 0, 0]   # D
]

# Access the edge between A and B (graph[0][1])
print("Edge between A and B exists:", graph[0][1] == 1)
```

### Adjacency List

An **adjacency list** is a collection of lists where each vertex has a list of the vertices it is connected to. This representation is more space-efficient than the adjacency matrix, especially for sparse graphs.

#### Example:

Consider the same graph:

```
A -- B -- C
     |
     D
```

Adjacency list representation:

```
A: [B]
B: [A, C, D]
C: [B]
D: [B]
```

In the adjacency list:
- Vertex `A` is connected to `B`.
- Vertex `B` is connected to `A`, `C`, and `D`.

#### Python Implementation:

```python
# Adjacency List representation
graph = {
    'A': ['B'],
    'B': ['A', 'C', 'D'],
    'C': ['B'],
    'D': ['B']
}

# Access the neighbors of vertex B
print("Neighbors of B:", graph['B'])
```

### Comparison Between Adjacency Matrix and Adjacency List

| Feature                | Adjacency Matrix                      | Adjacency List                      |
|------------------------|---------------------------------------|-------------------------------------|
| Space Complexity        | O(V²), where V is the number of vertices | O(V + E), where E is the number of edges |
| Suitable For            | Dense graphs (many edges)             | Sparse graphs (few edges)           |
| Edge Lookup Time        | O(1)                                  | O(V) in the worst case              |
| Iterating Over Neighbors| O(V)                                  | O(k), where k is the number of neighbors |

---

## Conclusion

Graphs are incredibly powerful data structures used to represent complex relationships and connections. They can be directed or undirected, weighted or unweighted, and are represented in memory using adjacency matrices or adjacency lists. Understanding the basics of graph representation and operations is crucial for solving problems related to networks, maps, and optimization in computer science.
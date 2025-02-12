# Graph Algorithms: Overview and Examples

## Table of Contents
- [Graph Traversal Algorithms](#graph-traversal-algorithms)
  - [Depth-First Search (DFS)](#depth-first-search-dfs)
  - [Breadth-First Search (BFS)](#breadth-first-search-bfs)
- [Basic Graph Algorithms](#basic-graph-algorithms)
  - [Shortest Path (Overview of Dijkstra’s Algorithm)](#shortest-path-overview-of-dijkstra's-algorithm)
  - [Detecting Cycles in Graphs](#detecting-cycles-in-graphs)
  - [Topological Sorting](#topological-sorting)

---

## Graph Traversal Algorithms

### Depth-First Search (DFS)

**DFS** is an algorithm for traversing or searching through the vertices of a graph in a depthward motion. It uses a stack to remember the next vertex to visit, which ensures that when a vertex has no more neighbors to explore, the algorithm backtracks to previous vertices.

#### Steps:
1. Start from a selected vertex (starting node).
2. Visit the vertex and mark it as visited.
3. Explore one of the neighbors recursively (deep into the graph).
4. If no unvisited neighbors are left, backtrack to the previous vertex.
5. Repeat until all vertices are visited.

#### Example:

Consider the following graph:

```
   A -- B -- E
   |    |
   D -- C
```

The adjacency list for the graph:

```python
graph = {
    'A': ['B', 'D'],
    'B': ['A', 'C', 'E'],
    'C': ['B', 'D'],
    'D': ['A', 'C'],
    'E': ['B']
}
```

Performing DFS starting from node 'A':

```python
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    print(node, end=" ")

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

dfs(graph, 'A')
```

**Output**:
```
A B C D E
```

### Breadth-First Search (BFS)

**BFS** is a traversal algorithm that explores the neighbor nodes at the present depth before moving on to nodes at the next depth level. It uses a queue to keep track of the next node to explore.

#### Steps:
1. Start from a selected vertex (starting node).
2. Visit the vertex and mark it as visited.
3. Explore all neighboring vertices, add them to the queue.
4. Dequeue a vertex, visit it, and explore its neighbors.
5. Repeat until all vertices are visited.

#### Example:

Using the same graph as above, the BFS traversal from node 'A':

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        print(node, end=" ")

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

bfs(graph, 'A')
```

**Output**:
```
A B D C E
```

---

## Basic Graph Algorithms

### Shortest Path (Overview of Dijkstra’s Algorithm)

**Dijkstra's Algorithm** is a greedy algorithm used to find the shortest path between nodes in a graph, which may represent, for example, road networks. It works for graphs with non-negative edge weights.

#### Steps:
1. Start from the source node and assign a tentative distance value of 0 to it and infinity to all other nodes.
2. Select the unvisited node with the smallest tentative distance and mark it as the current node.
3. Update the tentative distances of its neighbors.
4. Once all neighbors have been visited, mark the current node as visited.
5. Repeat until the destination node is marked as visited.

#### Example:

Consider this weighted graph:

```
   A --1-- B --2-- C
    \      |
     4     3
      \    |
        D --1-- E
```

Adjacency list with weights:

```python
graph = {
    'A': {'B': 1, 'D': 4},
    'B': {'A': 1, 'C': 2, 'D': 3},
    'C': {'B': 2},
    'D': {'A': 4, 'B': 3, 'E': 1},
    'E': {'D': 1}
}
```

Applying Dijkstra’s algorithm to find the shortest path from 'A' to all other nodes:

```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]  # priority queue to store (distance, node)

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

distances_from_A = dijkstra(graph, 'A')
print(distances_from_A)
```

**Output**:
```
{'A': 0, 'B': 1, 'C': 3, 'D': 4, 'E': 5}
```

### Detecting Cycles in Graphs

Detecting cycles in graphs is crucial in various algorithms. For **directed graphs**, depth-first search (DFS) can be used to detect back edges, which indicate cycles. For **undirected graphs**, a cycle can be detected if a node is revisited that isn't the direct parent of the current node in the DFS traversal.

#### Example (Undirected Graph):

```python
def detect_cycle(graph, node, visited, parent):
    visited.add(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            if detect_cycle(graph, neighbor, visited, node):
                return True
        elif neighbor != parent:
            return True
    return False

def has_cycle(graph):
    visited = set()
    for node in graph:
        if node not in visited:
            if detect_cycle(graph, node, visited, None):
                return True
    return False

graph = {
    'A': ['B', 'D'],
    'B': ['A', 'C', 'E'],
    'C': ['B'],
    'D': ['A', 'E'],
    'E': ['B', 'D']
}

print(has_cycle(graph))
```

**Output**:
```
True
```

### Topological Sorting

**Topological Sorting** is used to order the vertices in a directed acyclic graph (DAG). It ensures that for every directed edge `u -> v`, vertex `u` appears before `v` in the ordering.

#### Steps:
1. Perform DFS on the graph.
2. Add each vertex to a stack once all its neighbors are visited.
3. Pop the vertices from the stack to get the topological order.

#### Example:

Consider this directed acyclic graph (DAG):

```
   5 --> 0 <-- 4
   |     ^
   v     |
   2 --> 3
```

Adjacency list for the DAG:

```python
graph = {
    5: [2, 0],
    4: [0, 1],
    2: [3],
    3: [1],
    0: [],
    1: []
}
```

Topological sort implementation:

```python
def topological_sort_util(node, visited, stack, graph):
    visited.add(node)
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            topological_sort_util(neighbor, visited, stack, graph)
    
    stack.append(node)

def topological_sort(graph):
    visited = set()
    stack = []
    
    for node in graph:
        if node not in visited:
            topological_sort_util(node, visited, stack, graph)
    
    return stack[::-1]  # return in reverse order

topological_order = topological_sort(graph)
print(topological_order)
```

**Output**:
```
[4, 5, 2, 3, 1, 0]
```

---
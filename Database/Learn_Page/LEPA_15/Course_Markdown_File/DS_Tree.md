# Trees

## Table of Contents
1. [Introduction to Trees](#introduction-to-trees)
   1. [Basic Terminology](#basic-terminology)
   2. [Properties of Trees](#properties-of-trees)
2. [Types of Trees](#types-of-trees)
   1. [Binary Trees](#binary-trees)
   2. [Binary Search Trees (BST)](#binary-search-trees-bst)
   3. [AVL Trees (Basic Introduction)](#avl-trees-basic-introduction)
   4. [Other Balanced Trees (Red-Black Trees Overview)](#other-balanced-trees-red-black-trees-overview)

---

## Introduction to Trees

A **tree** is a hierarchical data structure that consists of nodes connected by edges. It is widely used to represent hierarchical relationships such as family trees, file systems, and organizational structures. Trees are non-linear and can have multiple levels of nodes.

### Basic Terminology

Understanding basic tree terminology is essential for working with trees:

- **Node**: A node represents a value or data point. Each node in a tree can have child nodes.
- **Edge**: An edge is a link between two nodes, representing the parent-child relationship.
- **Root**: The root is the topmost node in a tree, which has no parent.
- **Leaf**: A leaf is a node with no children, i.e., it is the end point of a branch in the tree.
- **Parent**: A parent node is one that has child nodes connected to it.
- **Child**: A child node is one that descends from a parent node.
- **Subtree**: A subtree is a portion of the larger tree, which itself is a tree.
- **Depth**: The depth of a node is the number of edges from the root to that node.
- **Height**: The height of a tree is the number of edges on the longest path from the root to a leaf.
  
#### Example of a Tree Structure:
```plaintext
          A
         / \
        B   C
       / \   \
      D   E   F
```

In this tree:
- Node A is the root.
- Nodes D, E, and F are leaves.
- Node B is the parent of nodes D and E.

### Properties of Trees

- **Connectedness**: A tree is a connected graph, meaning there is a path between any two nodes.
- **Acyclic**: A tree has no cycles, which means you cannot return to the starting node by following edges.
- **n-1 Edges**: A tree with `n` nodes has exactly `n-1` edges.
- **Hierarchy**: Trees represent hierarchical structures where one element is the parent of others.

---

## Types of Trees

There are many types of trees, each designed for specific operations or use cases. Below are some common types of trees.

### Binary Trees

A **binary tree** is a type of tree where each node can have at most two children, often referred to as the left and right children.

#### Properties of Binary Trees:
- **At most two children per node**.
- The left child typically contains values smaller than the parent, while the right child contains values larger than the parent (in Binary Search Trees).

#### Example:

```plaintext
        1
       / \
      2   3
     / \
    4   5
```

In this binary tree:
- Node 1 is the root.
- Node 2 is the left child of node 1, and node 3 is the right child.
- Nodes 4 and 5 are the children of node 2.

#### Common Operations:
- **Traversal**: Pre-order, In-order, Post-order
- **Insertion and Deletion**: Insert elements as per the binary tree property.

#### Example (In-order Traversal):

```python
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

# In-order traversal
def in_order_traversal(root):
    if root:
        in_order_traversal(root.left)
        print(root.val, end=" ")
        in_order_traversal(root.right)

# Example usage:
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)

in_order_traversal(root)  # Output: 4 2 5 1 3
```

### Binary Search Trees (BST)

A **Binary Search Tree (BST)** is a binary tree that follows specific ordering rules. Each node's left subtree contains values less than the node's key, and the right subtree contains values greater than the node's key.

#### Properties:
- **Left subtree contains smaller values**.
- **Right subtree contains larger values**.
- Efficient for searching, inserting, and deleting nodes.

#### Example:

```plaintext
        15
       /  \
      10   20
     /  \    \
    8   12    25
```

In this BST:
- Node 10 is smaller than the root (15), so it's placed in the left subtree.
- Node 20 is larger than 15, so it's placed in the right subtree.

#### Common Operations:
- **Search**: O(log n) time complexity for balanced trees.
- **Insertion**: Insert based on comparison with parent nodes.

#### Example (Search Operation):

```python
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

# Search function in BST
def search(root, key):
    if root is None or root.val == key:
        return root
    if key < root.val:
        return search(root.left, key)
    return search(root.right, key)

# Example usage:
root = Node(15)
root.left = Node(10)
root.right = Node(20)
root.left.left = Node(8)
root.left.right = Node(12)

result = search(root, 12)
print(result.val if result else "Not found")  # Output: 12
```

### AVL Trees (Basic Introduction)

An **AVL Tree** is a self-balancing binary search tree where the heights of the left and right subtrees of any node differ by no more than one.

#### Properties:
- **Self-balancing**: After every insertion or deletion, the tree checks the balance factor and rebalances itself if needed.
- **Efficient operations**: Search, insertion, and deletion are all O(log n) due to balancing.

#### Balancing Example:

```plaintext
        30
       /  \
      20   40
     /
    10
```

After inserting 10 into the tree, it may become unbalanced. Rotations are used to restore balance.

#### Example (Simple AVL Insertion):

```python
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        self.height = 1

# Insert and balance function (simplified)
def insert(root, key):
    # Perform normal BST insert
    if not root:
        return Node(key)
    if key < root.val:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)

    # Update height of the ancestor node
    root.height = 1 + max(height(root.left), height(root.right))

    # Balance the node (simple cases handled here)
    balance_factor = height(root.left) - height(root.right)
    if balance_factor > 1:
        # Perform rotations
        pass  # Simplified for example

    return root

def height(node):
    if not node:
        return 0
    return node.height
```

### Other Balanced Trees (Red-Black Trees Overview)

A **Red-Black Tree** is another type of self-balancing binary search tree, but it uses additional color properties (red or black) to ensure balance.

#### Properties:
- **Each node is either red or black**.
- **The root and leaves are black**.
- **Red nodes cannot have red children**.
- **Every path from a node to its descendant leaves contains the same number of black nodes**.

#### Example of Red-Black Tree:

```plaintext
       10 (Black)
      /    \
   5 (Red)  15 (Black)
```

In this tree:
- The root (10) is black.
- Node 5 is red, and it cannot have red children.
- The number of black nodes on both sides is equal.

Red-Black Trees ensure that operations like search, insert, and delete remain O(log n) by maintaining balance through color-changing and rotations.

---

Trees are one of the most fundamental data structures in computer science, used to model hierarchical data efficiently. Various types of trees offer different properties and performance optimizations depending on the use case.
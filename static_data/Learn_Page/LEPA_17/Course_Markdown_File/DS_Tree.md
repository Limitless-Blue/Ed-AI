# Operations on Trees

## Table of Contents
1. [Insertion](#insertion)
2. [Deletion](#deletion)
3. [Searching for Elements](#searching-for-elements)
4. [Balancing Trees](#balancing-trees)

## Operations on Trees

Tree data structures support a variety of operations that are essential for manipulating and accessing the stored data efficiently. Common operations include insertion, deletion, searching, and balancing the tree.

### Insertion

Insertion in a binary tree depends on the specific type of tree. For a Binary Search Tree (BST), the insertion operation follows specific rules to ensure the properties of the tree remain intact.

- If the value to be inserted is less than the current node, insert it in the left subtree.
- If the value to be inserted is greater than the current node, insert it in the right subtree.

**Example:**

Consider an empty BST. Insert the following values in this order: `10, 5, 15, 3, 7, 12, 17`.

The resulting tree will look like this:

```
        10
       /  \
      5   15
     / \   / \
    3   7 12 17
```

**Implementation in Python:**

```python
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    if root is None:
        return Node(key)
    
    if key < root.val:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    
    return root

# Example usage:
root = None
values = [10, 5, 15, 3, 7, 12, 17]
for value in values:
    root = insert(root, value)
```

### Deletion

Deletion in a binary tree is more complex than insertion, as it involves three possible scenarios:

1. **Node with no children (leaf node)**: Simply remove the node.
2. **Node with one child**: Remove the node and replace it with its child.
3. **Node with two children**: Find the node's in-order successor (smallest node in the right subtree) or in-order predecessor (largest node in the left subtree), replace the node with that value, and delete the successor or predecessor.

**Example:**

Consider the following BST:

```
        10
       /  \
      5   15
     / \   / \
    3   7 12 17
```

If we delete `15`, its in-order successor is `17`. We replace `15` with `17`, resulting in:

```
        10
       /  \
      5   17
     / \   /
    3   7 12
```

**Implementation in Python:**

```python
def delete(root, key):
    if root is None:
        return root
    
    if key < root.val:
        root.left = delete(root.left, key)
    elif key > root.val:
        root.right = delete(root.right, key)
    else:
        # Node with one child or no child
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        
        # Node with two children
        temp = min_value_node(root.right)
        root.val = temp.val
        root.right = delete(root.right, temp.val)
    
    return root

def min_value_node(node):
    current = node
    while current.left is not None:
        current = current.left
    return current

# Example usage:
root = delete(root, 15)
```

### Searching for Elements

Searching in a binary tree, particularly a Binary Search Tree (BST), can be performed efficiently due to its structure. In a BST, the left child is smaller than the parent node, and the right child is larger than the parent node.

- If the value to be searched is less than the current node, search the left subtree.
- If the value to be searched is greater than the current node, search the right subtree.
- If the value matches the current node, the search is successful.

**Example:**

Consider the following BST:

```
        10
       /  \
      5   15
     / \   / \
    3   7 12 17
```

To search for `7`, start at the root and go left to `5`, then right to `7`, and the search is successful.

**Implementation in Python:**

```python
def search(root, key):
    if root is None or root.val == key:
        return root
    
    if key < root.val:
        return search(root.left, key)
    
    return search(root.right, key)

# Example usage:
found = search(root, 7)
if found:
    print(f"Element {found.val} found in the tree.")
else:
    print("Element not found.")
```

### Balancing Trees

Balancing a tree is crucial to maintain its efficiency. An unbalanced tree can degenerate into a linked list, making operations like search, insertion, and deletion take linear time. Self-balancing binary search trees like AVL trees and Red-Black trees ensure that the tree remains balanced after every insertion and deletion.

- **AVL Tree**: An AVL tree is a self-balancing binary search tree where the difference between the heights of left and right subtrees cannot be more than one for all nodes.
- **Red-Black Tree**: A Red-Black tree is another self-balancing binary search tree where nodes are colored either red or black, and the tree maintains specific rules about the color distribution to ensure balance.

#### AVL Tree Example:

Insertion in an AVL tree works similarly to a BST, but after every insertion, the tree checks for balance. If the tree becomes unbalanced, it performs rotations to restore balance.

**Rotations:**
- **Left Rotation**: Performed when a node’s right child is heavier than its left child.
- **Right Rotation**: Performed when a node’s left child is heavier than its right child.

**Example (Before balancing):**

```
        30
       /  \
      20   40
     /
    10
```

After inserting `5`, the tree becomes unbalanced. A right rotation on node `20` restores balance:

```
        30
       /  \
      10   40
       \
       20
```

**Implementation of AVL Tree Insertion:**

```python
class AVLNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        self.height = 1

def insert_avl(root, key):
    if root is None:
        return AVLNode(key)
    
    if key < root.val:
        root.left = insert_avl(root.left, key)
    else:
        root.right = insert_avl(root.right, key)

    root.height = 1 + max(get_height(root.left), get_height(root.right))

    balance = get_balance(root)
    
    if balance > 1 and key < root.left.val:
        return right_rotate(root)
    if balance < -1 and key > root.right.val:
        return left_rotate(root)
    if balance > 1 and key > root.left.val:
        root.left = left_rotate(root.left)
        return right_rotate(root)
    if balance < -1 and key < root.right.val:
        root.right = right_rotate(root.right)
        return left_rotate(root)
    
    return root

def left_rotate(z):
    y = z.right
    T2 = y.left
    y.left = z
    z.right = T2
    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y

def right_rotate(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x

def get_height(node):
    if not node:
        return 0
    return node.height

def get_balance(node):
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)
```

## Conclusion

Understanding and implementing operations such as insertion, deletion, searching, and balancing trees are fundamental to working with tree data structures. Efficient manipulation of trees ensures better performance in a wide range of applications.
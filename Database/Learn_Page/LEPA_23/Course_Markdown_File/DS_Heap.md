# Heaps in Data Structures

## Table of Contents
- [Introduction to Heaps](#introduction-to-heaps)
- [Heap Operations](#heap-operations)
  - [Insertion](#insertion)
  - [Deletion (Extract Max/Min)](#deletion-extract-maxmin)
  - [Peek/Top Element](#peektop-element)
- [Implementing Heaps](#implementing-heaps)
  - [Using Arrays](#using-arrays)
  - [Heapify Process](#heapify-process)

---

## Introduction to Heaps

A **heap** is a specialized tree-based data structure that satisfies the heap property. There are two main types of heaps:

1. **Max Heap**: The value of each parent node is greater than or equal to the values of its children. The highest value is at the root.
2. **Min Heap**: The value of each parent node is less than or equal to the values of its children. The lowest value is at the root.

Heaps are often implemented using binary trees, and they are commonly used in priority queues and sorting algorithms (like heapsort).

---

## Heap Operations

### Insertion

Inserting an element into a heap involves adding the element to the end of the heap and then "bubbling up" to restore the heap property. 

**Steps for Insertion**:
1. Add the new element at the end of the heap (complete binary tree).
2. Compare the added element with its parent; if it violates the heap property, swap them.
3. Repeat step 2 until the heap property is restored or the element reaches the root.

**Example**:
```plaintext
Initial Max Heap:
        10
       /  \
      8    9
     / \  /
    6  7 5

Insert 11:
        10
       /  \
      8    9
     / \  / \
    6  7 5  11
Bubble Up 11:
        10
       /  \
      11   9
     / \  /
    8  7 5
   /
  6
```

### Deletion (Extract Max/Min)

The process of deleting an element from a heap typically involves removing the root element (maximum for max heaps, minimum for min heaps) and then "bubbling down" to restore the heap property.

**Steps for Deletion**:
1. Replace the root element with the last element in the heap.
2. Remove the last element.
3. Compare the new root with its children; if it violates the heap property, swap it with the larger (max heap) or smaller (min heap) of the two children.
4. Repeat step 3 until the heap property is restored or the element reaches a leaf.

**Example**:
```plaintext
Initial Max Heap:
        10
       /  \
      8    9
     / \  /
    6  7 5

Delete Max (10):
Replace 10 with 5:
        5
       /  \
      8    9
     / \  /
    6  7

Bubble Down 5:
        8
       /  \
      5    9
     / \  /
    6  7
```

### Peek/Top Element

The **peek** operation retrieves the top element of the heap without removing it. For a max heap, this is the maximum element; for a min heap, it is the minimum element. 

**Example**:
```plaintext
Max Heap:
        10
       /  \
      8    9
     / \  /
    6  7 5

Peek:
Result: 10 (the root of the max heap)
```

---

## Implementing Heaps

### Using Arrays

Heaps can be efficiently implemented using arrays. The array representation allows us to take advantage of the properties of complete binary trees.

**Array Representation**:
- For a node at index `i`:
  - The left child is at index `2i + 1`
  - The right child is at index `2i + 2`
  - The parent is at index `(i - 1) / 2` (integer division)

**Example**:
A max heap represented as an array:
```plaintext
Array: [10, 8, 9, 6, 7, 5]
```
This array corresponds to the following tree structure:
```plaintext
        10
       /  \
      8    9
     / \  /
    6  7 5
```

### Heapify Process

The **heapify** process converts a binary tree into a heap. This is useful for building a heap from an arbitrary collection of elements.

**Heapify Steps**:
1. Start from the last non-leaf node and move upwards to the root.
2. For each node, ensure the subtree rooted at that node satisfies the heap property by performing bubble down operations.

**Example**:
Consider the following array: `[3, 9, 2, 1, 4]`

1. Start from index 1 (last non-leaf node):
   - Compare with children: `9` and `2` (max heap property).
   - No changes needed.

2. Move to index 0:
   - Compare with children: `3` and `9`.
   - Swap `3` and `9`.
   
Heapified Array: `[9, 4, 2, 1, 3]` which represents the following max heap:
```plaintext
        9
       / \
      4   2
     / \
    1   3
```

---

## Conclusion

Heaps are powerful data structures that provide efficient ways to manage priority information. Understanding heap operations, their implementation, and the heapify process is crucial for leveraging their capabilities in algorithms such as heapsort and priority queues.

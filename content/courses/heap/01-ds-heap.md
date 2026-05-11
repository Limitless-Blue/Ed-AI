# Heaps

## Table of Contents
1. [Introduction to Heaps](#introduction-to-heaps)
   - [Definition and Properties](#definition-and-properties)
   - [Types of Heaps](#types-of-heaps)
     - [Max Heap](#max-heap)
     - [Min Heap](#min-heap)
   - [Heap Properties](#heap-properties)
2. [Difference Between Max Heap and Min Heap](#difference-between-max-heap-and-min-heap)
   - [Comparison Table](#comparison-table)
3. [Heap Operations](#heap-operations)
   - [Insertion](#insertion)
   - [Deletion](#deletion)
   - [Heapify](#heapify)
4. [Applications of Heaps](#applications-of-heaps)
5. [Conclusion](#conclusion)

---

## Introduction to Heaps

Heaps are specialized tree-based data structures that satisfy the heap property, which makes them suitable for implementing priority queues and various algorithms such as heapsort. They can be represented as binary trees and are efficient in both time and space.

### Definition and Properties

A **heap** is defined as a complete binary tree that maintains a specific order:

- **Max Heap**: In a max heap, for every node `N`, the value of `N` is greater than or equal to the values of its children. This means that the maximum element is always located at the root of the tree.
  
  ![Max Heap Example](https://i.imgur.com/XpW9mg0.png)

- **Min Heap**: In a min heap, for every node `N`, the value of `N` is less than or equal to the values of its children. Thus, the minimum element is always at the root.

  ![Min Heap Example](https://i.imgur.com/GP3gGR9.png)

### Types of Heaps

Heaps can be classified into two main types based on the heap property they follow:

#### Max Heap

- **Definition**: In a max heap, every parent node has a value greater than or equal to that of its children.
- **Example**:
  
  ```
          10
        /    \
       9      8
      / \    / \
     7   6  5   4
  ```
  
- **Array Representation**: The above max heap can be represented as an array: `[10, 9, 8, 7, 6, 5, 4]`.

#### Min Heap

- **Definition**: In a min heap, every parent node has a value less than or equal to that of its children.
- **Example**:
  
  ```
          1
        /   \
       3     2
      / \   / \
     5   6 7   8
  ```
  
- **Array Representation**: The above min heap can be represented as an array: `[1, 3, 2, 5, 6, 7, 8]`.

### Heap Properties

1. **Complete Binary Tree**: Heaps are always complete binary trees. This means all levels of the tree are fully filled except possibly for the last level, which is filled from left to right.
  
2. **Heap Order Property**: 
   - In a max heap, each parent node's key is greater than or equal to the keys of its children.
   - In a min heap, each parent node's key is less than or equal to the keys of its children.

3. **Efficient Operations**: Heaps allow efficient insertion, deletion, and access to the maximum or minimum element, typically with:
   - Insertion: O(log n)
   - Deletion: O(log n)
   - Accessing Max/Min: O(1)

---

## Difference Between Max Heap and Min Heap

### Comparison Table

| Feature              | Max Heap                               | Min Heap                               |
|----------------------|----------------------------------------|----------------------------------------|
| **Root Element**     | Maximum value at the root              | Minimum value at the root              |
| **Heap Order**       | Parent node >= Child nodes             | Parent node <= Child nodes             |
| **Use Cases**        | Priority queues (highest priority first), heapsort | Priority queues (lowest priority first), heapsort |
| **Insertion**        | Added at the end and "bubbled up"     | Added at the end and "bubbled up"     |
| **Deletion**         | Remove the root and "bubble down"     | Remove the root and "bubble down"     |

---

## Heap Operations

### Insertion

Inserting a new element into a heap involves the following steps:

1. **Add the Element**: Insert the new element at the end of the heap (complete binary tree property).
2. **Heapify Up (Bubble Up)**: Compare the inserted element with its parent; if it violates the heap property, swap it with the parent. Repeat this process until the heap property is restored.

#### Example of Insertion

For a max heap with initial array `[10, 9, 8, 7]`, if we insert `11`:

1. Add `11` at the end: `[10, 9, 8, 7, 11]`
2. Compare with parent `9`, since `11 > 9`, swap them: `[10, 11, 8, 7, 9]`
3. Compare with parent `10`, since `11 > 10`, swap them: `[11, 10, 8, 7, 9]`

The final heap after insertion is:

```
       11
      /  \
    10    8
   /  \
  7    9
```

### Deletion

To delete the root element from a heap (which is either the maximum or minimum):

1. **Replace the Root**: Replace the root with the last element in the heap (the rightmost leaf).
2. **Heapify Down (Bubble Down)**: Compare the new root with its children; if it violates the heap property, swap it with the larger (or smaller for min heaps) child. Repeat until the heap property is restored.

#### Example of Deletion

For a max heap represented as `[11, 10, 8, 7, 9]`, removing the root (`11`):

1. Replace root with last element `9`: `[9, 10, 8, 7]`
2. Compare `9` with children `10` and `8`. Swap `9` with `10` (larger child): `[10, 9, 8, 7]`
3. No further swaps needed as the heap property is restored.

The final heap after deletion is:

```
       10
      /  \
     9    8
    /
   7
```

### Heapify

Heapify is the process of converting a binary tree into a heap. The algorithm can be applied recursively or iteratively.

#### Example of Heapify

Consider an array `[3, 5, 1, 8, 2]`. To convert it into a max heap:

1. Start from the last non-leaf node and move upwards, applying the bubble down operation.
2. For index 1 (`5`):
   - Compare with children `8` and `2`. Swap with `8`.
3. Move to index 0 (`3`):
   - Compare with children `5` and `1`. Swap with `5`.
4. Final max heap: `[8, 5, 1, 3, 2]`.

---

## Applications of Heaps

1. **Priority Queues**: Heaps are used to implement priority queues, allowing efficient retrieval of the highest (or lowest) priority item.
  
2. **Heapsort**: Heaps can be utilized in the heapsort algorithm, which sorts an array in O(n log n) time by building a max heap and repeatedly extracting the maximum element.

3. **Graph Algorithms**: Algorithms such as Dijkstra's and Prim's use heaps to efficiently retrieve the minimum distance node.

4. **Load Balancing**: Heaps can help in load balancing tasks in systems by prioritizing certain tasks over others.

---

## Conclusion

Heaps are a powerful data structure that provides efficient methods for priority management and sorting. Understanding the differences between max heaps and min heaps, as well as their operations, is crucial for implementing effective algorithms. With their complete binary tree structure and logarithmic time complexity for insertion and deletion, heaps serve as a fundamental tool in various applications in computer science.
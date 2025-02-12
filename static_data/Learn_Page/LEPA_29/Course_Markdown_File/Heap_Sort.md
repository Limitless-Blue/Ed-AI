# Heap Sort

## Table of Contents
1. [Basics of Heap Data Structure](#basics-of-heap-data-structure)
2. [Building a Heap](#building-a-heap)
3. [Implementation of Heap Sort](#implementation-of-heap-sort)
4. [Time and Space Complexity](#time-and-space-complexity)

---

## 1. Basics of Heap Data Structure

A **Heap** is a special type of **binary tree** that satisfies the **heap property**:
- **Max-Heap**: The key at the root is greater than or equal to the keys of its children. This ensures the largest element is at the root.
- **Min-Heap**: The key at the root is less than or equal to the keys of its children. This ensures the smallest element is at the root.

### Characteristics of a Heap:
- A heap is a **complete binary tree**, meaning all levels are filled except possibly the last one, which is filled from left to right.
- **Heap property** ensures efficient retrieval of the maximum (in max-heap) or minimum (in min-heap) element.

### Applications of Heaps:
- **Priority Queue**: Heaps are commonly used to implement priority queues because of their efficient insertion and extraction of the minimum or maximum element.
- **Heap Sort**: Heaps are used in Heap Sort to efficiently sort elements.

---

## 2. Building a Heap

Building a heap can be done using an array representation of a binary tree. We can build a max-heap or min-heap from an unsorted array using the **heapify** process.

### Heapify Process:
1. For a given node, compare it with its children.
2. If it violates the heap property, swap it with the largest (for max-heap) or smallest (for min-heap) of its children.
3. Recursively apply heapify to the affected subtree.

### Example:
Consider the array `[3, 5, 1, 10, 2, 7]`. To build a max-heap:
- Start from the first non-leaf node (index 2, value 1).
- Apply heapify to create a max-heap:
  - Swap 1 with 7: `[3, 5, 7, 10, 2, 1]`
  - Then apply heapify to index 1 (value 5), and so on until the entire array satisfies the heap property.

### Building a Heap in Linear Time:
Building a heap takes **O(n)** time. This is because each level of the tree is heapified in decreasing order, and the number of nodes at each level decreases geometrically.

---

## 3. Implementation of Heap Sort

Heap Sort is an efficient comparison-based sorting algorithm that leverages the heap data structure to sort elements in **O(n log n)** time. It works by:
1. Building a max-heap from the input array.
2. Repeatedly extracting the maximum element (root of the heap) and placing it at the end of the array.
3. Reducing the heap size and heapifying the remaining elements.

### Python Code for Heap Sort

```python
# Function to heapify the tree
def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    left = 2 * i + 1  # left child
    right = 2 * i + 2  # right child

    # If left child is larger than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # If right child is larger than largest so far
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If largest is not root
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Swap
        heapify(arr, n, largest)  # Recursively heapify the affected subtree

# Function to perform heap sort
def heap_sort(arr):
    n = len(arr)

    # Build a max-heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap
        heapify(arr, i, 0)  # Heapify the root element

# Example usage
arr = [3, 5, 1, 10, 2, 7]
heap_sort(arr)
print(f"Sorted array: {arr}")
```

### Explanation:
- **Heapify** function ensures that the subtree rooted at the index `i` satisfies the heap property.
- **Heap Sort** first builds a max-heap and then repeatedly swaps the root with the last element in the heap and reduces the heap size by one. After each swap, it re-heapifies the remaining elements.

---

## 4. Time and Space Complexity

### Time Complexity:
- **Building the heap**: O(n). This is because, while heapifying each node takes O(log n) time, the number of nodes at each level decreases as you go deeper into the tree, resulting in an overall linear time for building the heap.
- **Extracting elements and heapifying**: O(n log n). Each extraction involves swapping the root with the last element and then heapifying, which takes O(log n) time. This is repeated for all n elements, giving a time complexity of O(n log n).

### Overall Time Complexity: O(n log n)

### Space Complexity:
- **In-place sorting**: The algorithm sorts the array in place, requiring only a constant amount of extra space for temporary variables.
- **Space Complexity**: O(1) auxiliary space, as heap sort uses only a few extra variables and modifies the input array directly.

---

## Conclusion
Heap Sort is a highly efficient sorting algorithm that leverages the heap data structure to achieve an overall time complexity of **O(n log n)**. It is particularly useful when you need an in-place sorting algorithm that avoids the worst-case time complexities of other algorithms like Quick Sort. However, it is typically slower than Quick Sort in practice due to the overhead of maintaining the heap structure.

# Quick Sort

## Table of Contents
1. [Introduction to Quick Sort](#introduction-to-quick-sort)
2. [Partitioning Process](#partitioning-process)
3. [Implementation in Code](#implementation-in-code)
4. [Best and Worst Case Scenarios](#best-and-worst-case-scenarios)

---

## 1. Introduction to Quick Sort

**Quick Sort** is a highly efficient sorting algorithm that uses the **Divide and Conquer** approach to sort elements. It is an in-place sorting algorithm, meaning it requires a small amount of extra memory space. It is widely used due to its **average-case time complexity** of **O(n log n)**.

Quick Sort works by selecting a **pivot** element from the array and partitioning the other elements into two subarrays:
- One with elements less than the pivot,
- One with elements greater than the pivot.

The process is repeated recursively for both subarrays until the base case is reached (i.e., subarrays of size 1 or 0).

### Key Characteristics:
- **In-place** sorting algorithm.
- **Unstable** (the relative order of equal elements is not preserved).
- **Average-case time complexity**: O(n log n).
- **Worst-case time complexity**: O(n²).
- **Space complexity**: O(log n) due to recursion.

---

## 2. Partitioning Process

The **Partitioning Process** is the key to Quick Sort. The goal is to rearrange the array such that:
1. All elements less than the pivot are moved to the left.
2. All elements greater than the pivot are moved to the right.
3. The pivot element is placed in its correct position.

There are two common ways to implement the partitioning process:
- **Lomuto Partition Scheme**: It always chooses the last element as the pivot.
- **Hoare Partition Scheme**: It uses two indices that move toward each other, stopping when they detect an inversion.

### Example: Lomuto Partitioning

Consider the array: `[10, 80, 30, 90, 40, 50, 70]`.

Steps for partitioning:
1. Choose the pivot (last element): 70.
2. Rearrange elements:
   - Move elements less than 70 to the left.
   - Move elements greater than 70 to the right.
3. After rearrangement, the array looks like: `[10, 30, 40, 50, 70, 90, 80]`.

Now, 70 is in its correct sorted position. Quick Sort will recursively sort the left (`[10, 30, 40, 50]`) and right (`[90, 80]`) subarrays.

### Example: Hoare Partitioning

Consider the array: `[10, 80, 30, 90, 40, 50, 70]`.

Steps for Hoare partitioning:
1. Choose a pivot (can be the first or middle element).
2. Start two pointers, `i` from the left and `j` from the right.
3. Increment `i` until an element greater than the pivot is found.
4. Decrement `j` until an element smaller than the pivot is found.
5. Swap the elements at `i` and `j`.
6. Continue this process until the pointers cross.

---

## 3. Implementation in Code

Here is a Python implementation of Quick Sort using the **Lomuto partition scheme**.

### Python Code

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr  # Base case: A single element is already sorted.
    
    pivot = arr[-1]  # Choose the pivot (last element).
    left = [x for x in arr[:-1] if x <= pivot]  # Elements less than or equal to pivot.
    right = [x for x in arr[:-1] if x > pivot]  # Elements greater than pivot.

    # Recursively sort left and right subarrays, then combine.
    return quick_sort(left) + [pivot] + quick_sort(right)

# Example usage:
arr = [10, 80, 30, 90, 40, 50, 70]
sorted_arr = quick_sort(arr)
print(f"Sorted array: {sorted_arr}")
```

### Explanation:
- The array is split into two parts: elements less than or equal to the pivot and elements greater than the pivot.
- The function recursively sorts the left and right parts, then combines them with the pivot.
  
---

## 4. Best and Worst Case Scenarios

### Best Case Scenario
The **best case** for Quick Sort occurs when the pivot divides the array into two nearly equal halves at each step. This results in the most balanced recursion tree, leading to the optimal time complexity of **O(n log n)**.

#### Example (Best Case):
Consider an array that splits evenly at each step:
```
[15, 3, 9, 8, 5, 2, 7, 12]
```
After the first partition, the pivot (7) splits the array into two halves:
```
[3, 2, 5] and [9, 8, 12, 15]
```
Both subarrays are then recursively sorted. Each level of the recursion splits evenly, so the overall time complexity is **O(n log n)**.

### Worst Case Scenario
The **worst case** occurs when the pivot chosen is either the smallest or largest element, resulting in unbalanced partitions. In this case, Quick Sort degenerates into an inefficient **O(n²)** algorithm because the recursion depth is the maximum, and each partition only reduces the problem size by one element.

#### Example (Worst Case):
Consider an already sorted array:
```
[2, 3, 5, 7, 8, 9, 12, 15]
```
If Quick Sort always chooses the last element as the pivot, the array will be partitioned in the most unbalanced way possible, leading to a time complexity of **O(n²)**.

### Avoiding the Worst Case:
To avoid the worst-case scenario, you can:
- **Randomize the pivot selection**: Instead of always selecting the first or last element as the pivot, choose a random element.
- **Use the median-of-three rule**: Choose the pivot as the median of the first, middle, and last elements in the array.

---

## Conclusion
Quick Sort is a powerful and efficient sorting algorithm, especially for larger datasets, due to its average-case time complexity of **O(n log n)**. However, its worst-case performance can be mitigated by selecting pivots more intelligently. Despite being unstable, its in-place sorting capability and flexibility in pivot selection make it a popular choice for many real-world applications.

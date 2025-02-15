# Sorting Algorithms: Bubble Sort

## Table of Contents
1. [Introduction](#introduction)
2. [How Bubble Sort Works](#how-bubble-sort-works)
3. [Step-by-Step Example](#step-by-step-example)
4. [Implementation in Code](#implementation-in-code)
5. [Time and Space Complexity](#time-and-space-complexity)
6. [Conclusion](#conclusion)

## Introduction
Bubble Sort is a simple sorting algorithm that compares adjacent elements in a list and swaps them if they are in the wrong order. This process is repeated until the list is sorted. Despite its simplicity, Bubble Sort is not suitable for large datasets as its average and worst-case time complexity is quite high compared to more advanced sorting algorithms.

## How Bubble Sort Works
Bubble Sort works by repeatedly stepping through the list to be sorted, comparing each pair of adjacent items. If two elements are in the wrong order, they are swapped. The algorithm gets its name because smaller elements "bubble" to the top of the list with each pass. The process continues until the list is sorted.

### Steps:
1. Start at the beginning of the list.
2. Compare the first two adjacent elements.
3. If the first element is greater than the second, swap them.
4. Move to the next pair of adjacent elements and repeat step 3.
5. Continue this process for the entire list.
6. After each pass, the largest unsorted element will have moved to its correct position.
7. Repeat the process for the entire list until no swaps are needed.

## Step-by-Step Example
Let’s consider an example with the following unsorted list:

```
[5, 2, 9, 1, 5, 6]
```

### First Pass:
1. Compare 5 and 2 → swap → `[2, 5, 9, 1, 5, 6]`
2. Compare 5 and 9 → no swap → `[2, 5, 9, 1, 5, 6]`
3. Compare 9 and 1 → swap → `[2, 5, 1, 9, 5, 6]`
4. Compare 9 and 5 → swap → `[2, 5, 1, 5, 9, 6]`
5. Compare 9 and 6 → swap → `[2, 5, 1, 5, 6, 9]`

### Second Pass:
1. Compare 2 and 5 → no swap → `[2, 5, 1, 5, 6, 9]`
2. Compare 5 and 1 → swap → `[2, 1, 5, 5, 6, 9]`
3. Compare 5 and 5 → no swap → `[2, 1, 5, 5, 6, 9]`
4. Compare 5 and 6 → no swap → `[2, 1, 5, 5, 6, 9]`
5. Compare 6 and 9 → no swap → `[2, 1, 5, 5, 6, 9]`

### Third Pass:
1. Compare 2 and 1 → swap → `[1, 2, 5, 5, 6, 9]`
2. Compare 2 and 5 → no swap → `[1, 2, 5, 5, 6, 9]`
3. Compare 5 and 5 → no swap → `[1, 2, 5, 5, 6, 9]`
4. Compare 5 and 6 → no swap → `[1, 2, 5, 5, 6, 9]`
5. Compare 6 and 9 → no swap → `[1, 2, 5, 5, 6, 9]`

At this point, no swaps were made, and the list is sorted.

## Implementation in Code
Here's a simple implementation of Bubble Sort in Python:

```python
def bubble_sort(arr):
    n = len(arr)
    # Traverse through all elements in the array
    for i in range(n):
        # Last i elements are already sorted
        for j in range(0, n-i-1):
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Example usage
unsorted_list = [5, 2, 9, 1, 5, 6]
sorted_list = bubble_sort(unsorted_list)
print("Sorted List:", sorted_list)
```

## Time and Space Complexity
### Time Complexity
- **Best Case:** O(n) - This occurs when the array is already sorted, and only one pass through the array is needed.
- **Average Case:** O(n^2) - On average, Bubble Sort will require about n^2 comparisons and swaps.
- **Worst Case:** O(n^2) - This occurs when the array is sorted in reverse order, requiring the maximum number of swaps.

### Space Complexity
- O(1) - Bubble Sort is an in-place sorting algorithm, meaning it requires only a constant amount of additional space for its operations.

## Conclusion
Bubble Sort is a straightforward and easy-to-understand algorithm that is useful for educational purposes. However, due to its inefficiency for large datasets, it is rarely used in practice compared to more advanced algorithms like Quick Sort or Merge Sort. Understanding Bubble Sort helps in grasping the basic concepts of sorting and algorithm design.
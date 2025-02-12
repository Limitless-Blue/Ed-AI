# Binary Search

## Table of Contents
1. [Introduction to Binary Search](#introduction-to-binary-search)
2. [Preconditions (Sorted Array)](#preconditions-sorted-array)
3. [Step-by-Step Example](#step-by-step-example)
4. [Implementation in Code](#implementation-in-code)
5. [Time Complexity](#time-complexity)

---

## Introduction to Binary Search

Binary search is an efficient search algorithm that finds the position of a target value within a sorted array or list. It works by repeatedly dividing the search interval in half, eliminating half of the potential candidates with each comparison. This algorithm significantly reduces the number of comparisons needed to find a target compared to linear search, especially for large datasets.

---

## Preconditions (Sorted Array)

For binary search to work effectively, the following preconditions must be met:

1. **Sorted Array:** The array or list must be sorted in ascending (or descending) order. Binary search cannot be applied to unsorted data.
2. **Random Access:** The data structure used must allow for efficient random access to its elements, meaning that the algorithm should be able to access any element in constant time.

---

## Step-by-Step Example

Let's illustrate how binary search works with a step-by-step example.

### Example

Given the following sorted array of integers:

```
array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
```

Let's say we want to find the target value `11`.

**Steps:**

1. **Initial Setup:**
   - Start with two pointers: `low = 0` (first index) and `high = 9` (last index).

2. **First Iteration:**
   - Calculate the mid index: `mid = (low + high) // 2 = (0 + 9) // 2 = 4`.
   - Compare the middle element `array[4] = 9` with the target `11`.
   - Since `9 < 11`, adjust the `low` pointer: `low = mid + 1 = 5`.

3. **Second Iteration:**
   - Recalculate the mid index: `mid = (5 + 9) // 2 = 7`.
   - Compare `array[7] = 15` with the target `11`.
   - Since `15 > 11`, adjust the `high` pointer: `high = mid - 1 = 6`.

4. **Third Iteration:**
   - Recalculate the mid index: `mid = (5 + 6) // 2 = 5`.
   - Compare `array[5] = 11` with the target `11`.
   - Match found! The target value `11` is located at index `5`.

---

## Implementation in Code

Here’s how you can implement binary search in Python:

```python
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid  # Return the index if found
        elif arr[mid] < target:
            low = mid + 1  # Target is in the right half
        else:
            high = mid - 1  # Target is in the left half
            
    return -1  # Return -1 if the target is not found

# Example usage
arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
target = 11
result = binary_search(arr, target)

if result != -1:
    print(f"Element found at index: {result}")
else:
    print("Element not found in the array.")
```

### Explanation of Code

- The function `binary_search` takes an array `arr` and a `target` value as arguments.
- It initializes two pointers, `low` and `high`, to represent the current search bounds.
- It enters a loop that continues until the `low` pointer is greater than the `high` pointer.
- The mid index is calculated, and the value at that index is compared with the target.
- Depending on the comparison, it adjusts either the `low` or `high` pointer.
- If the target is found, the index is returned; otherwise, `-1` is returned to indicate that the target is not present.

---

## Time Complexity

The time complexity of binary search is:

- **Best Case:** O(1) - When the target element is at the mid index on the first check.
- **Average Case:** O(log n) - On average, the search space is halved with each iteration.
- **Worst Case:** O(log n) - This occurs when the target is not present, requiring multiple iterations to conclude the search.

### Summary

Binary search is a highly efficient search algorithm that operates on sorted data. With a time complexity of O(log n), it is much faster than linear search for large datasets, making it a preferred choice in many applications where quick data retrieval is essential.

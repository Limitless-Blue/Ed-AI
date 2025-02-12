# Selection Sort

## Table of Contents
1. [How Selection Sort Works](#how-selection-sort-works)
2. [Step-by-Step Example](#step-by-step-example)
3. [Implementation in Code](#implementation-in-code)
4. [Time and Space Complexity](#time-and-space-complexity)
5. [Conclusion](#conclusion)

---

## How Selection Sort Works

Selection Sort is a straightforward comparison-based sorting algorithm. The algorithm divides the input list into two parts: the sorted part and the unsorted part. It repeatedly selects the smallest (or largest, depending on sorting order) element from the unsorted part and swaps it with the first unsorted element, thereby expanding the sorted part of the list one element at a time.

### Key Steps in Selection Sort:
1. **Initialization**: Start with the first element as the initial minimum.
2. **Find the Minimum**: Iterate through the unsorted part of the list to find the smallest element.
3. **Swap**: Swap this smallest element with the first unsorted element.
4. **Repeat**: Move the boundary between sorted and unsorted elements one position to the right and repeat the process until the entire list is sorted.

Selection Sort has several characteristics:
- **Simplicity**: It is easy to understand and implement.
- **In-place**: It requires a constant amount of additional space (O(1)).
- **Unstable**: It may change the relative order of equal elements.
- **Time Complexity**: It has an average and worst-case time complexity of O(n^2).

---

## Step-by-Step Example

Let’s consider the following unsorted list of numbers that we want to sort in ascending order:

```
[64, 25, 12, 22, 11]
```

### Step 1: Find the minimum
- The first step is to find the minimum element in the entire list, which is `11`.

**Sorted part:** []  
**Unsorted part:** [64, 25, 12, 22, 11]  
**Swap:** 11 with 64.

**Result:** [11, 25, 12, 22, 64]

### Step 2: Find the next minimum
- Now, find the minimum in the remaining unsorted part [25, 12, 22, 64], which is `12`.

**Sorted part:** [11]  
**Unsorted part:** [25, 12, 22, 64]  
**Swap:** 12 with 25.

**Result:** [11, 12, 25, 22, 64]

### Step 3: Find the next minimum
- Next, find the minimum in [25, 22, 64], which is `22`.

**Sorted part:** [11, 12]  
**Unsorted part:** [25, 22, 64]  
**Swap:** 22 with 25.

**Result:** [11, 12, 22, 25, 64]

### Step 4: Find the next minimum
- Now, find the minimum in [25, 64], which is `25`.

**Sorted part:** [11, 12, 22]  
**Unsorted part:** [25, 64]  
**Swap:** No swap needed since 25 is already in place.

**Result:** [11, 12, 22, 25, 64]

### Step 5: Last Element
- Finally, the last element `64` is already in the correct position.

**Sorted part:** [11, 12, 22, 25, 64]  
**Unsorted part:** []

The final sorted list is `[11, 12, 22, 25, 64]`.

---

## Implementation in Code

Here is a simple implementation of Selection Sort in Python:

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        # Assume the minimum is the first element of the unsorted part
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        # Swap the found minimum element with the first unsorted element
        arr[i], arr[min_index] = arr[min_index], arr[i]

# Example usage
numbers = [64, 25, 12, 22, 11]
selection_sort(numbers)
print("Sorted array:", numbers)
```

### Explanation of the Code
- The outer loop iterates through each element, treating it as the boundary between the sorted and unsorted parts.
- The inner loop scans the unsorted part of the list to find the minimum element.
- Once the minimum is found, it is swapped with the element at the current index of the outer loop.

---

## Time and Space Complexity

### Time Complexity
- **Best Case**: O(n^2) - The best-case scenario occurs when the list is already sorted. The algorithm still checks all elements.
- **Average Case**: O(n^2) - Selection Sort performs consistently regardless of the initial order of elements.
- **Worst Case**: O(n^2) - The worst-case scenario also involves checking all elements.

### Space Complexity
- **O(1)** - Selection Sort is an in-place sorting algorithm, requiring only a constant amount of additional space for variables, irrespective of the input size.

---

## Conclusion

Selection Sort is a simple yet effective sorting algorithm, especially suitable for small datasets. While its O(n^2) time complexity makes it inefficient for large lists, its ease of implementation and in-place sorting capability make it useful in specific contexts. Understanding Selection Sort also lays the foundation for more complex sorting algorithms and helps in grasping fundamental algorithmic principles.

# Insertion Sort

## Table of Contents
1. [How Insertion Sort Works](#how-insertion-sort-works)
2. [Step-by-Step Example](#step-by-step-example)
3. [Implementation in Code](#implementation-in-code)
4. [When to Use Insertion Sort](#when-to-use-insertion-sort)
5. [Conclusion](#conclusion)

---

## How Insertion Sort Works

Insertion Sort is a simple sorting algorithm that builds a sorted array (or list) one element at a time. It is much less efficient on large lists compared to more advanced algorithms like quicksort, heapsort, or merge sort. However, it offers several advantages:

- **Simplicity**: The algorithm is straightforward to understand and implement.
- **Efficient for small datasets**: Insertion Sort can be more efficient for small lists, especially when compared to more complex algorithms.
- **Adaptive**: It performs well when the list is already partially sorted, making fewer comparisons and shifts.
- **Stable**: It maintains the relative order of records with equal keys, which is important in certain applications.

The algorithm works by dividing the list into a sorted and an unsorted part. Initially, the sorted part contains the first element. The algorithm then repeatedly takes the next element from the unsorted part and inserts it into the correct position in the sorted part.

---

## Step-by-Step Example

Let’s consider the following unsorted list of numbers that we want to sort in ascending order:

```
[5, 2, 4, 6, 1, 3]
```

### Step 1: Start with the first element
The first element, `5`, is already considered sorted.

**Sorted part:** [5]  
**Unsorted part:** [2, 4, 6, 1, 3]

### Step 2: Insert the second element
Take `2` from the unsorted part. Compare it with `5`. Since `2` is smaller, we place `2` before `5`.

**Sorted part:** [2, 5]  
**Unsorted part:** [4, 6, 1, 3]

### Step 3: Insert the third element
Next, we take `4`. We compare it with `5` and then `2`. Since `4` is greater than `2` but less than `5`, we place `4` between `2` and `5`.

**Sorted part:** [2, 4, 5]  
**Unsorted part:** [6, 1, 3]

### Step 4: Insert the fourth element
Now, we take `6`. Since `6` is greater than all elements in the sorted part, it remains at the end.

**Sorted part:** [2, 4, 5, 6]  
**Unsorted part:** [1, 3]

### Step 5: Insert the fifth element
Next, we take `1`. We compare it with `6`, `5`, `4`, and `2`. Since `1` is smaller than all of them, we place `1` at the beginning.

**Sorted part:** [1, 2, 4, 5, 6]  
**Unsorted part:** [3]

### Step 6: Insert the last element
Finally, we take `3`. We compare it with `6`, `5`, and `4`, finding that `3` should be placed between `2` and `4`.

**Sorted part:** [1, 2, 3, 4, 5, 6]  
**Unsorted part:** []

The final sorted list is `[1, 2, 3, 4, 5, 6]`.

---

## Implementation in Code

Here is a simple implementation of Insertion Sort in Python:

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]  # The element to be positioned
        j = i - 1
        
        # Move elements of arr[0..i-1], that are greater than key,
        # to one position ahead of their current position
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key  # Insert key at its correct position

# Example usage
numbers = [5, 2, 4, 6, 1, 3]
insertion_sort(numbers)
print("Sorted array:", numbers)
```

### Explanation of the Code
- We start from the second element (index 1) since the first element is trivially sorted.
- We store the current element in `key` and compare it with the elements in the sorted part.
- We shift larger elements to the right until we find the correct position for `key`, where we insert it.

---

## When to Use Insertion Sort

Insertion Sort is particularly useful in the following scenarios:

- **Small datasets**: It is efficient for small lists (generally less than 20 elements).
- **Nearly sorted datasets**: When the list is mostly sorted, it can be very efficient due to its adaptive nature.
- **Real-time applications**: Where the algorithm needs to continually insert elements in a sorted manner, such as in online sorting.
- **Memory constraints**: Since it sorts in place with a space complexity of O(1), it is suitable for memory-constrained environments.

---

## Conclusion

Insertion Sort is a straightforward sorting algorithm that works well for small or nearly sorted datasets. While it is not suitable for large lists due to its O(n^2) time complexity, it remains an important algorithm to understand due to its simplicity and practical use cases in certain contexts. Understanding Insertion Sort also lays the groundwork for more complex sorting algorithms.

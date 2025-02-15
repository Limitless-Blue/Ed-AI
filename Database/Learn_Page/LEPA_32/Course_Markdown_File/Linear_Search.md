# Linear Search

## Table of Contents
1. [What is Linear Search?](#what-is-linear-search)
2. [How Linear Search Works](#how-linear-search-works)
3. [Step-by-Step Example](#step-by-step-example)
4. [Implementation in Code](#implementation-in-code)
5. [Time Complexity](#time-complexity)

---

## What is Linear Search?

Linear search, also known as sequential search, is a simple search algorithm that checks each element in a list or array sequentially until the desired element is found or the end of the list is reached. It is the most straightforward search algorithm, making it easy to implement but inefficient for large datasets.

---

## How Linear Search Works

The linear search algorithm operates as follows:

1. Start from the first element of the list.
2. Compare the current element with the target value.
3. If the current element matches the target, return the index of the element.
4. If the current element does not match, move to the next element in the list.
5. Repeat steps 2-4 until the target is found or the end of the list is reached.
6. If the target is not found after checking all elements, return a value indicating that the target is not present in the list.

---

## Step-by-Step Example

Let's consider a simple example to illustrate how linear search works.

### Example

Given the following list of integers:

```
list = [3, 5, 1, 4, 2]
```

Let's say we want to find the target value `4`.

**Steps:**

1. Start with the first element `3`:
   - Compare `3` with `4`: No match.
2. Move to the second element `5`:
   - Compare `5` with `4`: No match.
3. Move to the third element `1`:
   - Compare `1` with `4`: No match.
4. Move to the fourth element `4`:
   - Compare `4` with `4`: Match found!

The target value `4` is found at index `3` of the list.

---

## Implementation in Code

Here’s how you can implement linear search in Python:

```python
def linear_search(arr, target):
    for index in range(len(arr)):
        if arr[index] == target:
            return index  # Return the index if found
    return -1  # Return -1 if the target is not found

# Example usage
arr = [3, 5, 1, 4, 2]
target = 4
result = linear_search(arr, target)

if result != -1:
    print(f"Element found at index: {result}")
else:
    print("Element not found in the array.")
```

### Explanation of Code

- The function `linear_search` takes an array `arr` and a `target` value as arguments.
- It iterates through each element of the array.
- If it finds the target, it returns the index.
- If it completes the loop without finding the target, it returns `-1` to indicate that the target is not present.

---

## Time Complexity

The time complexity of linear search is:

- **Best Case:** O(1) - When the target element is the first element of the list.
- **Average Case:** O(n) - On average, half of the elements will be checked.
- **Worst Case:** O(n) - When the target element is the last element or not present in the list at all.

### Summary

Linear search is simple to implement and understand but is inefficient for large datasets due to its O(n) time complexity. For better performance, especially with large datasets, other search algorithms like binary search should be considered, provided that the data is sorted.

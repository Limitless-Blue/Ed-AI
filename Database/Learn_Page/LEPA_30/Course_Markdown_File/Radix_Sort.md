# Radix Sort

## Table of Contents
1. [Introduction to Radix Sort](#introduction-to-radix-sort)
2. [How Radix Sort Works](#how-radix-sort-works)
3. [Implementation in Code](#implementation-in-code)
4. [When to Use Radix Sort](#when-to-use-radix-sort)

---

## 1. Introduction to Radix Sort

**Radix Sort** is a non-comparative sorting algorithm that sorts numbers by processing individual digits. It processes numbers digit by digit, starting from the least significant digit (LSD) to the most significant digit (MSD), or vice versa.

### Key Characteristics:
- **Non-comparative**: Unlike sorting algorithms such as Merge Sort or Quick Sort, Radix Sort doesn’t compare elements directly.
- **Stable Sorting**: Radix Sort maintains the relative order of elements with equal keys.
- **Efficient**: It has a time complexity of **O(nk)**, where **n** is the number of elements, and **k** is the number of digits in the largest number.

### Example:
Consider sorting the numbers [170, 45, 75, 90, 802, 24, 2, 66]:
- First, sort by the least significant digit (LSD).
- Then, sort by the next digit, and so on.

---

## 2. How Radix Sort Works

Radix Sort typically works in two steps:
1. **Digit-by-Digit Sorting**: Start sorting from the least significant digit and move towards the most significant digit.
2. **Use a Stable Sorting Algorithm**: For sorting based on digits, a stable sorting algorithm like **Counting Sort** is used. Stability ensures that numbers with the same digit in the current place retain their relative order from previous sorts.

### Steps:
- **Step 1**: Start by sorting based on the least significant digit (LSD).
- **Step 2**: Move to the next digit (tens, hundreds, etc.) and sort again, maintaining the previous sorting order.
- **Step 3**: Repeat the process for all digits.

### Example:

Suppose we have the following numbers: `[170, 45, 75, 90, 802, 24, 2, 66]`.
- First, sort by the unit place (LSD):
  - `[170, 90, 802, 2, 24, 45, 75, 66]`
- Then sort by the tens place:
  - `[802, 2, 24, 45, 66, 170, 75, 90]`
- Finally, sort by the hundreds place:
  - `[2, 24, 45, 66, 75, 90, 170, 802]`

---

## 3. Implementation in Code

Here is a Python implementation of Radix Sort:

```python
# A function to do counting sort based on a digit
def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n  # Output array
    count = [0] * 10  # Count array to store occurrences of digits (0-9)

    # Store count of occurrences in the count array
    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1

    # Change count[i] to store the actual position of this digit
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array using the count array
    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    # Copy the output array to arr
    for i in range(n):
        arr[i] = output[i]

# Function to do Radix Sort
def radix_sort(arr):
    # Find the maximum number to know the number of digits
    max_num = max(arr)

    # Do counting sort for every digit, starting from the least significant digit (LSD)
    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10

# Example usage
arr = [170, 45, 75, 90, 802, 24, 2, 66]
radix_sort(arr)
print(f"Sorted array: {arr}")
```

### Explanation:
- **Counting Sort** is used to sort based on the current digit. It counts the occurrences of each digit and arranges the elements accordingly.
- **Radix Sort** function determines the number of digits in the largest number and applies counting sort to each digit from least significant to most significant.

---

## 4. When to Use Radix Sort

Radix Sort is particularly useful when:
- **All elements have a similar range of values**: Radix Sort performs well when sorting integers or strings of fixed length.
- **The number of digits (k) is significantly smaller than the number of elements (n)**: In such cases, the time complexity of Radix Sort, O(nk), is efficient.
- **You require stable sorting**: Since Radix Sort is stable, it can be advantageous when the order of equivalent elements is important.

### Pros:
- **Efficiency**: When the number of digits is relatively small, Radix Sort is more efficient than comparison-based algorithms.
- **Non-comparative**: Radix Sort doesn’t rely on element-to-element comparisons, making it faster for sorting large datasets with fixed-width keys.

### Cons:
- **Not In-Place**: Radix Sort requires additional space for storing counting arrays, making it less memory-efficient than in-place sorting algorithms like Quick Sort.
- **Limited Scope**: Radix Sort is mainly applicable to integers or strings and is less useful for general-purpose sorting.

---

## Conclusion

Radix Sort is a powerful non-comparative sorting algorithm that works by sorting numbers digit by digit. By leveraging a stable sorting algorithm such as Counting Sort for each digit, Radix Sort can achieve efficient sorting with time complexity O(nk). However, it is best suited for cases where the number of digits is much smaller than the number of elements, making it highly efficient for sorting integers or fixed-length strings.
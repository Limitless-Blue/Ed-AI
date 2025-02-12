# Advanced Searching Techniques

## Table of Contents
- [1. Ternary Search Overview](#1-ternary-search-overview)
- [2. Fibonacci Search Basics](#2-fibonacci-search-basics)
- [3. Summary](#3-summary)

## 1. Ternary Search Overview
Ternary Search is a divide-and-conquer search algorithm that finds the position of a target value within a sorted array. It is similar to Binary Search but divides the search space into three parts instead of two. This method can be particularly useful when you want to optimize search operations for specific types of data.

### How Ternary Search Works
1. **Dividing the Array**: Ternary Search divides the sorted array into three parts using two midpoints. Specifically, it calculates two midpoints, \( mid1 \) and \( mid2 \):
   - \( mid1 = left + (right - left) / 3 \)
   - \( mid2 = right - (right - left) / 3 \)
  
2. **Comparisons**: The algorithm then performs comparisons:
   - If the target is equal to the element at \( mid1 \), return \( mid1 \).
   - If the target is equal to the element at \( mid2 \), return \( mid2 \).
   - If the target is less than the element at \( mid1 \), search the left third of the array.
   - If the target is greater than the element at \( mid2 \), search the right third of the array.
   - If the target is between the two midpoints, search the middle third.

### Example
Consider a sorted array:
```
array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
```
Let’s search for the number `8`.

1. Initial indices: `left = 0`, `right = 14`
2. Calculate midpoints:
   - \( mid1 = 0 + (14 - 0) / 3 = 4 \) (value = `5`)
   - \( mid2 = 14 - (14 - 0) / 3 = 10 \) (value = `11`)
3. Compare:
   - `8` is greater than `5` and less than `11`, so search the middle section `[6, 7, 8, 9]`.
4. Repeat the process in this smaller range until the target is found.

### Complexity
- **Time Complexity**: O(log3 n), as each iteration reduces the size of the search space to one-third.
- **Space Complexity**: O(1) for the iterative version or O(log n) for the recursive version due to function call overhead.

## 2. Fibonacci Search Basics
Fibonacci Search is another efficient searching algorithm that uses Fibonacci numbers to divide the array into sections for searching. This technique can be particularly advantageous when the size of the dataset is not a power of two, as it optimally uses the properties of Fibonacci numbers.

### How Fibonacci Search Works
1. **Precompute Fibonacci Numbers**: The first step involves generating Fibonacci numbers up to the size of the array.
  
2. **Division**: The search space is divided based on the Fibonacci sequence:
   - Let \( F_k \) be the largest Fibonacci number less than or equal to the length of the array.
   - The division points are determined using \( F_{k-1} \) and \( F_{k-2} \).

3. **Comparisons**: Similar to Binary Search, Fibonacci Search compares the target with elements at the division points:
   - If the target is equal to the element, return the index.
   - If the target is less than the element, narrow the search to the previous Fibonacci segment.
   - If the target is greater than the element, adjust the indices according to the Fibonacci numbers.

### Example
Consider the same sorted array:
```
array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
```
Let’s search for the number `8`.

1. **Precompute Fibonacci Numbers**: The Fibonacci numbers are `[0, 1, 1, 2, 3, 5, 8, 13]`.
2. **Use the largest Fibonacci number**: Here, \( F_k = 13 \) (length of the array).
3. Start with `offset = -1` and use the Fibonacci sequence to check elements at indices determined by \( F_{k-2} \) and \( F_{k-1} \).
4. Continue the process until the target is found or the search space is exhausted.

### Complexity
- **Time Complexity**: O(log n), as it effectively reduces the search space using Fibonacci numbers.
- **Space Complexity**: O(1) for both iterative and recursive implementations.

## 3. Summary
Both Ternary Search and Fibonacci Search are advanced searching techniques that optimize search operations compared to traditional methods. While Ternary Search divides the search space into three parts, Fibonacci Search leverages the properties of Fibonacci numbers to perform efficient searches in sorted arrays. These techniques offer alternatives to Binary Search, especially in scenarios where the dataset size and structure warrant their use.
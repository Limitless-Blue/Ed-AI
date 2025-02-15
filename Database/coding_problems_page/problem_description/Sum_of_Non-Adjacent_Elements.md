
**Problem Statement**

You are given an array of integers. Your task is to find the maximum sum of elements such that no two elements are adjacent to each other in the array. In other words, you cannot pick two consecutive elements.

**Input**

- A single integer `n` denoting the size of the array.
- An array `arr` of size `n`, where `arr[i]` is the `i`-th integer of the array.

**Output**

- The maximum sum you can obtain from non-adjacent elements.

**Constraints**

- \(1 \leq n \leq 10^5\)
- \(-10^4 \leq arr[i] \leq 10^4\)

**Example**

**Example 1:**
**Input:**
4 3 2 7 10


**Output:**
13


**Explanation:** You can pick 3 and 10, which gives the maximum sum of 13.

**Example 2:**
**Input:**
5 3 2 5 10 7


**Output:**
15

**Explanation:** You can pick 3, 5, and 7, giving a total of 15.

**Example 3:**
**Input:**
3 3 2 7


**Output:**
10

**Explanation:** You can pick 3 and 7, giving a total of 10.

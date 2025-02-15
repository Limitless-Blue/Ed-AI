
Given an array of **N** positive integers and an integer **K**, find the minimum length of a contiguous subarray whose sum is greater than or equal to **K**. If no such subarray exists, output `0`.

**Input Format**

- The first line contains two space-separated integers **N** and **K**.
- The second line contains **N** space-separated positive integers representing the elements of the array.

**Constraints**

- \(1 \leq N \leq 10^5\)
- \(1 \leq K \leq 10^{14}\)
- \(1 \leq \text{array}[i] \leq 10^9\)

**Output Format**

- Print a single integer denoting the minimum length of a subarray with sum ≥ **K**. If no such subarray exists, print `0`.

**Sample Input**

10 15 1 2 3 4 5 6 7 8 9 10


**Sample Output**

2


**Explanation**

The subarray `[7, 8]` has a sum of `15` and length `2`, which is the minimal possible.


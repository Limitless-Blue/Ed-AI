
**Problem Statement**

Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` (`0 <= i <= n`), `ans[i]` is the number of `1`'s in the binary representation of `i`.

**Example**

**Example 1:**
Input:  
`n = 2`  
Output:  
`[0, 1, 1]`  
Explanation:  
- 0 -> 0 has 0 one-bits.  
- 1 -> 1 has 1 one-bit.  
- 2 -> 10 has 1 one-bit.

**Example 2:**
Input:  
`n = 5`  
Output:  
`[0, 1, 1, 2, 1, 2]`  
Explanation:  
- 0 -> 0 has 0 one-bits.  
- 1 -> 1 has 1 one-bit.  
- 2 -> 10 has 1 one-bit.  
- 3 -> 11 has 2 one-bits.  
- 4 -> 100 has 1 one-bit.  
- 5 -> 101 has 2 one-bits.

**Constraints:**
- `0 <= n <= 10^5`

**Follow-up:**
- It is very important to optimize the solution to run in **O(n)** time.

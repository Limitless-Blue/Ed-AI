
**Problem Statement**

Given an integer array `nums`, return the maximum result of `nums[i] XOR nums[j]`, where `0 <= i <= j < n`.

**Example**

**Example 1:**
Input:  
`nums = [3, 10, 5, 25, 2, 8]`  
Output:  
`28`  
Explanation: The maximum result is `5 XOR 25 = 28`.

**Example 2:**
Input:  
`nums = [14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70]`  
Output:  
`127`  
Explanation: The maximum result is `53 XOR 83 = 127`.

**Constraints:**
- `1 <= nums.length <= 2 * 10^5`
- `0 <= nums[i] <= 2^31 - 1`

**Follow-up:**
Can you find an `O(n)` solution?

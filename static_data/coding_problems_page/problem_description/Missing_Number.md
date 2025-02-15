
**Problem Statement**

Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.

**Example**

**Example 1:**
Input:  
`nums = [3,0,1]`  
Output:  
`2`  
Explanation: The range is `[0, 3]`, and `2` is the missing number.

**Example 2:**
Input:  
`nums = [0,1]`  
Output:  
`2`  
Explanation: The range is `[0, 2]`, and `2` is the missing number.

**Example 3:**
Input:  
`nums = [9,6,4,2,3,5,7,0,1]`  
Output:  
`8`  
Explanation: The range is `[0, 9]`, and `8` is the missing number.

**Constraints:**
- `n == nums.length`
- `1 <= n <= 10^4`
- `0 <= nums[i] <= n`
- All the numbers of `nums` are distinct.

**Follow-up:**
Could you implement a solution using **O(n)** time complexity and **O(1)** extra space complexity?

# Arrays & Hashing

## What is an Array?

An array is a contiguous block of memory storing elements of the same type. Accessing any element by index is O(1) because the address is computed directly: `base_address + index * element_size`.

## Common Patterns

### Two Pointers
Use two indices moving toward each other to avoid nested loops. Reduces O(n²) to O(n).

```python
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
```

### Hash Map for O(1) Lookup
Store values you've seen so you can check complements in constant time.

```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i
```

## Key Insight
The jump from O(n²) to O(n) almost always comes from trading space for time — storing something in a hash map so you don't have to scan again.

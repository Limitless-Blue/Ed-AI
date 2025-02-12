def two_sum(nums, target):
    # Dictionary to store the complement and corresponding index
    num_map = {}
    # Loop through the array
    for i, num in enumerate(nums):
        # Calculate complement
        complement = target - num
        # If the complement is found in the map, return the indices
        if complement in num_map:
            return [num_map[complement], i]
        # Otherwise, store the number with its index
        num_map[num] = i


# Input parsing
nums = list(map(int, input().split()))
target = int(input())
# Get result
result = two_sum(nums, target)
# Print result
print(result)

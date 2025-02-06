def single_number(nums):
    # XOR all elements in the array
    result = 0
    for num in nums:
        result ^= num  # XOR with each element
    return result


input_data = list(map(int, input().strip().split()))
print(single_number(input_data))

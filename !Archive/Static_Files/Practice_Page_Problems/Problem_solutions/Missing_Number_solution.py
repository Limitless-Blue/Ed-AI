def missing_number(nums):
    # XOR all numbers from 0 to n and XOR with all elements in the array
    missing = len(nums)

    for i, num in enumerate(nums):
        missing ^= i ^ num

    return missing


input_data = list(map(int, input().strip().split()))
print(missing_number(input_data))

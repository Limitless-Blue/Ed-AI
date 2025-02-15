def find_maximum_xor(nums):
    L = len(bin(max(nums))) - 2  # Find the length of the largest number in binary
    max_xor = 0
    prefix_set = set()

    # Iteratively compute the maximum XOR for each bit position, starting from the most significant bit
    for i in range(L - 1, -1, -1):
        # Shift the current max_xor by 1 to accommodate the next bit
        max_xor <<= 1
        current_xor = (
            max_xor | 1
        )  # Consider current bit to be set in the potential max result

        # Store prefixes of the numbers up to the ith bit
        prefix_set.clear()
        for num in nums:
            prefix_set.add(
                num >> i
            )  # Only consider the first (L-i) bits of each number

        # Check if there's a pair of prefixes that could form the current_xor
        for p in prefix_set:
            if current_xor ^ p in prefix_set:
                max_xor = current_xor
                break

    return max_xor


input_data = list(map(int, input().strip().split()))
print(find_maximum_xor(input_data))

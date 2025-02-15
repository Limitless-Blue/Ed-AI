def single_number(nums):
    ones, twos = 0, 0

    for num in nums:
        # `ones & num` gives the bits that are going to be added to `twos`
        twos |= ones & num
        # XOR to add the current number to `ones`
        ones ^= num
        # Mask to remove bits that appear three times in both `ones` and `twos`
        common_mask = ~(ones & twos)
        # Apply the mask
        ones &= common_mask
        twos &= common_mask

    return ones


input_data = list(map(int, input().strip().split()))
print(single_number(input_data))

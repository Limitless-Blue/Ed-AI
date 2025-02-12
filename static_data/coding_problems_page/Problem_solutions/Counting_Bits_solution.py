def count_bits(n):
    # Initialize the result array with 0's
    ans = [0] * (n + 1)

    for i in range(1, n + 1):
        # Using the formula: ans[i] = ans[i >> 1] + (i & 1)
        ans[i] = ans[i >> 1] + (i & 1)

    return ans


n = int(input().strip())
result = count_bits(n)
print(result)

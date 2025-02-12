def max_non_adjacent_sum(arr):
    if not arr:
        return 0

    n = len(arr)

    # Edge cases
    if n == 1:
        return max(0, arr[0])

    # Initialize two variables to store the maximum sum till previous index
    incl = arr[0]  # include the first element
    excl = 0  # exclude the first element

    for i in range(1, n):
        # Store the current max excluding arr[i]
        new_excl = max(incl, excl)

        # Update incl to be the previous excl + arr[i]
        incl = excl + arr[i]
        excl = new_excl

    # Return the maximum of incl and excl
    return max(incl, excl)


n = int(input())
arr = list(map(int, input().split()))
print(max_non_adjacent_sum(arr))

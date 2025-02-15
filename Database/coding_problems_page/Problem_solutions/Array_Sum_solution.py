# Solution for Array Sum Problem


def array_sum():
    n = int(input())  # Read the size of the array
    arr = list(map(int, input().split()))  # Read the array elements
    print(sum(arr))  # Print the sum of array elements


# Call the function
array_sum()

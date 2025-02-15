def is_anagram(s, t):
    # Check if sorted versions of both strings are equal
    return sorted(s) == sorted(t)


input_data = input().strip().split()
s, t = input_data[0], input_data[1]
print(is_anagram(s, t))

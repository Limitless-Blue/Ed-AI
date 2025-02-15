def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    if k == 0 or not s:
        return 0

    left = 0
    right = 0
    max_len = 0
    char_map = {}

    while right < len(s):
        char = s[right]
        if char in char_map:
            char_map[char] += 1
        else:
            char_map[char] = 1

        while len(char_map) > k:
            left_char = s[left]
            char_map[left_char] -= 1
            if char_map[left_char] == 0:
                del char_map[left_char]
            left += 1

        max_len = max(max_len, right - left + 1)
        right += 1

    return max_len


input_data = input().strip().split()
s = input_data[0]
k = int(input_data[1])
print(length_of_longest_substring_k_distinct(s, k))

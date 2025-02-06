def longest_palindromic_substring(s: str) -> str:
    if len(s) == 0:
        return ""

    start = 0
    max_len = 1

    def expand_around_center(left: int, right: int) -> None:
        nonlocal start, max_len
        while left >= 0 and right < len(s) and s[left] == s[right]:
            current_len = right - left + 1
            if current_len > max_len:
                start = left
                max_len = current_len
            left -= 1
            right += 1

    for i in range(len(s)):
        # Odd length palindromes
        expand_around_center(i, i)
        # Even length palindromes
        expand_around_center(i, i + 1)

    return s[start : start + max_len]


In_String = input()
print(longest_palindromic_substring(In_String))

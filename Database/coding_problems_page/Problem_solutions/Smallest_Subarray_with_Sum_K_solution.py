n_k = input().split()
n = int(n_k[0])
k = int(n_k[1])
arr = list(map(int, input().split()))

min_length = n + 1
current_sum = 0
start = 0

for end in range(n):
    current_sum += arr[end]
    while current_sum >= k:
        min_length = min(min_length, end - start + 1)
        current_sum -= arr[start]
        start += 1

if min_length == n + 1:
    print(0)
else:
    print(min_length)

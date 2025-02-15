n = int(input())
arr = list(map(int, input().split()))

max_current = max_global = arr[0]

for i in range(1, n):
    max_current = max(arr[i], max_current + arr[i])
    max_global = max(max_global, max_current)

print(max_global)

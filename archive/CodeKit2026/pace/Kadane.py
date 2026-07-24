x = int (input())
arr = list(map(int, input().split()))

sum = arr[0] # current sum
mostsum = arr[0] # store the most sum that have been founded

for i in range(1,x):
    sum = max(arr[i], sum + arr[i])
    mostsum = max(mostsum,sum)

print(mostsum)
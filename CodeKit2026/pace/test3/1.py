# Kadane's Algorithm
x = int(input())
y = (list(map(int, input().split())))

current_sum = y[0]
max_sum = y[0]

for i in range(1,x):
    current_sum = max(y[i], current_sum+y[i])
    max_sum = max(max_sum, current_sum)

print(max_sum)
x = int (input())
arr = list(map(int, input().split()))

count = {}

for i in arr:
    if i in count:
        count[i] += 1
    else:
        count[i] = 1
    
for j in count:
    if count[j] == 1:
        print(j)
        break
    
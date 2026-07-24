### Input
# 5 80
# 75 90 81 60 100

### Output
# 3

x=list(map(int, input().split()))
y=list(map(int, input().split()))
a=0
for i in range(int(x[0])):
    if y[i] >= x[1]:
        a=a+1
print(a)
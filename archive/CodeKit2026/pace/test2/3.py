x=int(input())
y=list(map(int, input().split()))
a=0
for i in range(x):
    if y[i] < 0:
        a=1
if a == 0:
    print("safe")
else:
    print("alert")
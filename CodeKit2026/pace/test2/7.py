x=int(input())
y=list(map(int,input().split()))
a=0
for i in range(x-1):
    if y[i] == y[i+1]:
        a=1
if a == 1:
    print("yes")
else:
    print("no")
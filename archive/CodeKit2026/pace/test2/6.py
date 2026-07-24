x=int(input())
y=list(map(int,input().split()))
a=0
for i in range(x):
    if y[i] % 2 == 1:
        a=a+1

print(a)
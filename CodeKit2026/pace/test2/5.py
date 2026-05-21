x=list(map(int, input().split()))
y=list(map(int,input().split()))
a=0
for i in range(x[0]):
    if y[i] >= x[1]:
        a=a+1
print(a)
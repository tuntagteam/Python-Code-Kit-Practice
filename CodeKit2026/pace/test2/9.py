x=int(input())
y=list(map(int,input().split()))
a=0
for i in range(x-1):
    if y[i+1] > y[i]:
        a+=1
print(a)
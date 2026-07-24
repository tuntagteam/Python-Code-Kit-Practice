x=int(input())
y=list(map(int,input().split()))

a = {}
for i in y:
    if i in a:
        a[i]+=1
    else:
        a[i] = 1

for i, k in a.items():
    if k == 1:
        print(i)
        break
x=int(input())
y=list(map(int,input().split()))


a = b =y[0]

for x in y[1:]:
    b = max(x, b +x)
    a = max(a, b)

print(a)
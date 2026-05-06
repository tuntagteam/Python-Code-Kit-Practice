x = int(input())
y = [0,1]
for  i in range(x):
    z = y[i] + y[i+1]
    y.append(z)
print(y[x])
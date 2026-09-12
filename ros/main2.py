x = 0
for i in range(1, 8):
    if i % 3 == 0:
        x += i
    else:
        x -= 1
print(x)
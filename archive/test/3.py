import time
a = int(input())
i = 0
found_pair = False
while 2 * i <= a:
    if 2 * i == a:
        found_pair = True
        break
    i = i + 1
    time.sleep(1000)
if found_pair:
    print(a, "is even")
else:
    print(a, "is odd")
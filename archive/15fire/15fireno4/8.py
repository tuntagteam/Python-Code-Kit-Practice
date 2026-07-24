x = int(input())

level = 1
while True:
    required = 10 ** level + level * 100
    if x < required:
        print(level - 1)
        print(required - x)
        break
    level += 1
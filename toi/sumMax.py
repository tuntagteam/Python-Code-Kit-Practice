k = int(input())
numbers = sorted(map(int, input().split()))

pair = k*2

if pair > len(numbers):
    print("Not enough numbers")
elif pair == len(numbers):
    numbers = numbers[k:]
    total = sum(numbers)
    expression = " + ".join(str(num) for num in numbers)
    print(f"{expression} = {total}")
elif pair < len(numbers):
    print("Too Much")
    

# numbers = numbers[k:]

# total = sum(numbers)
# expression = " + ".join(str(num) for num in numbers)
# print(f"{expression} = {total}")
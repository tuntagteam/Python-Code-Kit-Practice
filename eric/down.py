# n=10

# for i in range(n,1,-1):
#     print(i)


# n = int(input())

# for i in range(1,13):
#     print(f"{n} x {i} = {n*i}")

# fruits = ["apple" , "banana" , 'orange']

# print(fruits)

# for i in range(len(fruits)):
#     print(fruits[i])

# fruits.pop(0)

# for i in range(len(fruits)):
#     print(fruits[i])

score = []
total = 0

for i in range(5):
    student = int(input())
    score.append(student)

print(score)

for i in range(len(score)):
    total += score[i]

avg = total / 5
print(total)
print(avg)

user_input = input("กรอกคะแนน (คั่นด้วยช่องว่าง): ")
scores = list(map(int, user_input.strip().split()))

total = 0
count = 0

for score in scores:
    total += score
    count += 1

average = total / count

print("{:.2f}".format(average))
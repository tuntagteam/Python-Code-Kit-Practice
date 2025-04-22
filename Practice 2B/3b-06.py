user_input = input("กรอกคะแนน (คั่นด้วยช่องว่าง): ")
scores = list(map(int, user_input.strip().split()))

total = sum(scores)
count = len(scores)
average = total / count

print("{:.2f}".format(average))




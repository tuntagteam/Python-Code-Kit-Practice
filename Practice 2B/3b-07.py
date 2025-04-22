user_input = input("กรอกคะแนน (คั่นด้วยช่องว่าง): ")
scores = list(map(int, user_input.strip().split()))

top_score = scores[0]

for score in scores:
    if score > top_score:
        top_score = score 

print(top_score)
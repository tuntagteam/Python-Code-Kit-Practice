import numpy as np
import pandas as pd

n = int(input("กรุณาใส่จำนวนผู้เล่น: "))

names = []
scores = []

for i in range(n):
    name = input(f"ชื่อผู้เล่นคนที่ {i+1}: ")
    score = float(input(f"คะแนนของ {name}: "))
    names.append(name)
    scores.append(score)

names = np.array(names)
scores = np.array(scores)
df = pd.DataFrame({'name': names, 'score': scores})

df = df.sort_values('score', ascending=False).reset_index(drop=True)

df['rank'] = df['score'].rank(method='min', ascending=False).astype(int)

print("\nLeaderboard:")
print(df[['rank', 'name', 'score']].to_string(index=False))
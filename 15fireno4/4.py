import pandas as pd

user_input = input("Enter n: ").strip()
n = int(user_input)

df = pd.DataFrame({
    'Multiplier': range(1, 26),
})
df['Result'] = df['Multiplier'] * n

print(df.to_string(index=False))

total = df['Result'].sum()
print(f"\nTotal = {total}")
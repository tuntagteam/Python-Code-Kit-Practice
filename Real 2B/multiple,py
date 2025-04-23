import pandas as pd

num = int(input("Enter a number to generate its multiplication table: "))

lines = [f"{num} x {i} = {num * i}" for i in range(1, 13)]

df = pd.DataFrame({"Multiplication Table": lines})

print("\nMultiplication Table:")
print(df.to_string(index=False))
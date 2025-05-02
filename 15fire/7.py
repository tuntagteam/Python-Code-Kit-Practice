import pandas as pd

def solve():
    data = [
        {"product": "Coke", "amount": 100},
        {"product": "Pepsi", "amount": 150},
        {"product": "Sprite", "amount": 80},
        {"product": "Fanta", "amount": 120},
        {"product": "Pepsi", "amount": 200},
        {"product": "Coke", "amount": 50},
        {"product": "Sprite", "amount": 60},
        {"product": "Fanta", "amount": 30},
        {"product": "Coke", "amount": 80},
    ]

    df = pd.DataFrame(data)
    top_products = df.groupby("product")["amount"].sum().sort_values(ascending=False).head(3)

    for product, total in top_products.items():
        print(f"{product}: {total}")

if __name__ == "__main__":
    solve()
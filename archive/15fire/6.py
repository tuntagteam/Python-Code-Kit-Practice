import pandas as pd

def solve():
    data = [
        {"date": "2025-01-05", "amount": 100},
        {"date": "2025-01-18", "amount": 150},
        {"date": "2025-02-02", "amount": 80},
        {"date": "2025-02-20", "amount": 220},
        {"date": "2025-03-01", "amount": 90},
        {"date": "2025-03-15", "amount": 60},
    ]

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly = df.groupby("month")["amount"].sum()

    for month, total in monthly.items():
        print(f"{month}: {total}")

if __name__ == "__main__":
    solve()
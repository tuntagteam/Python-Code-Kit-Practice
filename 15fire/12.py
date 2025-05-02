import pandas as pd

def solve():
    data = [
        {"name": "Alice", "start": "2024-12-20", "end": "2025-01-10"},
        {"name": "Bob", "start": "2025-01-01", "end": None},
        {"name": "Charlie", "start": "2025-02-10", "end": "2025-02-20"},
        {"name": "David", "start": "2025-01-25", "end": "2025-03-01"},
        {"name": "Eva", "start": "2025-01-15", "end": None},
    ]

    df = pd.DataFrame(data)
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"]).fillna(pd.to_datetime("2025-05-02"))

    df["days_worked"] = (df["end"] - df["start"]).dt.days
    result = df[["name", "days_worked"]]
    print(result)

if __name__ == "__main__":
    solve()
import pandas as pd
from datetime import datetime

def solve():
    data = [
        {"name": "Alice", "birthdate": "2000-05-01"},
        {"name": "Bob", "birthdate": "1995-10-22"},
        {"name": "Charlie", "birthdate": "1988-12-30"},
        {"name": "David", "birthdate": "2003-07-19"},
    ]

    df = pd.DataFrame(data)
    df["birthdate"] = pd.to_datetime(df["birthdate"])
    today = datetime(2025, 5, 2)

    def calculate_age(birthdate):
        age = today.year - birthdate.year
        if (today.month, today.day) < (birthdate.month, birthdate.day):
            age -= 1
        return age

    df["age"] = df["birthdate"].apply(calculate_age)
    print(df)

solve()
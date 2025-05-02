import pandas as pd

def solve():
    data = [
        {"name": "Alice", "score": 85},
        {"name": "Bob", "score": 45},
        {"name": "Charlie", "score": 91},
        {"name": "David", "score": 50},
        {"name": "Eva", "score": 39},
    ]

    df = pd.DataFrame(data)
    df["result"] = df["score"].apply(lambda x: "Pass" if x >= 50 else "Fail")
    print(df)

if __name__ == "__main__":
    solve()
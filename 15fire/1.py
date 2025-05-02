import pandas as pd

def solve():
    data = [
        {"name": "Alice", "score": 85},
        {"name": "Bob", "score": 74},
        {"name": "Charlie", "score": 91},
        {"name": "David", "score": 65}
    ]

    df = pd.DataFrame(data)
    avg = df['score'].mean()
    print(f"{avg:.2f}")

if __name__ == "__main__":
    solve()
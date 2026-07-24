import pandas as pd

def solve():
    data = [
        {"name": "Alice", "department": "HR"},
        {"name": "Bob", "department": "IT"},
        {"name": "Charlie", "department": "Finance"},
        {"name": "David", "department": "IT"},
        {"name": "Eva", "department": "Finance"},
        {"name": "Frank", "department": "IT"},
        {"name": "Grace", "department": "HR"},
        {"name": "Helen", "department": "Finance"},
        {"name": "Isaac", "department": "HR"},
    ]

    df = pd.DataFrame(data)
    counts = df["department"].value_counts()

    for dept, count in counts.items():
        print(f"{dept:8} {count}")

if __name__ == "__main__":
    solve()
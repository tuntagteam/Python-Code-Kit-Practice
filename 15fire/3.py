import pandas as pd

def solve():
    data = [
        {"name": "Alice", "score": 85, "class": "A"},
        {"name": "Bob", "score": 74, "class": "B"},
        {"name": "Charlie", "score": 91, "class": "A"},
        {"name": "David", "score": 65, "class": "B"},
        {"name": "Eva", "score": 79, "class": "A"},
        {"name": "Frank", "score": 88, "class": "B"},
    ]

    df = pd.DataFrame(data)
    grouped = df.groupby("class")["score"].mean().sort_index()

    for class_name, avg in grouped.items():
        print(f"Class {class_name}: {avg:.2f}")

if __name__ == "__main__":
    solve()
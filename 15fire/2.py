import pandas as pd

def solve():
    data = {
        "actual":    ["Positive", "Negative", "Positive", "Positive", "Negative", "Negative", "Positive", "Negative"],
        "predicted": ["Positive", "Negative", "Negative", "Positive", "Positive", "Negative", "Positive", "Negative"]
    }

    df = pd.DataFrame(data)
    accuracy = (df["actual"] == df["predicted"]).mean()
    print(f"Accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    solve()
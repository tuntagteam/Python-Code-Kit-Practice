import pandas as pd

def solve():
    data = {
        "actual":   ["Positive", "Negative", "Positive", "Positive", "Negative", "Negative", "Positive", "Negative"],
        "model_A":  ["Positive", "Negative", "Negative", "Positive", "Positive", "Negative", "Positive", "Negative"],
        "model_B":  ["Positive", "Negative", "Positive", "Positive", "Negative", "Positive", "Positive", "Negative"]
    }

    df = pd.DataFrame(data)

    def calculate_metrics(pred_col):
        TP = ((df["actual"] == "Positive") & (df[pred_col] == "Positive")).sum()
        FP = ((df["actual"] == "Negative") & (df[pred_col] == "Positive")).sum()
        FN = ((df["actual"] == "Positive") & (df[pred_col] == "Negative")).sum()
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0
        return precision, recall

    p1, r1 = calculate_metrics("model_A")
    p2, r2 = calculate_metrics("model_B")

    print(f"Model A - Precision: {p1:.2f}, Recall: {r1:.2f}")
    print(f"Model B - Precision: {p2:.2f}, Recall: {r2:.2f}")

if __name__ == "__main__":
    solve()
import pandas as pd

def solve():
    n = int(input("จำนวนนักเรียน: "))
    data = []

    for _ in range(n):
        entry = input("กรอกข้อมูล: ")  # เช่น Alice 85
        name, score = entry.split()
        data.append({"name": name, "score": int(score)})

    df = pd.DataFrame(data)

    def assign_grade(score):
        if score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"

    df["grade"] = df["score"].apply(assign_grade)
    print(df)

if __name__ == "__main__":
    solve()
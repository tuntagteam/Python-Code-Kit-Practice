import pandas as pd

def solve():
    data = [
        {"name": "Alice", "start": "2025-05-01 08:00", "end": "2025-05-01 12:00"},
        {"name": "Bob", "start": "2025-05-01 11:00", "end": "2025-05-01 15:00"},
        {"name": "Charlie", "start": "2025-05-01 14:00", "end": "2025-05-01 18:00"},
        {"name": "David", "start": "2025-05-01 09:00", "end": "2025-05-01 10:30"},
        {"name": "Eva", "start": "2025-05-01 13:00", "end": "2025-05-01 16:00"},
    ]

    df = pd.DataFrame(data)
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])

    print("คู่พนักงานที่ทำงานเวลาเดียวกัน (เวลาซ้อนทับ):")
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            a_start, a_end = df.loc[i, "start"], df.loc[i, "end"]
            b_start, b_end = df.loc[j, "start"], df.loc[j, "end"]
            if a_start < b_end and b_start < a_end:
                print(f"- {df.loc[i, 'name']} ⬄ {df.loc[j, 'name']}")

if __name__ == "__main__":
    solve()
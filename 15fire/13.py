import pandas as pd

def solve():
    data = [
        {"date": "2025-01-01", "type": "in", "amount": 100},
        {"date": "2025-01-05", "type": "out", "amount": 30},
        {"date": "2025-01-10", "type": "in", "amount": 50},
        {"date": "2025-01-15", "type": "out", "amount": 70},
        {"date": "2025-01-20", "type": "out", "amount": 20},
    ]

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    stock = []  # จะเก็บเป็น list ของ dict {"date": ..., "amount": ...}

    for _, row in df.iterrows():
        if row["type"] == "in":
            stock.append({"date": row["date"], "amount": row["amount"]})
        else:
            qty = row["amount"]
            while qty > 0 and stock:
                if stock[0]["amount"] > qty:
                    stock[0]["amount"] -= qty
                    qty = 0
                else:
                    qty -= stock[0]["amount"]
                    stock.pop(0)

    total = sum(item["amount"] for item in stock)
    print(f"สินค้าคงเหลือรวม: {total}")
    print("รายละเอียดคงเหลือ (ตามลำดับ FIFO):")
    for item in stock:
        print(f"- เหลือจากวันที่ {item['date'].date()}: {item['amount']} หน่วย")

if __name__ == "__main__":
    solve()
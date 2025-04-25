n = int(input())
data = [input().split() for _ in range(n)]

income_total = 0
expense_total = 0
beverage_income = 0
utilities_expense = 0
daily_profit = {}

for date, typ, category, amount in data:
    amount = int(amount)
    
    if date not in daily_profit:
        daily_profit[date] = 0

    if typ == 'income':
        income_total += amount
        daily_profit[date] += amount
        if category == 'beverage':
            beverage_income += amount
    else:
        expense_total += amount
        daily_profit[date] -= amount
        if category == 'utilities':
            utilities_expense += amount

net_profit = income_total - expense_total
best_day = max(daily_profit, key=daily_profit.get)

print(f"รายรับรวม: {income_total} บาท")
print(f"รายจ่ายรวม: {expense_total} บาท")
print(f"กำไรสุทธิ: {net_profit} บาท\n")

print(f"รายจ่ายด้าน utilities: {utilities_expense} บาท")
print(f"รายรับจาก beverage: {beverage_income} บาท\n")

print(f"วันที่ทำกำไรสูงสุด: {best_day}")
print("สถานะแต่ละวัน:")
for d in sorted(daily_profit):
    status = "ได้กำไร" if daily_profit[d] > 0 else ("ขาดทุน" if daily_profit[d] < 0 else "เท่าทุน")
    print(f"  {d}: {status}")
# เวอร์ชันที่ 1: Greedy ธรรมดา
m = int(input())
price = 17
bottles = m // price
change = m % price

c10 = change // 10
change %= 10
c5 = change // 5
change %= 5
c1 = change

print("[เวอร์ชัน 1: Greedy]")
print(f"กดน้ำได้ {bottles} ขวด")
print(f"เงินทอน {c10 * 10 + c5 * 5 + c1} บาท")
print(f"10บาท: {c10}, 5บาท: {c5}, 1บาท: {c1}\n")

# เวอร์ชันที่ 2: ใช้ while loop
m = int(input())
price = 17
bottles = m // price
change = m % price

c10 = c5 = c1 = 0
while change >= 10:
    c10 += 1
    change -= 10
while change >= 5:
    c5 += 1
    change -= 5
while change >= 1:
    c1 += 1
    change -= 1

print("[เวอร์ชัน 2: while loop]")
print(f"กดน้ำได้ {bottles} ขวด")
print(f"เงินทอน {c10 * 10 + c5 * 5 + c1} บาท")
print(f"10บาท: {c10}, 5บท: {c5}, 1บท: {c1}\n")

# เวอร์ชันที่ 3: ใช้ list + loop
m = int(input())
price = 17
bottles = m // price
change = m % price

coins = [10, 5, 1]
result = {}

for coin in coins:
    result[coin] = change // coin
    change %= coin

print("[เวอร์ชัน 3: list + loop]")
print(f"กดน้ำได้ {bottles} ขวด")
print(f"เงินทอน {sum(k*v for k,v in result.items())} บาท")
print(f"10บาท: {result[10]}, 5บท: {result[5]}, 1บท: {result[1]}\n")

# เวอร์ชันที่ 4: ใช้ฟังก์ชัน

def change_breakdown(change):
    coins = [10, 5, 1]
    result = {}
    for coin in coins:
        result[coin] = change // coin
        change %= coin
    return result

m = int(input())
price = 17
bottles = m // price
change = m % price
coins = change_breakdown(change)

print("[เวอร์ชัน 4: function]")
print(f"กดน้ำได้ {bottles} ขวด")
print(f"เงินทอน {sum(k*v for k,v in coins.items())} บาท")
print(f"10บาท: {coins[10]}, 5บท: {coins[5]}, 1บท: {coins[1]}\n")

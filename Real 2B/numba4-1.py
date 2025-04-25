m = int(input("Enter a money: "))
price = 17
bottles = m // price
change = m % price

c10 = change // 10
change %= 10
c5 = change // 5
change %= 5
c1 = change

print(f"กดน้ำได้ {bottles} ขวด")
print(f"เงินทอน {c10 * 10 + c5 * 5 + c1} บาท")
print(f"10บาท: {c10}, 5บาท: {c5}, 1บาท: {c1}\n")

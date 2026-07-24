money = 1000

while money > 0:
    withdraw = int(input())
    money -= withdraw
    print("==========")
    print("Money left : ", money)

print("==========")
print("ATM CLOSED")
print("==========")
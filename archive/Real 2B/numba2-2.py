x = int(input("Enter a number: "))

coin = 0

while x >= 9 :
    newcoin = x // 9
    coin += newcoin
    x = newcoin + (x % 9)

print(coin)
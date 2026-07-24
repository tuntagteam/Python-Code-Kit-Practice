money = int(input())
ten = 0
five = 0
two = 0
one = 0

ten = money // 10
money = money % 10
five = money // 5
money = money % 5
two = money // 2
money = money % 2
one = money;

print("10: ", ten)
print("5 :", five)
print("2 :", two)
print("1 :", one)



print(f"10:",ten,"\n5:",five,"\n2:",two,"\n1:",one)
age = int(input())
status = input()

if age <= 18 or status in ("s", "S" ):
    print(20)
else:
    print(50)
user_input = input("Winner Names (With Space): ")
winners = user_input.strip().split()

for index, name in enumerate(winners, start=1):
    print(index)
    print(name)



    
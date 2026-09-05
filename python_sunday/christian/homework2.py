balance = 0
running = True

while running:
    print("=======================")
    print("Welcome to Tag's Bank")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Show Balance")
    print("=======================")
    print("9. Exit")
    print("=======================")

    x = int(input("Enter your choice : "))

    if x == 1:
        print("=======================")
        print("How much do you want to deposit?")

        amount = float(input("Amount : "))

        if amount > 0:
            balance = balance + amount
            print("Deposit Successful!")
            print("Balance :", balance)
        else:
            print("Amount must be more than 0!")

    elif x == 2:
        print("=======================")
        print("How much do you want to withdraw?")

        amount = float(input("Amount : "))

        if amount <= 0:
            print("Amount must be more than 0!")

        elif amount > balance:
            print("Not enough balance!")

        else:
            balance = balance - amount
            print("Withdraw Successful!")
            print("Balance :", balance)

    elif x == 3:
        print("=======================")
        print("Balance :", balance)

    elif x == 9:
        print("=======================")
        print("Thank you for using us!")
        print("=======================")
        running = False

    else:
        print("Wrong Process!")

    print()
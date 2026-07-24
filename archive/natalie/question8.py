balance = 0

while True:
    print("\n1. Deposit")
    print("2. Withdraw")
    print("3. Check Balance")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        amount = float(input("Enter deposit amount: "))
        balance += amount
        print("Deposit successful.")
    elif choice == "2":
        amount = float(input("Enter withdraw amount: "))

        if amount <= balance:
            balance -= amount
            print("Withdraw successful.")
        else:
            print("Not enough balance.")
    elif choice == "3":
        print("Balance =", balance)
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid option.")

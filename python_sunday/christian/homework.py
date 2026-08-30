# Do anything that include Print Input If else and while except number game
print("=== SECRET DOOR ADVENTURE ===")

password = ""

while password != "dragon":
    password = input("Enter the secret password: ")

    if password == "dragon":
        print("The door opens!")
    else:
        print("Wrong password. Try again.")

print("\nYou enter a mysterious room.")

playing = True

while playing:
    print("\nWhat do you want to do?")
    print("1. Open the chest")
    print("2. Enter the dark tunnel")
    print("3. Drink the mysterious potion")
    print("4. Leave the room")

    choice = input("Choose 1-4: ")

    if choice == "1":
        print("You found a golden key!")

    elif choice == "2":
        answer = input("A monster appears! Run or Fight? ").lower()

        if answer == "run":
            print("You escaped safely!")
        elif answer == "fight":
            print("You defeated the monster!")
        else:
            print("You stood there confused...")

    elif choice == "3":
        print("You drink the potion.")

        answer = input("Do you feel GOOD or BAD? ").lower()

        if answer == "good":
            print("You gained super strength!")
        else:
            print("Your hair turned blue!")

    elif choice == "4":
        print("You leave the mysterious room.")
        playing = False

    else:
        print("Invalid choice.")

print("GAME OVER")
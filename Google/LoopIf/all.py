# ==============================
# 0-15 min: Game - Should I Eat It?
# ==============================

foods = ["apple", "chocolate", "carrot", "candy", "banana", "fries", "grapes", "pizza"]

for food in foods:
    print ("\nFood:", food)

    # Check if it's a fruit
    if food in ["apple", "banana", "grapes"]:
        print ("Is it a fruit? Yes!")
        print ("Is it healthy? Yes, go ahead and eat it!")

    # Check if it's a healthy veggie
    elif food == "carrot":
        print ("Is it a fruit? No.")
        print ("Is it healthy? Yes, great choice!")

    # Check for unhealthy snacks
    elif food in ["chocolate", "candy", "fries", "pizza"]:
        print ("Is it a fruit? No.")
        print ("Is it healthy? Not really...")
        print ("Maybe save it for a special day!")

    # Just in case
    else:
        print ("I don't know that food. Be careful!")


# ==============================
# 15-30 min: Mini-Lesson - if, elif, else
# ==============================

number = int(raw_input("\nEnter any number: "))

if number > 0:
    print ("That's a positive number!")
elif number < 0:
    print ("That's a negative number!")
else:
    print ("That's zero!")


# ==============================
# 30-45 min: Challenge - Snack Classifier
# ==============================

snacks = ["apple", "chips", "banana", "candy", "carrot"]

for snack in snacks:
    if snack in ["apple", "banana", "carrot"]:
        print (snack.title(), "is a healthy snack!")
    else:
        print (snack.title(), "is a treat – eat it sometimes!")


# ==============================
# 45-55 min: Big Challenge - Kid Budget Checker
# ==============================

items = {
    "book": 8.50,
    "lego": 12.00,
    "chips": 2.50,
    "pencil": 1.25
}

cart = ["book", "lego", "chips"]
total = 0

for item in cart:
    price = items[item]
    print ("Added"), item + ":", "$%.2f" % price
    total += price

print ("Total: $%.2f" % total)

if total > 20:
    print ("You're over budget!")
else:
    print( "You're within budget!")


# ==============================
# 55-60 min: Discussion - Plan your own project
# ==============================

# You could ask: 
# "What if we made a program that sorts your toys by type?"
# or
# "What if we track your exercise over a week and give messages based on how much you moved?"
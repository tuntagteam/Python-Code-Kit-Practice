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
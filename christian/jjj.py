food_brand = ["McDonalds","KFC","Burkey Queen","Dairy King","Pizza Castle"]
food_food = ["SmallMac","Biscuits","Whoppy","Blizzarrrd","Pepperoni"]

print(*food_brand)
print(*food_food)

for food_brand,food_food in zip(food_brand,food_food):
    print(f"I went to {food_brand} to order {food_food}")

for i in food_food:
    print(food_food[i])
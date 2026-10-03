# Enter a number: 100

# 1 is Odd
# 2 is Even
# 3 is Odd
# 4 is Even
# 5 is Odd
# 6 is Even
# ...
# 100 is Even

food_brand = ["McDonalds","KFC","Burkey Queen","Dairy King","Pizza Castle"]
food_food = ["SmallMac","Biscuits","Whoppy","Blizzarrrd","Pepperoni"]

print(*food_brand)
print(*food_food)

for food_brand,food_food in zip(food_brand,food_food):
    print(f"I went to {food_brand} to order {food_food}")

for i in food_food:
    print(food_food[i])
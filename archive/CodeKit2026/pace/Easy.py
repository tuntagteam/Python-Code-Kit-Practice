# # Python Problem — Smart Vending Machine 🥤

# A beverage shop has an automatic vending machine.
# One glass of water costs 12 baht.
# The customer inserts money.
# Then they choose how many glasses to buy.

# The program should calculate:
# * The total amount to be paid.
# * Whether the customer has enough money.
# * If there is enough money, how much change should be given?

# # Example 1

# ### Input
# 50
# 3

# Meaning:
# * Has 50 baht
# * Buys 3 glasses

# ### Output
# Total = 36
# Change = 14

# # Example 2

# ### Input
# 20
# 2

# ### Output
# Total = 24
# Not enough money

x=int(input())
y=int(input())
z=y*12
u=x-z
if z > x:
    print("Total = ",z)
    print("Not enough money")
else:
    print("Total",z)
    print("Change = ",u)
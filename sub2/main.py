username = input("Enter your username :")
password = input("Enter your password :")

if username == "truecs" and password == "python123":
    print("Logged in!")
elif username == "truecs" and password != "python123":
    print("Incorrect Password")
elif username != "truecs" and password == "python123":
    print("Incorrect Username")
else:
    print("Wrong")
# +
# -
# *
# /
# // หารแบบไม่เอา Remainder
# % Mod หารเอาแต่ Remainder

# 6/3 = 2.0
# 6//3 = 2
# 6%3 = 0

# print(14/3) # All
# print(14//3) # No remainder
# print(14%3) # Remainder Only

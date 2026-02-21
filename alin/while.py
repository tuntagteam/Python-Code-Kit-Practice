secret = 2
guess = int(input("Enter Guess"))

while guess != secret:
    print("Wrong")
    guess = int(input("Enter Guess"))

print("Correct you are the best")
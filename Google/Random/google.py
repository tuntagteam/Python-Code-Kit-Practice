import random

lower_bound = 1
upper_bound = 100

# Generate a random number
secret_number = random.randint(lower_bound, upper_bound)
attempts = 0

print("Welcome to the Number Guessing Game!")
print(f"I'm thinking of a number between {lower_bound} and {upper_bound}.")

while True:
    guess_input = input("Enter your guess: ")

    if guess_input.isdigit():
        guess = int(guess_input)
        attempts += 1

        if guess < lower_bound or guess > upper_bound:
            print(f"Please guess a number within the range {lower_bound}-{upper_bound}.")
        elif guess < secret_number:
            print("Too low! Try again.")
        elif guess > secret_number:
            print("Too high! Try again.")
        else:
            print(f"Congratulations! You guessed the number {secret_number} in {attempts} attempts.")
            break
    else:
        print("Invalid input. Please enter a whole number.")
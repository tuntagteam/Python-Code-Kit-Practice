import random

def guessing_game():
    secret = random.randint(1, 100)
    tries = 0

    print("I'm thinking of a number between 1 and 100.")
    while True:
        guess = input("Your guess: ").strip()
        # ตรวจสอบว่าเป็นตัวเลขหรือไม่
        if not guess.isdigit():
            print("Please enter a valid integer.")
            continue

        guess = int(guess)
        tries += 1

        if guess < secret:
            print("Too low.")
        elif guess > secret:
            print("Too high.")
        else:
            print(f"You got it in {tries} tries!")
            break

if __name__ == "__main__":
    guessing_game()
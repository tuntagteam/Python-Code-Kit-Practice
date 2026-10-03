import random

print("===============")
print("Welcome to the guess game!")
print("Enter the number between 1-10")
print("===============")
question = random.randint(1,10)
answer = int(input("Enter your guess : "))

attempts = 0

while question != answer: 
    # != is not equal sign. So that's mean question is not equal with answer
    print("Incorrect!")
    attempts += 1
    # attempts = attempts + 1
    if answer > question:
        print("Too High! Try Lower.")
    else:
        print("Too Low! Try Higher.")
    answer = int(input("Enter your guess : "))

print("===============")
print("Correct!")
print(f"You got it in {attempts} tries!")
if attempts > 7:
    print("You are Noob! 😂")
elif attempts > 4:
    print("You are Pro! 😎")
elif attempts > 1:
    print("You are Hacker! 😱")
else:
    print("You are GOD🔥😱")
print("===============")
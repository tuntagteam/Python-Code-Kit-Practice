# 1. Introduce Yourself
print("1. Introduce Yourself")
name = input("Enter your name: ")
age = input("Enter your age: ")
print(f"Hello, {name}! You are {age} years old.")

# 2. Even or Odd
print("2. Even or Odd")
number = int(input("Enter an integer: "))
if number % 2 == 0:
    print("Even")
else:
    print("Odd")

# 3. Positive, Negative, or Zero
print("3. Positive, Negative, or Zero")
number = float(input("Enter a number: "))
if number > 0:
    print("Positive")
elif number < 0:
    print("Negative")
else:
    print("Zero")

# 4. Largest of Two Numbers
print("4. Largest of Two Numbers")
first_number = float(input("Enter the first number: "))
second_number = float(input("Enter the second number: "))
if first_number > second_number:
    print(f"The larger number is {first_number}.")
elif second_number > first_number:
    print(f"The larger number is {second_number}.")
else:
    print("The two numbers are equal.")

# 5. Pass or Fail
print("5. Pass or Fail")
score = float(input("Enter a score from 0 to 100: "))
if score >= 50:
    print("Pass")
else:
    print("Fail")

# 6. Counting with for
print("6. Counting with for")
n = int(input("Enter a positive integer: "))
for current_number in range(1, n + 1):
    print(current_number)

# 7. Multiplication Table
print("7. Multiplication Table")
table_number = int(input("Enter a number: "))
for multiplier in range(1, 11):
    product = table_number * multiplier
    print(f"{table_number} x {multiplier} = {product}")

# 8. Sum from 1 to n
print("8. Sum from 1 to n")
n = int(input("Enter a positive integer: "))
total = 0
for current_number in range(1, n + 1):
    total += current_number
print(f"The sum from 1 to {n} is {total}.")

# 9. Password Checker
print("9. Password Checker")
password = input("Enter the password: ")
while password != "python123":
    print("Incorrect password. Try again.")
    password = input("Enter the password: ")
print("Access granted")

# 10. Guess the Number
print("10. Guess the Number")
secret_number = 7
guess = int(input("Guess the secret number: "))
while guess != secret_number:
    if guess > secret_number:
        print("Too high")
    else:
        print("Too low")
    guess = int(input("Guess again: "))
print("Correct!")

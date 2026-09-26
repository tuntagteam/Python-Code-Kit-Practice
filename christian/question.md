# Python Exercises

## 1. Greeting Program

Write a program that asks the user for their name and age, then prints a greeting message.

### Input Example
```text
Enter your name: Alex
Enter your age: 15
```

### Output Example
```text
Hello Alex!
You are 15 years old.
```

---

## 2. Simple Calculator

Write a program that asks the user for two numbers.

Print:

- Addition
- Subtraction
- Multiplication
- Division

### Input Example
```text
Enter first number: 10
Enter second number: 5
```

### Output Example
```text
Addition: 15
Subtraction: 5
Multiplication: 50
Division: 2.0
```

---

## 3. Even or Odd

Write a program that asks the user for a number.

Use `if` and `else` to check whether the number is even or odd.

### Input Example
```text
Enter a number: 7
```

### Output Example
```text
7 is odd.
```

### Another Example
```text
Enter a number: 10
```

```text
10 is even.
```

---

## 4. Grade Checker

Write a program that asks the user for a score from `0` to `100`.

Display the grade using these rules:

- `80 - 100` → A
- `70 - 79` → B
- `60 - 69` → C
- `50 - 59` → D
- Below `50` → F

### Input Example
```text
Enter your score: 76
```

### Output Example
```text
Grade: B
```

---

## 5. Multiplication Table

Write a program that asks the user for a number.

Use a `for` loop to display its multiplication table from `1` to `12`.

### Input Example
```text
Enter a number: 5
```

### Output Example
```text
5 x 1 = 5
5 x 2 = 10
5 x 3 = 15
5 x 4 = 20
5 x 5 = 25
5 x 6 = 30
5 x 7 = 35
5 x 8 = 40
5 x 9 = 45
5 x 10 = 50
5 x 11 = 55
5 x 12 = 60
```

---

## 6. Number Guessing

Create a secret number with the value `7`.

Ask the user to guess the number.

Use a `while` loop to keep asking until the user guesses correctly.

### Input Example
```text
Guess the number: 3
Guess the number: 10
Guess the number: 7
```

### Output Example
```text
Wrong! Try again.
Wrong! Try again.
Correct!
```

---

## 7. Shopping List

Write a program that asks the user to enter `5` shopping items.

Store all items inside a `list`.

After all items are entered, print the complete shopping list.

### Input Example
```text
Item 1: Milk
Item 2: Bread
Item 3: Eggs
Item 4: Apple
Item 5: Chicken
```

### Output Example
```text
Shopping List:
Milk
Bread
Eggs
Apple
Chicken
```

---

## 8. Find the Highest Number

Write a program that asks the user to enter `5` numbers.

Store the numbers inside a `list`.

Find and print the highest number.

### Input Example
```text
Enter number 1: 12
Enter number 2: 45
Enter number 3: 7
Enter number 4: 30
Enter number 5: 21
```

### Output Example
```text
Highest number: 45
```

---

## 9. Create a Function

Create a function called:

```python
calculate_area(width, height)
```

The function should calculate and return the area of a rectangle.

Ask the user for the width and height, then call the function.

### Input Example
```text
Enter width: 8
Enter height: 5
```

### Output Example
```text
Area: 40
```

---

## 10. Student Score System

Write a program that asks how many students you want to enter.

For each student, ask for:

- Name
- Score

Store the student names and scores.

Use a function called:

```python
get_grade(score)
```

The function should return:

- `A` if score is `80` or higher
- `B` if score is `70-79`
- `C` if score is `60-69`
- `D` if score is `50-59`
- `F` if score is below `50`

After entering all students, print every student's name, score, and grade.

### Input Example
```text
How many students: 3

Student name: Alex
Score: 85

Student name: Bob
Score: 72

Student name: Jane
Score: 45
```

### Output Example
```text
Alex - 85 - Grade A
Bob - 72 - Grade B
Jane - 45 - Grade F
```
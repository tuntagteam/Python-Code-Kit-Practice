# Python Homework Exercises

## 1. Pocket Money Tracker

Write a program that asks the user how much pocket money they receive each day and how many days they save it.

Calculate the total amount of money saved.

If the total is `100` or more, print:

```text
Great job saving!
```

Otherwise print:

```text
Keep saving!
```

### Input Example
```text
Pocket money per day: 20
Number of days: 7
```

### Output Example
```text
Total saved: 140
Great job saving!
```

---

## 2. Number Counter

Write a program that asks the user for a number.

Use a `for` loop to print every number from `1` up to that number.

After that, print the total of all the numbers.

### Input Example
```text
Enter a number: 5
```

### Output Example
```text
1
2
3
4
5
Total: 15
```

---

## 3. Game Score Bonus

Write a program that asks the user for their game score.

Use these rules:

- Score `100` or higher → add `50` bonus points
- Score `50-99` → add `20` bonus points
- Score below `50` → no bonus points

Print the original score, bonus points, and final score.

### Input Example
```text
Enter score: 80
```

### Output Example
```text
Score: 80
Bonus: 20
Final score: 100
```

---

## 4. Favorite Food List

Ask the user how many favorite foods they want to enter.

Use a `for` loop to ask for each food and store them inside a `list`.

After that, print all foods with numbers starting from `1`.

### Input Example
```text
How many foods: 3
Food: Pizza
Food: Sushi
Food: Burger
```

### Output Example
```text
1. Pizza
2. Sushi
3. Burger
```

---

## 5. Count Big Numbers

Ask the user to enter `5` numbers.

Store the numbers inside a `list`.

Count how many numbers are greater than `10`.

### Input Example
```text
Number 1: 5
Number 2: 12
Number 3: 25
Number 4: 3
Number 5: 18
```

### Output Example
```text
Numbers greater than 10: 3
```

---

## 6. Simple ATM

Start with:

```python
money = 100
```

Use a `while` loop to keep asking the user how much money they want to spend.

If the amount is less than or equal to the money left, subtract it.

If the amount is greater than the money left, print:

```text
Not enough money!
```

The program stops when the money reaches `0`.

### Input Example
```text
You have: 100
Spend: 30
You have: 70
Spend: 20
You have: 50
Spend: 50
```

### Output Example
```text
Money left: 70
Money left: 50
Money left: 0
No money left!
```

---

## 7. Find Even Numbers

Ask the user to enter `6` numbers.

Store all numbers inside a `list`.

Use a `for` loop and `if` statement to print only the even numbers.

### Input Example
```text
Number 1: 3
Number 2: 8
Number 3: 11
Number 4: 20
Number 5: 5
Number 6: 14
```

### Output Example
```text
Even numbers:
8
20
14
```

---

## 8. Temperature Checker Function

Create a function called:

```python
check_temperature(temp)
```

The function should return:

- `"Cold"` if the temperature is below `20`
- `"Warm"` if the temperature is from `20` to `29`
- `"Hot"` if the temperature is `30` or higher

Ask the user for a temperature and call the function.

### Input Example
```text
Enter temperature: 32
```

### Output Example
```text
Weather: Hot
```

---

## 9. Mini Shop

Create these two lists:

```python
items = ["Apple", "Milk", "Bread"]
prices = [10, 25, 30]
```

Print the shop menu.

Ask the user to choose an item number.

Then ask how many they want.

Calculate the total price.

### Input Example
```text
1. Apple - 10
2. Milk - 25
3. Bread - 30

Choose item: 2
How many: 3
```

### Output Example
```text
You bought Milk
Amount: 3
Total: 75
```

---

## 10. Student Score Analyzer

Create a function called:

```python
get_grade(score)
```

The function should return:

- `A` for `80-100`
- `B` for `70-79`
- `C` for `60-69`
- `D` for `50-59`
- `F` for below `50`

Ask the user how many students they want to enter.

Use a `for` loop to ask for each student's name and score.

Store the names and scores inside lists.

After entering everyone, print each student's name, score, and grade.

Also count how many students passed.

A student passes if their score is `50` or higher.

### Input Example
```text
How many students: 4

Name: Tom
Score: 82

Name: Anna
Score: 65

Name: Max
Score: 40

Name: Lily
Score: 75
```

### Output Example
```text
Tom - 82 - Grade A
Anna - 65 - Grade C
Max - 40 - Grade F
Lily - 75 - Grade B

Students passed: 3
```

---

## 11. Password Guess Game

Set the password to:

```python
password = "python"
```

Use a `while` loop to keep asking the user to enter the password.

Count how many attempts the user makes.

Stop when the password is correct.

### Input Example
```text
Password: hello
Password: game
Password: python
```

### Output Example
```text
Wrong password!
Wrong password!
Correct password!
Attempts: 3
```

---

## 12. Number List Analyzer

Ask the user to enter `5` numbers and store them in a list.

Create a function called:

```python
analyze_numbers(numbers)
```

The function should calculate:

- Total of all numbers
- Highest number
- Lowest number
- How many numbers are even
- How many numbers are odd

### Input Example
```text
Number 1: 5
Number 2: 8
Number 3: 2
Number 4: 11
Number 5: 6
```

### Output Example
```text
Total: 32
Highest: 11
Lowest: 2
Even numbers: 3
Odd numbers: 2
```
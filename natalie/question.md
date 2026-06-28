# Python Practice Worksheet: Basic to Medium

**Objective / เป้าหมาย:**  
Practice applying Python basics to solve small programming problems.  
ฝึกใช้พื้นฐาน Python เพื่อแก้โจทย์สั้น ๆ แบบค่อย ๆ เพิ่มความยาก

**Estimated Time / เวลาที่ใช้:** 60-90 minutes  
**Do not write full answers here / ยังไม่ต้องดูเฉลย:** Try solving each question by yourself first.

**Topics / หัวข้อที่ใช้:** variables, input/output, if/else, loops, lists, dictionaries, functions, and basic classes

---

## Question 1: Even or Odd

### Scenario / สถานการณ์

A user enters a number.  
ผู้ใช้กรอกตัวเลขเข้ามา 1 ตัว

### Task / งานที่ต้องทำ

Write a program that checks whether the number is **Even** or **Odd**.  
เขียนโปรแกรมเพื่อตรวจสอบว่าตัวเลขนั้นเป็น **เลขคู่** หรือ **เลขคี่**

### Example / ตัวอย่าง

```text
Input:
7

Output:
Odd
```

### Concepts / แนวคิดที่ใช้

- `input()`
- `int()`
- `if/else`
- `%`

### Hint / คำใบ้

Use `% 2` to check the remainder. If the remainder is `0`, the number is even.  
ใช้ `% 2` เพื่อดูเศษจากการหาร ถ้าเศษเป็น `0` แปลว่าเป็นเลขคู่

---

## Question 2: Average Score

### Scenario / สถานการณ์

A teacher wants to calculate the average score of 5 students.  
ครูต้องการคำนวณคะแนนเฉลี่ยของนักเรียน 5 คน

### Task / งานที่ต้องทำ

Store the scores in a list and calculate the average score.  
เก็บคะแนนไว้ใน list แล้วคำนวณค่าเฉลี่ย

### Example / ตัวอย่าง

```python
scores = [70, 80, 65, 90, 75]
```

```text
Output:
Average = 76.0
```

### Concepts / แนวคิดที่ใช้

- list
- `sum()`
- `len()`

### Hint / คำใบ้

The average is the total score divided by the number of scores.  
ค่าเฉลี่ยคือคะแนนรวม หารด้วยจำนวนคะแนนทั้งหมด

---

## Question 3: Count Even Numbers

### Scenario / สถานการณ์

You are given a list of numbers.  
มี list ของตัวเลขให้มา

### Task / งานที่ต้องทำ

Count how many numbers in the list are even.  
นับว่ามีเลขคู่ทั้งหมดกี่ตัวใน list

### Example / ตัวอย่าง

```python
numbers = [4, 7, 2, 9, 10, 13]
```

```text
Output:
There are 3 even numbers.
```

### Concepts / แนวคิดที่ใช้

- `for` loop
- `if`
- `%`

### Hint / คำใบ้

Create a counter variable before the loop. Increase it every time you find an even number.  
สร้างตัวแปรสำหรับนับก่อนเริ่ม loop แล้วเพิ่มค่าทุกครั้งที่เจอเลขคู่

---

## Question 4: Student Grade

### Scenario / สถานการณ์

A teacher wants to convert a student score into a letter grade.  
ครูต้องการแปลงคะแนนของนักเรียนให้เป็นเกรดตัวอักษร

### Task / งานที่ต้องทำ

Ask the user to enter a score, then print the correct grade.  
ให้ผู้ใช้กรอกคะแนน จากนั้นแสดงเกรดที่ถูกต้อง

### Rules / เงื่อนไข

| Score / คะแนน | Grade / เกรด |
|---|---|
| 80-100 | A |
| 70-79 | B |
| 60-69 | C |
| 50-59 | D |
| Below 50 / ต่ำกว่า 50 | F |

### Example / ตัวอย่าง

```text
Input:
74

Output:
Grade B
```

### Concepts / แนวคิดที่ใช้

- `if`
- `elif`
- `else`

### Hint / คำใบ้

Check the highest grade range first, then continue with lower ranges using `elif`.  
เริ่มตรวจจากช่วงคะแนนที่สูงที่สุดก่อน แล้วค่อยใช้ `elif` ตรวจช่วงที่ต่ำลงมา

---

## Question 5: Shopping Cart

### Scenario / สถานการณ์

A customer has several items in a shopping cart.  
ลูกค้ามีสินค้าหลายชิ้นอยู่ในตะกร้า

### Task / งานที่ต้องทำ

Calculate the total cost of all items.  
คำนวณราคารวมของสินค้าทั้งหมด

### Example / ตัวอย่าง

```python
prices = [50, 120, 30, 200]
```

```text
Output:
Total = 400
```

### Concepts / แนวคิดที่ใช้

- list
- loop
- accumulator

### Hint / คำใบ้

Start with `total = 0`, then add each price to `total` inside the loop.  
เริ่มจาก `total = 0` แล้วบวกราคาของแต่ละสินค้าเข้าไปใน `total` ภายใน loop

---

## Question 6: Create a Function

### Scenario / สถานการณ์

You want to reuse code for calculating the area of a rectangle.  
ต้องการเขียนโค้ดคำนวณพื้นที่สี่เหลี่ยมผืนผ้าให้ใช้ซ้ำได้

### Task / งานที่ต้องทำ

Write a function named `calculate_area()` that receives width and height, then returns the area.  
เขียน function ชื่อ `calculate_area()` ที่รับความกว้างและความสูง แล้ว return พื้นที่

### Example / ตัวอย่าง

```python
calculate_area(5, 8)
```

```text
Output:
40
```

### Concepts / แนวคิดที่ใช้

- `def`
- parameters
- `return`

### Hint / คำใบ้

The area of a rectangle is width multiplied by height.  
พื้นที่สี่เหลี่ยมผืนผ้าคือความกว้างคูณความสูง

---

## Question 7: Student Dictionary

### Scenario / สถานการณ์

You need to store student information in one variable.  
ต้องการเก็บข้อมูลนักเรียนไว้ในตัวแปรเดียว

### Task / งานที่ต้องทำ

Create a dictionary with student information, then print each value clearly.  
สร้าง dictionary สำหรับข้อมูลนักเรียน แล้วแสดงผลแต่ละค่าให้อ่านง่าย

### Example / ตัวอย่าง

```python
student = {
    "name": "John",
    "age": 15,
    "grade": "A"
}
```

```text
Output:
Name : John
Age : 15
Grade : A
```

### Concepts / แนวคิดที่ใช้

- dictionary
- key/value

### Hint / คำใบ้

Use the dictionary keys, such as `"name"` and `"age"`, to access each value.  
ใช้ key ของ dictionary เช่น `"name"` และ `"age"` เพื่อดึงค่าข้อมูลออกมา

---

## Question 8: Simple ATM Menu

### Scenario / สถานการณ์

You are creating a simple ATM program.  
กำลังสร้างโปรแกรม ATM แบบง่าย

### Task / งานที่ต้องทำ

Create a menu that lets the user deposit money, withdraw money, check balance, or exit. The menu should repeat until the user chooses Exit.  
สร้างเมนูให้ผู้ใช้ฝากเงิน ถอนเงิน เช็กยอดเงิน หรือออกจากโปรแกรม โดยเมนูต้องแสดงซ้ำจนกว่าผู้ใช้จะเลือกออก

### Menu / เมนู

```text
1. Deposit
2. Withdraw
3. Check Balance
4. Exit
```

### Concepts / แนวคิดที่ใช้

- `while` loop
- `if`
- variables

### Hint / คำใบ้

Keep the balance in one variable. Use a `while` loop so the menu keeps running until option `4` is selected.  
เก็บยอดเงินไว้ในตัวแปรเดียว แล้วใช้ `while` loop เพื่อให้เมนูทำงานต่อไปจนกว่าจะเลือกข้อ `4`

---

## Question 9: Create a Dog Class

### Scenario / สถานการณ์

You want to create a simple object that represents a dog.  
ต้องการสร้าง object แบบง่ายที่แทนสุนัขหนึ่งตัว

### Task / งานที่ต้องทำ

Create a class called `Dog` with `name` and `age` properties. Add a method called `bark()` that prints a message.  
สร้าง class ชื่อ `Dog` ที่มี properties คือ `name` และ `age` แล้วเพิ่ม method ชื่อ `bark()` เพื่อแสดงข้อความ

### Example / ตัวอย่าง

```python
dog = Dog("Buddy", 3)
dog.bark()
```

```text
Output:
Buddy says Woof!
```

### Concepts / แนวคิดที่ใช้

- class
- `__init__`
- `self`
- methods

### Hint / คำใบ้

Use `__init__` to save the dog's name and age. Inside `bark()`, use `self.name` to include the dog's name in the message.  
ใช้ `__init__` เพื่อเก็บชื่อและอายุของสุนัข แล้วใน `bark()` ใช้ `self.name` เพื่อแสดงชื่อในข้อความ

---

## Question 10: Student Management

### Scenario / สถานการณ์

You are building a basic student management program using OOP.  
กำลังสร้างโปรแกรมจัดการข้อมูลนักเรียนแบบง่ายโดยใช้ OOP

### Task / งานที่ต้องทำ

Create a class called `Student` with `name` and `score` properties. Add methods named `display_info()` and `is_pass()`. The passing score is `50`.  
สร้าง class ชื่อ `Student` ที่มี properties คือ `name` และ `score` แล้วเพิ่ม methods ชื่อ `display_info()` และ `is_pass()` โดยคะแนนผ่านคือ `50`

### Example / ตัวอย่าง

```text
Output:
Name : Alice
Score : 78
Status : Pass
```

### Concepts / แนวคิดที่ใช้

- class
- methods
- `if/else`
- `return`

### Hint / คำใบ้

Let `is_pass()` return `True` or `False`, then use that result inside `display_info()` to print the status.  
ให้ `is_pass()` return เป็น `True` หรือ `False` แล้วนำผลลัพธ์นั้นไปใช้ใน `display_info()` เพื่อแสดงสถานะ

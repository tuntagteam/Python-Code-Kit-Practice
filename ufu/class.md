## โจทย์ทดสอบเรื่อง Class: ข้อมูลนักเรียน

ให้นักเรียนสร้าง Class ชื่อ `Student` สำหรับเก็บข้อมูลนักเรียน โดยมีข้อมูลดังนี้

- ชื่อนักเรียน
- อายุ
- คะแนนสอบ

ภายใน Class ให้มี Method ชื่อ `show_info()` สำหรับแสดงข้อมูลนักเรียนและผลสอบ

เกณฑ์ผลสอบ:

- คะแนนตั้งแต่ 50 ขึ้นไป แสดง `Pass`
- คะแนนต่ำกว่า 50 แสดง `Fail`

### ตัวอย่างการใช้งาน

```python
student1 = Student("Pace", 9, 85)
student1.show_info()
```

### Output

```text
Name: Pace
Age: 9
Score: 85
Result: Pass
```

## โจทย์ทดสอบ Class: ระบบบัญชีธนาคาร

ให้นักเรียนสร้าง Class ชื่อ `BankAccount` สำหรับจำลองบัญชีธนาคารอย่างง่าย

### ข้อมูลใน Class

ใช้ `__init__()` รับข้อมูล:

- `owner` ชื่อเจ้าของบัญชี
- `balance` ยอดเงินเริ่มต้น



### Method ที่ต้องสร้าง

1. `deposit(amount)`
  ฝากเงินเข้าบัญชี และแสดงยอดเงินคงเหลือ
2. `withdraw(amount)`
  ถอนเงินออกจากบัญชี โดยมีเงื่อนไข:
  - ถ้ายอดเงินเพียงพอ ให้ถอนเงินได้
  - ถ้ายอดเงินไม่เพียงพอ ให้แสดง `Insufficient balance`
  - ถ้าจำนวนเงินที่ฝากหรือถอนน้อยกว่าหรือเท่ากับ `0` ให้แสดง `Invalid amount`
3. `show_balance()`
  แสดงชื่อเจ้าของบัญชีและยอดเงินปัจจุบัน



### ตัวอย่างการใช้งาน

```python
account1 = BankAccount("Alex", 1000)

account1.deposit(500)
account1.withdraw(300)
account1.withdraw(2000)
account1.show_balance()
```



### Output ตัวอย่าง

```text
Deposit: 500
Balance: 1500

Withdraw: 300
Balance: 1200

Insufficient balance

Owner: Alex
Balance: 1200
```


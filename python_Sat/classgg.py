class BankAccount:
    def __init__(self, account_number, account_holder_name, initial_balance=0.0):
        self.account_number = account_number
        self.account_holder_name = account_holder_name
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited {amount}. New balance: {self.balance}"
        else:
            return "Invalid deposit amount. Please enter a positive number."

    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                return f"Withdrew {amount}. New balance: {self.balance}"
            else:
                return "Insufficient balance."
        else:
            return "Invalid withdrawal amount. Please enter a positive number."

    def get_balance(self):
        return self.balance
    
def main():
    account = BankAccount("1234567890", "John Doe", 1000.0)
    print(account.deposit(500.0))
    print(account.withdraw(200.0))
    print(account.get_balance())

if __name__ == "__main__":
    main()  
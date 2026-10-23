
import random

class BankAccount:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    def show_balance(self):
        print(f"[{self.account_number}] balance = ${self.balance}")

    def deposit(self, amount):
        self.balance += amount
        print(f"+ ${amount}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"[{self.account_number}] -${amount}")
        else:
            print(f"Not enough money")


class Student:
    def __init__ (self, name, age, bankAccount: BankAccount):
        self.name = name
        self.age = age
        self.skills = 1
        self.money = 100
        self.bankAccount = bankAccount

    def info (self):
        print(f"Hi my name is {self.name} and I am {self.age} years old.")
        print(f"Skills: {self.skills}")
        print(f"Money: ${self.money}")
        print(f"Deposit: ${self.bankAccount.balance}")

    def study(self):
        self.skills += random.randint( 0, 1)
        print("Time to study")

    def chill(self):
        expenses = random.randint( 25, 100)
        if expenses <= self.money:
            self.money -= expenses
        else:
            self.bankAccount.withdraw(expenses)

        self.skills -= 0.5
        print("Time to chill ")

    def work(self):
        self.skills += 0.5
        income = 50 + random.randint( 0, 50)
        amount = random.randint( 0, income)

        self.bankAccount.deposit(amount)
        self.money += income - amount

        print("Hard working ...")

mono = BankAccount("Mon", 100)

vasya = Student("Vasya", 13, mono)

vasya.info()

for day in range(366):
    vasya_choice = random.randint( 1, 3)
    if vasya_choice == 1:
        vasya. work()
    elif vasya_choice == 2:
        vasya.chill()
    else:
        vasya.study()

vasya.age += 1
vasya.info()

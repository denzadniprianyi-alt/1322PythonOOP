import random

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.skills = 1
        self.money = 100

    def info (self):
        print(f"Hi my name is {self.name} and I am {self.age} years old.")
        print(f"Skills: {self.skills}")
        print(f"Money: ${self.money}")

    def study(self):
        self.skills += random.randint(0, 1)
        print("Time to study 📚📚")

    def chill(self):
        self.money -= random.randint(25, 100)
        self.skills -= 0.5
        print("Time to chill 😎🐐")

    def work(self):
        self.skills += 0.5
        self.money += 50 + random.randint(0, 50)
        print("Hard working... 👷👷")

ira = Student("Ira", 12)
vasya = Student("Vasya", 13)

ira.info()
vasya.info()

for day in range(366):
    vasya_choice = random.randint(1, 3)
    if vasya_choice == 1:
        vasya.work()
    elif vasya_choice == 2:
        vasya.chill()
    else:
        vasya.study()
    ira_choice = random.randint(1, 3)
    if ira_choice == 1:
        ira.work()
    elif ira_choice == 2:
        ira.chill()
    else:
        ira.study()

vasya.age += 1
vasya.info()
ira.age += 1
ira.info()
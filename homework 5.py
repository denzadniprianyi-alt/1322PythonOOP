from colorama import Fore, Back

try:
    a = float(input("Enter a number: "))

    print(Fore.LIGHTWHITE_EX + Back.LIGHTGREEN_EX + f"{round(a)}")
except ValueError as ve:
    print(Back.RED + Fore.BLACK + "Cannot convert your input to number")
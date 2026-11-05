import colorama
from colorama import Fore, Back, Style, Cursor


help(colorama)
print(dir(colorama))

print("colorama has got 4 modules")
print(Fore.LIGHTRED_EX + "the first one is Fore")
print(Fore.RESET + Back.LIGHTGREEN_EX + "the second one is Back")
print(Fore.RESET + Back.RESET + Style.BRIGHT + "the third one is Style")
print(Fore.RESET + Back.RESET + Style.RESET_ALL + Cursor.UP(1) + "and the last one is Cursor")
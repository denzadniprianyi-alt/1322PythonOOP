d = 0
F = input("Do you know password?")
if F == "yes":
    N = int(input("Enter the password:"))
    if N == 1718:
        print("Correct Password!")
    else:
        print("Wrong Password!")
if F == "no":
    N = int(input("Enter the new password:"))
    print("New Password:")
    print(N)
else:
    print("Invalid answer!")
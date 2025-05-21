
    try:
    num=int(input("Enter a number"))
    result=10/num
    print(result)
except (ZeroDivisionError,ValueError):
    print("Cannot divide by 0")
    print("Invalid number")
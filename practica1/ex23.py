def validate_age(age):
    if (age<0):
        raise ValueError ("Age cannot be negative.")
    else:
        print("Ok")


age=int(input("Enter age"))
validate_age(age)
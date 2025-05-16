class client:
    def __init__(self, id, name, age, password, sold):
        self.id = id
        self.name = name
        self.age = age
        self.password = password
        self.sold = sold



    def afisare(self):
        return f"Id Client: {self.id}, Nume: {self.name}, Varsta: {self.age}, Parola: {self.password} Sold: {self.sold}"

    def __str__(self):

        return f"{self.id},{self.name},{self.age},{self.password},{self.sold}"

    def deposit(self, suma):
        if suma > 0:
            self.sold += suma


            print(f"Depunere reusita. Sold curent: {self.sold}")
        else:
            print("Suma introdusa nu este valida.")






    def retragere(self,suma):
        if (self.sold<suma):
            print(f"Retragere esuata. Sold disponibil: {self.sold}")
        else:


            self.sold-=suma
            print(f"Retragere reusita. Sold curent: {self.sold}")

    def password_change(self,password):
        if (self.password==password):
            passnew=input("Introdu parola noua: ")
            self.password=passnew
            print("Password updated")
        else:
            print("Password wrong. Try again")
from client import client
from admin import admin
import datetime

def incarca_clienti_din_fisier(nume_fisier):
    cont = []
    try:
        with open(nume_fisier, "r") as f:
            for linie in f:
                parts = linie.strip().split(",")
                if len(parts) == 5:
                    id_c, nume, varsta, parola, sold = parts
                    cont.append(client(int(id_c), nume, int(varsta), parola, float(sold)))
    except FileNotFoundError:
        pass 
    return cont


def salveaza_clienti_in_fisier(nume_fisier, lista_clienti):
    with open(nume_fisier, "w") as f:
        for client_obj in lista_clienti:
            f.write(str(client_obj) + "\n")


def main():
    admin_obj = admin("admin", "1234") 
    cont = incarca_clienti_din_fisier("clienti.txt")
    x = datetime.datetime
    print(f"     {x.now()}")
    while True:
        print("\n1. Admin")
        print("2. Client")
        print("0. Iesire")
        try:
            meniugen = int(input("Alege optiunea: "))
        except ValueError:

            print("Introduceti un numar valid.")
            continue
        if meniugen == 1:
            while True:
                numeadmin = input("Introdu nume admin: ")

                paroladmin = input("Introdu parola admin: ")
                if admin_obj.check_admin(numeadmin, paroladmin):
                    while True:
                        print("\n1. Afiseaza toti clientii")
                        print("2. Sterge client")

                        print("3. Iesire")
                        try:


                            meniuadm = int(input("Alege optiunea: "))
                        except ValueError:
                            print("Introduceti un numar valid.")
                            continue

                        if meniuadm==1:
                            for c in cont:
                                print(c.afisare())
                        if meniuadm==2:
                            desters=int(input("Id cont de sters: "))
                            for c in cont:
                                if c.id==desters:
                                    cont.remove(c)
                                    print("\nClient sters cu succes: ")
                                    salveaza_clienti_in_fisier("clienti.txt", cont)

                        elif meniuadm == 3:
                            print("Iesire din modul admin...")
                            break
                        
                else:
                    print("\nCredentiale invalide....")
                    break
                    
            

        elif meniugen == 2:
            while True:
                print("\n1. Afiseaza date")

                print("2. Client nou")
                print("3. Depunere")

                print("4. Retragere")
                print("5. Schimba Parola")


                print("6. Transfer Bancar")
                print("0. Iesire")
                
                try:
                    meniucli = int(input("Alege optiunea: "))
                except ValueError:
                    print("Introduceti un numar valid.")
                    continue

                if meniucli == 1:
                    id1 = int(input("Introdu ID cont: "))
                    verif = 0
                    for c in cont:
                        if c.id == id1:
                            print(c.afisare())
                            verif = 1
                            break
                    if verif == 0:
                        print("\nClient inexistent....")

                elif meniucli == 2:
                    nume = input("Introdu Nume: ")
                    varsta = int(input("Varsta: "))

                    parola = input("Parola: ")
                    sold = float(input("Sold: "))

                    id_nou = cont[-1].id + 1 if cont else 1
                    nou_client = client(id_nou, nume, varsta, parola, sold)

                    cont.append(nou_client)
                    print("Client adaugat cu succes")

                    with open("clienti.txt", "a") as f:
                        f.write(str(nou_client) + "\n")

                elif meniucli == 3:
                    id1 = int(input("Introdu ID cont: "))
                    found = False
                    for c in cont:
                        if c.id == id1:
                            depunere = float(input("Suma de depus: "))
                            c.deposit(depunere)

                            salveaza_clienti_in_fisier("clienti.txt", cont)
                            found = True
                            break
                    if not found:
                        print("\nId invalid......")

                elif meniucli == 4:
                    id1 = int(input("Introdu ID cont: "))
                    pass1 = input("Introdu parola cont: ")
                    found = False
                    for c in cont:
                        if c.id == id1 and c.password == pass1:
                            retragere = float(input("Suma de retras: "))
                            c.retragere(retragere)

                            salveaza_clienti_in_fisier("clienti.txt", cont)
                            found = True

                            break
                    if not found:
                        print("\nId invalid sau parola gresita...")

                elif meniucli == 5:
                    id1 = int(input("Introdu ID cont: "))
                    found = False
                    for c in cont:
                        if c.id == id1:
                            passold = input("Introdu parola veche: ")
                            c.password_change(passold)
                            salveaza_clienti_in_fisier("clienti.txt", cont)
                            found = True
                            break
                    if not found:
                        print("\nId invalid sau parola gresita...")

                elif meniucli == 6:
                    id1 = int(input("Introdu ID cont: "))
                    found = False
                    for c in cont:
                        if c.id == id1:
                            pass1 = input("Introdu parola: ")
                            if c.password == pass1:
                                id2 = int(input("Introdu ID destinatar: "))
                                suma = float(input("Introdu suma de transfer: "))
                                if c.retragere(suma):
                                    found2 = False
                                    for c2 in cont:

                                        if c2.id == id2:
                                            c2.deposit(suma)
                                            salveaza_clienti_in_fisier("clienti.txt", cont)
                                            print("\nTransfer efectuat....")

                                            found2 = True
                                            break
                                    if not found2:
                                        print("\nID destinatar incorect...")
                                found = True
                                break
                            else:
                                print("\nParola incorecta....")
                                found = True
                                break
                    if not found:
                        print("\nID incorect")

                elif meniucli == 0:
                    print("Iesire din modul client...")
                    break
                else:
                    print("Optiune invalida.")
        
        elif meniugen == 0:
            print("Iesire din aplicatie...")
            break

        else:
            print("Optiune invalida.")


if __name__ == "__main__":
    main()

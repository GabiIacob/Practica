class CustomError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"CustomError: {self.message}"


def verifica_numar(numar):
    if numar < 0:
        raise CustomError("Nr nu poate fi negativ.")
    return f"Nr {numar} este valid."

try:
    rezultat = verifica_numar(10)
    print(rezultat)
except CustomError as e:
    print(f"A aparut o eroare: {e}")

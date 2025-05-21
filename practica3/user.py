
class user:
    def __init__(self,id,name,email,password):
        self.id=id
        self.name=name
        self.email=email
        self.password=password
        self.meals = []
    def __str__(self):
        return (f"{self.name} | email: {self.email} | password: {self.password}")

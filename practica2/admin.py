class admin:
    def __init__(self, name, password):
        self.name = "admin"
        self.password = "1234"

    def check_admin(self, name, password):
        if self.name == name and self.password == password:
            return True
        else:
            return False

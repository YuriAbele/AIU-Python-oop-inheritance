from .user import User

class Customer(User):
    """
    Класс, представляющий клиента, наследующий класс User.
    """
    def __init__(self, username, email, address):
        super().__init__(username, email)
        self.address = address

    def __str__(self):
        return f"Клиент: {self.username}, Email: {self.email}, Адрес: {self.address}"

    def get_details(self):
        return self.__str__()
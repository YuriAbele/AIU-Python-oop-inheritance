class User:
    """
    Базовый класс, представляющий пользователя.
    """
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __str__(self):
        return f"Пользователь: {self.username}, Email: {self.email}"

    def get_details(self):
        return self.__str__()

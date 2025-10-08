import hashlib
import uuid

class User:
    """
    Базовый класс, представляющий пользователя.
    """
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

    def __str__(self):
        return f"Пользователь: {self.username}, Email: {self.email}"

    def get_details(self) -> str:
        return self.__str__()

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Хеширование пароля
        """
        password_encoded = password.encode()
        password_salt = uuid.uuid4().bytes
        password_hash = hashlib.sha256(password_encoded + password_salt)
        password_hash_hex = password_hash.hexdigest()
        return password_hash_hex

    @staticmethod
    def check_password(stored_password_hash_hex: str, provided_password: str):
        """
        Проверка пароля.
        """
        return stored_password_hash_hex == User.hash_password(provided_password)

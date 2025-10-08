from .user import User

class Admin(User):
    """
    Класс, представляющий администратора, наследующий класс User.
    """
    def __init__(self, username: str, email: str, password: str, admin_level: int):
        super().__init__(username, email, password)
        self.admin_level = admin_level

    def get_details(self) -> str:
        return f"Admin: {self.username}, Email: {self.email}, Admin-Level: {self.admin_level}"

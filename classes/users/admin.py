from .user import User

class Admin(User):
	"""
	Класс, представляющий администратора, наследующий класс User.
	"""

	def __init__(self, username: str, email: str, password: str, admin_level: int):
		super().__init__(username, email, password)
		self.admin_level = admin_level

	def __str__(self):
		return f"Администратор: {self.username}, Email: {self.email}, Уровень: {self.admin_level}"

	def __repr__(self):
		return f"Admin(username=\"{self.username}\", email=\"{self.email}\", password=\"<CENSORED>\", admin_level={self.admin_level})"

	# По хорошему он вообще не нужен, так как есть __str__
	def get_details(self) -> str:
		return self.__str__()

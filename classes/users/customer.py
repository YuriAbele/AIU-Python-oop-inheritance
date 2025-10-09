from .user import User

class Customer(User):
	"""
	Класс, представляющий клиента, наследующий класс User.
	"""

	def __init__(self, username: str, email: str, password: str, address: str):
		super().__init__(username, email, password)

		# Нормализуем входные данные на случай, если кто-то будет создавать клиента напрямую
		normalized_address = address.strip() # Email может быть с заглавными буквами
		self.address = normalized_address

	def __str__(self):
		return f"Клиент: {self.username}, Email: {self.email}, Адрес: {self.address}"

	def __repr__(self):
		return f"Customer(username=\"{self.username}\", email=\"{self.email}\", password=\"<CENSORED>\", address=\"{self.address}\")"

	# По хорошему он вообще не нужен, так как есть __str__
	def get_details(self) -> str:
		return self.__str__()
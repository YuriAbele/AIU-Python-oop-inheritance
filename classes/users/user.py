import hashlib
import uuid
from classes.users.admin import Admin
from __future__ import annotations

class User:
	"""
	Базовый класс, представляющий пользователя.
	"""
	def __init__(self, username: str, email: str, password: str):
		self.username = username
		self.email = email
		# необходимо хранить хеш пароля, а не сам пароль
		self.password_hash_hex = User.hash_password(password)

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
	def check_password(password_hash_hex: str, password: str):
		"""
		Проверка пароля. Вычисляет хеш для введенного пароля и сравнивает с эталонным хешем.
		"""
		return password_hash_hex == User.hash_password(password)


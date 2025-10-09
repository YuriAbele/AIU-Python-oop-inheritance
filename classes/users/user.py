# from __future__ import annotations - уже не надо, т.к. всё перенесено в UsersService
import hashlib
import uuid

class User:
	"""
	Базовый класс, представляющий пользователя.
	"""

	def __init__(self, username: str, email: str, password: str):

		# Нормализуем входные данные на случай, если кто-то будет создавать пользователя напрямую
		# (вместо использования метода UsersService.register)
		normalized_username = username.strip().lower() # Usernames не чувствительны к регистру
		normalized_email = email.strip() # Email может быть с заглавными буквами

		self.username = normalized_username
		self.email = normalized_email

		# необходимо хранить хеш пароля, а не сам пароль, для безопасности, без возможности восстановления
		# Вопрос - надо ли как-то нормализовать пароль, например, обрезать пробелы?
		self.password_hash_hex = User.hash_password(password)

	def __str__(self):
		return f"Пользователь: {self.username}, Email: {self.email}"

	# По хорошему он вообще не нужен, так как есть __str__
	def get_details(self) -> str:
		return self.__str__()

	# Корректно было бы вынесесть в UsersService, но тогда будет циклическая зависимость
	# из-за использования User в AuthenticationService и наоборот.
	@staticmethod
	def hash_password(password: str) -> str:
		"""
		Хеширование пароля с солью.
		Используется SHA-256 с уникальной солью на основе UUID4.
		Возвращается хеш в виде hex-строки.
		"""
		password_encoded = password.encode()
		password_salt = uuid.uuid4().bytes
		password_hash = hashlib.sha256(password_encoded + password_salt)
		password_hash_hex = password_hash.hexdigest()
		return password_hash_hex

	# Корректно было бы вынесесть в UsersService, но тогда будет циклическая зависимость
	# из-за использования User в AuthenticationService и наоборот.
	@staticmethod
	def check_password(password_hash_hex: str, password: str):
		"""
		Проверка пароля. Вычисляет хеш для введенного пароля и сравнивает с эталонным хешем.
		"""
		return password_hash_hex == User.hash_password(password)


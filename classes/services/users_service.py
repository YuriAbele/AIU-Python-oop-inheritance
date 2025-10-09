from classes.users import Admin, User
from classes.users.customer import Customer

# СЕРВИС УПРАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯМИ
#
# В реальности управление пользователями - сложная тема, требующая
# продуманной архитектуры, хранения пользователей в базе данных,
# использования безопасных протоколов и т.д.
# Здесь же для простоты примера реализован упрощенный вариант.
# В реальности для управления пользователями часто используют сторонние библиотеки и сервисы.
# Например, LDAP, OAuth, Keycloak и т.д.
#
# Важно:
# 	Управление сессиями пользователями (аутентификация, выход) реализовано в классе AuthenticationService.


class UsersService:
	"""
	Сервис управления пользователями (создание, удаление, изменение, просмотр).
	"""

	# Значения по умолчанию для новых пользователей - скрыты от внешнего мира
	__DEFAULT_ADMIN_LEVEL = 1 # Уровень администратора по умолчанию
	__DEFAULT_ADDRESS = "Не указан" # Адрес клиента по умолчанию

	def __init__(self):
		pass # ХЗ что тут инициализировать :-)

	# Список всех пользователей
	__list_users: list[User] = []

	def list_users(self, current_user: User):
		"""
		Выводит список всех пользователей.
		"""

		# Только администраторы могут просматривать список всех пользователей
		# В реальности могут быть и другие роли с такими правами
		# Cделано упрощенно для примера и здесь достаточно проверить тип класса
		if not isinstance(current_user, Admin):
			return "Доступ запрещен. Только администраторы могут просматривать список пользователей."

		return UsersService.__list_users


	def add_user(current_user: User, new_user: User) -> str:
		"""
		Добавляет объект пользователя в список пользователей.
		"""

		if not isinstance(current_user, Admin):
			return "Доступ запрещен. Только администраторы могут просматривать список пользователей."

		if not isinstance(new_user, User):
			return "Ошибка: можно добавить только объекты класса User или его подклассов."

		if any(user.username == new_user.username for user in UsersService.__list_users):
			return f"Пользователь \"{new_user.username}\" уже существует."

		UsersService.__list_users.append(new_user)
		return f"Пользователь \"{new_user.username}\" добавлен."

	# user_class - строка с именем класса пользователя, например "Admin" или "Customer"
	# Зачем еще "*args" - я не понял
	def register(self, current_user: User, user_class: str, username: str, email: str, password: str) -> str:
		"""
		Регистрация нового пользователя.
		Здесь:
		- для простоты примера реализована регистрация только администраторов и клиентов.
		- создаётся экземпляр класса пользователя (Admin или Customer), само добавление в список пользователей
		  происходит в методе add_user.
		Args:
			current_user (User): Текущий пользователь, выполняющий регистрацию - должен быть администратором.
			user_class (str): Класс пользователя для регистрации ("Admin" или "Customer").
			username (str): Имя пользователя.
			email (str): Электронная почта пользователя.
			password (str): Пароль пользователя - будет храниться хэш пароля без возможности восстановления.
		"""

		if not isinstance(current_user, Admin):
			return "Доступ запрещен. Только администраторы могут просматривать список пользователей."

		# Нормализуем входные данные
		normalized_user_class = user_class.strip().lower() # User class names не чувствительны к регистру
		normalized_username = username.strip().lower() # Usernames не чувствительны к регистру
		normalized_email = email.strip() # Email может быть с заглавными буквами

		# Проверяем, что пользователь с таким именем не существует
		if any(user.username == normalized_username for user in UsersService.__list_users):
			return f"Пользователь \"{normalized_username}\" уже существует."

		if normalized_user_class == "admin":
			new_user = Admin(normalized_username, normalized_email, password, admin_level=UsersService.__DEFAULT_ADMIN_LEVEL)
		elif normalized_user_class == "customer":
			new_user = Customer(normalized_username, normalized_email, password, address=UsersService.__DEFAULT_ADDRESS)
		else:
			return f"Ошибка: неизвестный класс пользователя \"{normalized_user_class}\"'."

		message = UsersService.add_user(current_user, new_user) # Вернувшееся сообщение сохраняем в переменную для облегчения отладки
		return message

	def delete_user(self, current_user: User, username_to_delete: str) -> str:
		"""
		Удаляет пользователя по имени-пользователя.
		Только администраторы могут удалять пользователей.
		Возвращает сообщение об успешном удалении или сообщение об ошибке.
		"""

		if not isinstance(current_user, Admin):
			return "Доступ запрещен. Только администраторы могут удалять пользователей."

		# Нормализуем входные данные
		normalized_username_to_delete = username_to_delete.strip().lower() # Usernames не чувствительны к регистру

		# Ищем пользователя по username
		user_to_delete = next((user for user in UsersService.__list_users if user.username == normalized_username_to_delete), None)

		if not user_to_delete:
			return f"Пользователь \"{normalized_username_to_delete}\" не найден."

		UsersService.__list_users.remove(user_to_delete)
		return f"Пользователь \"{normalized_username_to_delete}\" удален."

	def find_user(self, username_to_find: str) -> str | User:
		"""
		Ищет пользователя по имени-пользователя.
		Должна использоваться только для аутентификации.
		Возвращает объект пользователя или сообщение об ошибке.
		"""

		# Нормализуем входные данные
		normalized_username_to_find = username_to_find.strip().lower() # Usernames не чувствительны к регистру

		# Ищем пользователя по username
		user_to_find = next((user for user in UsersService.__list_users if user.username == normalized_username_to_find), None)

		if not user_to_find:
			return f"Пользователь \"{normalized_username_to_find}\" не найден."

		return user_to_find
from classes.users import Admin, User

class UsersService:
	"""
	Сервис управления пользователями.
	"""

	def __init__(self):
		pass

	# Список всех пользователей
	__list_users: list[User] = []

	@staticmethod
	def list_users(admin: User):
		"""
		Выводит список всех пользователей.
		"""

		if not isinstance(admin, Admin):
			return "Доступ запрещен. Только администраторы могут просматривать список пользователей."

		return User.__list_users


	@staticmethod
	def add_user(current_user: User, new_user: User) -> str:
		"""
		Добавляет пользователя в список пользователей.
		"""

		if not isinstance(current_user, Admin):
			return "Доступ запрещен. Только администраторы могут просматривать список пользователей."

		if not isinstance(new_user, User):
			return "Ошибка: можно добавить только объекты класса User или его подклассов."

		if any(user.username == new_user.username for user in User.__list_users):
			return f"Пользователь {new_user.username} уже существует."

		User.__list_users.append(new_user)
		return f"Пользователь {new_user.username} добавлен."

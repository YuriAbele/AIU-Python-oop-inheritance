import uuid
from classes.services.users_service import UsersService
from classes.users import Admin, User

# СЕРВИС АУТЕНТИФИКАЦИИ ПОЛЬЗОВАТЕЛЕЙ
#
# В реальности аутентификация и управление сессиями - сложные темы, требующие
# продуманной архитектуры, хранения сессий в базе данных или кэше,
# использования безопасных протоколов и т.д.
# Здесь же для простоты примера реализован упрощенный вариант.
# В реальности для аутентификации часто используют сторонние библиотеки и сервисы.
# Например, OAuth, JWT, LDAP и т.д.
#
# Важно:
# 	Управление самими пользователями (создание, удаление, изменение) реализовано в классе UsersService.
# 	Аутентификация же - в классе AuthenticationService.
# 	Это разделение ответственности - хороший архитектурный подход.


class AuthenticationService:
	"""
	Сервис аутентификации пользователей.
	"""

	_user_service: UsersService

	def __init__(self, user_service: UsersService):
		"""_summary_
		Инициализация сервиса аутентификации.
		Args:
			user_service (UsersService): должени быть передан экземпляр UsersService извне (для доступа к списку пользователей)
		"""
		self._user_service = user_service

	# Список сессий пользователей, содержащий кортежи (username, session_token)
	# Можно было бы организовать хранение сессий в виде словаря {username: session_token}, но тогда не смогли бы быть
	# одновременно активны несколько сессий одного пользователя (что в реальности возможно)
	# В реальности сессии хранятся в базе данных или в кэше, с датой начала сессии, но для простоты примера используем list[(username, session_token)] в памяти
	__active_sessions: list[(str, str)] = []

	def login(self, username: str, password: str) -> str:
		"""
		Аутентифицирует пользователя по имени-пользователя и паролю.
		Если аутентификация успешна, создает токен сессии и сохраняет его в списке активных сессий.
		Возвращает сообщение об успешной аутентификации с токеном сессии или сообщение об ошибке.
		"""

		# Нормализуем входные данные
		normalized_username = username.strip().lower() # Usernames не чувствительны к регистру

		# Ищем пользователя по username
		result = self._user_service.find_user(username_to_find=normalized_username)
		# проверка, что пользователь найден
		user = result if isinstance(result, User) else None

		# Если найден - проверяем пароль. Если верный, создаем токен сессии и сохраняем (username, session_token) в списке активных сессий
		if user and User.check_password(user.password_hash_hex, password):
			# В роли токена сессии используем UUID4 в виде hex-строки
			session_token = uuid.uuid4().hex
			AuthenticationService.__active_sessions.append((normalized_username, session_token))
			return f"Аутентификация успешна. Токен сессии: {session_token}"

		return "Ошибка аутентификации. Неверное имя-пользователя или пароль."


	# Такой метод без параметров не имеет смысла, так как не знает, какую сессию закрывать.
	# Перенос же его в класс не имеет смысла, так как класс User не хранит информацию о сессиях.
	# Или это потребует хранения сессий в самом классе User, что не очень правильно с точки зрения архитектуры.
	# Импортирование же класса AuthenticationService в класс User создаст циклическую зависимость.
	#
	# def logout(self):
	#	"""
	#	Выход пользователя из системы.
	#	"""

	def close_user_sessions(self, current_user: User, username_to_close_sessions: str) -> str:
		"""
		Закрывает все активные сессии пользователя по имени-пользователя.
		Только администраторы могут закрывать сессии других пользователей.
		Возвращает сообщение о количестве закрытых сессий или сообщение об ошибке.
		"""
		if not isinstance(current_user, Admin):
			return "Доступ запрещен. Только администраторы могут закрывать сессии пользователей."

		# Нормализуем входные данные
		normalized_username_to_close_sessions = username_to_close_sessions.strip().lower() # Usernames не чувствительны к регистру

		# Считаем количество активных сессий до удаления
		initial_count = len(AuthenticationService.__active_sessions)
		# Фильтруем список активных сессий, удаляя все сессии с указанным имени-пользователя
		AuthenticationService.__active_sessions = [
			# На интересуются только username, остальные данные сессии не важны
			(username, _) for (username, _) in AuthenticationService.__active_sessions if username != normalized_username_to_close_sessions
		]
		# Считаем, сколько сессий было закрыто
		closed_count = initial_count - len(AuthenticationService.__active_sessions)
		return f"Закрыто {closed_count} сессий для пользователя с именем: \"{username_to_close_sessions}\""

	def list_active_sessions(self, current_user: User) -> list[(str, str)] | str:
		"""
		Возвращает список всех активных сессий в виде кортежей (username, session_token).
		Только администраторы могут просматривать список всех активных сессий.
		"""

		if not isinstance(current_user, Admin):
			return "Доступ запрещен. Только администраторы могут просматривать список активных сессий."

		return AuthenticationService.__active_sessions

	# Такой метод без параметров не имеет смысла, так как не знает, какую сессию закрывать.
	# Перенос же его в класс не имеет смысла, так как класс User не хранит информацию о сессиях.
	# Или это потребует хранения сессий в самом классе User, что не очень правильно с точки зрения архитектуры.
	# Импортирование же класса AuthenticationService в класс User создаст циклическую зависимость.
	#
	# def logout(self):
	#	"""
	#	Выход пользователя из системы.
	#	"""

	# Такой метод без параметров не имеет смысла, так как не знает, какого пользователя возвращать.
	# Перенос же его в класс не имеет смысла, так как класс User не хранит информацию о сессиях.
	# Или это потребует хранения сессий в самом классе User, что не очень правильно с точки зрения архитектуры.
	# Импортирование же класса AuthenticationService в класс User создаст циклическую зависимость.
	#
	# def get_current_user(self):
	#	"""
	#	Возвращает текущего вошедшего пользователя.
	#	"""

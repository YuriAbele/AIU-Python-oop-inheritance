import uuid
from classes.users import Admin, User

class AuthenticationService:
	"""
	Сервис аутентификации пользователей.
	"""

	def __init__(self):
		pass

	# Список сессий пользователей, содержащий кортежи (user_email, session_token)
	# Можно было бы организовать хранение сессий в виде словаря {user_email: session_token}, но тогда не смогли бы быть
	# одновременно активны несколько сессий одного пользователя (что в реальности возможно)
	__active_sessions: list[(str, str)] = []

	@staticmethod
	def authenticate(email: str, password: str) -> str:
		"""
		Аутентифицирует пользователя по email и паролю.
		"""
		# Ищем пользователя по email
		user = next((user for user in User.__list_users if user.email == email), None)

		# Если найден - проверяем пароль. Если верный, создаем токен сессии и сохраняем (user_email, session_token) в списке активных сессий
		if user and User.check_password(user.password, password):
			session_token = uuid.uuid4().hex
			AuthenticationService.__active_sessions.append((email, session_token))
			return f"Аутентификация успешна. Токен сессии: {session_token}"

		return "Ошибка аутентификации. Неверный email или пароль."


	@staticmethod
	def close_user_sessions(current_user: User, sessions_email: str) -> str:
		"""
		Закрывает все активные сессии пользователя по email.
		"""
		if not isinstance(current_user, Admin):
			return "Доступ запрещен. Только администраторы могут закрывать сессии пользователей."

		# Считаем количество активных сессий до удаления
		initial_count = len(AuthenticationService.__active_sessions)
		# Фильтруем список активных сессий, удаляя все сессии с указанным email
		AuthenticationService.__active_sessions = [
			(session_email, token) for (session_email, token) in AuthenticationService.__active_sessions
			if session_email != sessions_email
		]
		# Считаем, сколько сессий было закрыто
		closed_count = initial_count - len(AuthenticationService.__active_sessions)
		return f"Закрыто {closed_count} сессий для пользователя с email: {sessions_email}"

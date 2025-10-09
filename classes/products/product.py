class Product:
	"""
	Базовый класс, представляющий продукт.
	"""
	def __init__(self, name, price):

		# Нормализуем входные данные
		normalized_name = name.strip()

		self.name = normalized_name
		self.price = price

	def get_details(self):
		return f"Продукт: {self.name}, Цера: {self.price} руб."

# 3. Класс для управления корзиной покупок

from classes.products import Product
from classes.users import Admin, Customer, User

class ShoppingCart:
	"""
	Класс, представляющий корзину покупок.
	"""
	def __init__(self, customer: Customer, user: User):
		self.customer = customer
		self.user = user
		self.items = []

	def add_item(self, product: Product, quantity: int):
		"""
		Добавляет продукт в корзину.
		"""
		self.items.append({"Продукт": product, "количество": quantity})

	def remove_item(self, product_name: str):
		"""
		Удаляет продукт из корзины по имени.
		"""

		# Нормализуем входные данные на случай, если кто-то будет создавать пользователя напрямую
		normalized_product_name = product_name.strip().lower()

		self.items = [item for item in self.items if item["Продукт"].name.lower() != normalized_product_name]

	def get_total(self):
		"""
		Возвращает общую стоимость продуктов в корзине.
		"""
		total = sum(item["Продукт"].price * item["количество"] for item in self.items)
		return total

	def get_details(self):
		"""
		Возвращает детализированную информацию о содержимом корзины и общей стоимости.
		"""
		details = f"Корзина покупок:\n\tПокупатель: {self.customer}\n\tПользователь: {self.user}\n\tКупленные товары:\n"

		for item in self.items:
			details += f"\t\t{item['Продукт'].get_details()}, Количество: {item['количество']}\n"
		details += f"\tОбщее: {self.get_total()} руб"
		return details

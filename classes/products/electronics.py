from .product import Product

class Electronics(Product):
	"""
	Класс, представляющий электронный продукт, наследующий класс Product.
	"""
	def __init__(self, name, price, brand, warranty_period):
		super().__init__(name, price)
		self.brand = brand
		self.warranty_period = warranty_period

	def get_details(self):
		return f"Электроника: {self.name}, Бренд: {self.brand}, Цена: {self.price} руб, Гарантия: {self.warranty_period} лет"

from .product import Product

class Clothing(Product):
	"""
	Класс, представляющий одежду, наследующий класс Product.
	"""
	def __init__(self, name, price, size, material):
		super().__init__(name, price)
		self.size = size
		self.material = material

	def get_details(self):
		return f"Одежда: {self.name}, Размер: {self.size}, Материал: {self.material}, Цена: {self.price} руб."

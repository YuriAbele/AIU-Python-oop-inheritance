from classes.products import Clothing
from classes.products import Electronics
from classes.shoping_cart import ShoppingCart
from classes.users import Admin
from classes.users import Customer

# Создаем продукты
laptop = Electronics(name="Ноутбук", price=120000, brand="Dell", warranty_period=2)
tshirt = Clothing(name="Футболка", price=200, size="M", material="Хлопок")

# Создаем пользователей
customer = Customer(username="Mikhail", email="python@derkunov.ru", address="033 Russ Bur")
admin = Admin(username="root", email="root@derkunov.ru", admin_level=5)

# Создаем корзину покупок и добавляем товары
cart = ShoppingCart()
cart.add_item(laptop, 1)
cart.add_item(tshirt, 3)

# Выводим детали корзины
print(cart.get_details())

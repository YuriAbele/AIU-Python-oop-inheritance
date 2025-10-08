from datetime import datetime
from classes.products import Clothing, Electronics, HouseholdChemicals
from classes.shoping_cart import ShoppingCart
from classes.users import Admin, Customer

# Создаем продукты
laptop = Electronics(name="Ноутбук", price=120000, brand="Dell", warranty_period=2)
tshirt = Clothing(name="Футболка", price=200, size="M", material="Хлопок")
fairy = HouseholdChemicals(name="Fairy", price=150)

# Создаем пользователей
customer = Customer(username="Mikhail", email="python@derkunov.ru", password="Qwertz123!", address="033 Russ Bur")
admin = Admin(username="root", email="root@derkunov.ru", password="Asdfgh456!", admin_level=5)

# Создаем корзину покупок и добавляем товары
cart = ShoppingCart(customer, admin)
cart.add_item(laptop, 1)
cart.add_item(tshirt, 3)
cart.add_item(fairy, 2)

# Выводим детали корзины
print(cart.get_details())

#####################################################################
print(f"\nFinished at: {datetime.now():%Y-%m-%d %H:%M:%S}\n\n")
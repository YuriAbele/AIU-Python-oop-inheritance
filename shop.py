from datetime import datetime
import uuid
from classes.products import Clothing, Electronics, HouseholdChemicals
from classes.shoping_cart import ShoppingCart
from classes.users import Admin, Customer
from classes.services import UsersService, AuthenticationService


print(f"\nStarted at: {datetime.now():%Y-%m-%d %H:%M:%S}\n")

#####################################################################
print(f"{"="*58}\n== ДЗ-Lite: Пример использования класса ShoppingCart =====\n")

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


#####################################################################
print(f"\n\n{"="*75}\n== ДЗ-Pro: Пример использования сервисов регистрации и аутентификации =====\n")

# Тестовые константы
USER_CLASS_ADMIN = "Admin"
USER_CLASS_CUSTOMER = "Customer"
#
SUPER_ADMIN_USERNAME = "yuriabele"
SUPER_ADMIN_EMAIL = "yuri.abele@mydomain.com"
SUPER_ADMIN_PASSWORD = uuid.uuid4().hex
SUPER_ADMIN_LEVEL = 1
#
OTHER_ADMIN_USERNAME = "OtherAdmin"
OTHER_ADMIN_EMAIL = "other.admin@otherdomain.com"
OTHER_ADMIN_PASSWORD = uuid.uuid4().hex
#
CUSTOMER_1_USERNAME = "Customer1"
CUSTOMER_1_EMAIL = "info@customer1.com"
CUSTOMER_1_PASSWORD = uuid.uuid4().hex
#
CUSTOMER_TO_DELETE_USERNAME = "customer-to-delete"
CUSTOMER_TO_DELETE_EMAIL = "info@customer1.com"
CUSTOMER_TO_DELETE_PASSWORD = uuid.uuid4().hex

# Создаем сервисы
users_service = UsersService()
auth_service = AuthenticationService(user_service=users_service)

# Создаем нового администратора в роли текущего пользователя-администратора напрямую, без регистрации через сервис UsersService
# Причина - извечная проблема "курицы и яйца" - чтобы создать первого администратора через сервис UsersService,
# нужен уже существующий администратор, который его создаст.
super_admin = Admin(username=SUPER_ADMIN_USERNAME, email=SUPER_ADMIN_EMAIL, password=SUPER_ADMIN_PASSWORD, admin_level=SUPER_ADMIN_LEVEL)

# Регистрируем администратора (текущий пользователь - другой администратор)
# Здесь для примера создаем другого администратора напрямую, но в реальности
# его тоже должен был бы создать другой администратор через сервис UsersService - получается замкнутый круг :-)
print("Регистрируем администратора:\n\t=>", users_service.register(super_admin, user_class=USER_CLASS_ADMIN, username=OTHER_ADMIN_USERNAME, email=OTHER_ADMIN_EMAIL, password=OTHER_ADMIN_PASSWORD))
# Регистрируем клиента (текущий пользователь - администратор)
print("Регистрируем клиента:\n\t=>", users_service.register(super_admin, user_class=USER_CLASS_CUSTOMER, username=CUSTOMER_1_USERNAME, email=CUSTOMER_1_EMAIL, password=CUSTOMER_1_PASSWORD))
# Выводим зарегистрированных пользователей (текущий пользователь - администратор)
print("Выводим зарегистрированных пользователей:\n[", *users_service.list_users(super_admin), sep="\n\t", end="\n]\n")

print(f"\n{"-"*50}\n")

# Регистрируем клиента "to-delete" (текущий пользователь - администратор)
print("Регистрируем клиента \"to-delete\":\n\t=>", users_service.register(super_admin, user_class=USER_CLASS_CUSTOMER, username=CUSTOMER_TO_DELETE_USERNAME, email=CUSTOMER_TO_DELETE_EMAIL, password=CUSTOMER_TO_DELETE_PASSWORD))
# Выводим зарегистрированных пользователей (текущий пользователь - администратор)
print("Выводим зарегистрированных пользователей:\n[", *users_service.list_users(super_admin), sep="\n\t", end="\n]\n")
# Удаляем пользователя "to-delete" (текущий пользователь - администратор)
print("Удаляем пользователя \"to-delete\":\n\t=>", users_service.delete_user(super_admin, CUSTOMER_TO_DELETE_USERNAME))
# Выводим зарегистрированных пользователей (текущий пользователь - администратор)
print("Выводим зарегистрированных пользователей:\n[", *users_service.list_users(super_admin), sep="\n\t", end="\n]\n")

print(f"\n{"-"*50}\n")

print("Аутентифицируем администратора с неправильным паролем:\n\t=>", auth_service.login(username=OTHER_ADMIN_USERNAME, password="WrongPassword!"))
print("Аутентифицируем несуществующего пользователя:\n\t=>", auth_service.login(username="NonExistentUser", password="SomePassword!"))
print("Аутентифицируем администратора с правильным паролем:\n\t=>", auth_service.login(username=OTHER_ADMIN_USERNAME, password=OTHER_ADMIN_PASSWORD))
print("Аутентифицируем клиента #1 с неправильным паролем:\n\t=>", auth_service.login(username=CUSTOMER_1_USERNAME, password="WrongPassword!"))
print("Аутентифицируем клиента #1 с правильным паролем:\n\t=>", auth_service.login(username=CUSTOMER_1_USERNAME, password=CUSTOMER_1_PASSWORD))
print("Повторная Аутентифицируем клиента #1 с правильным паролем:\n\t=>", auth_service.login(username=CUSTOMER_1_USERNAME, password=CUSTOMER_1_PASSWORD))
print("Просмотр активных сессий:\n[", *auth_service.list_active_sessions(super_admin), sep="\n\t", end="\n]\n")
print("Завершаем все сессии клиента #1:\n\t=>", auth_service.close_user_sessions(super_admin, CUSTOMER_1_USERNAME))
print("Просмотр активных сессий:\n[", *auth_service.list_active_sessions(super_admin), sep="\n\t", end="\n]\n")
#####################################################################

print(f"\n{"="*50}\nFinished at: {datetime.now():%Y-%m-%d %H:%M:%S}\n\n")
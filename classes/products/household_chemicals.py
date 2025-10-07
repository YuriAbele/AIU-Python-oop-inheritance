from .product import Product

class HouseholdChemicals(Product):
    """
    Класс, представляющий продукт бытовой химии, наследующий класс Product.
    """
    def __init__(self, name, price):
        super().__init__(name, price)

    def get_details(self):
        return f"Бытовая химия: {self.name}, Цена: {self.price} руб"

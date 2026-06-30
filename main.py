class Product:
    """Класс для представления продукта."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс для представления категории продуктов."""

    # Атрибуты класса
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product] = None):
        self.name = name
        self.description = description
        self.products = products if products is not None else []

        # Увеличиваем счетчики
        Category.category_count += 1
        Category.product_count += len(self.products)

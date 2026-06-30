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


def load_from_json(file_path: str) -> list[Category]:
    """Загружает данные из JSON-файла и создает объекты Category и Product."""
    import json
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    categories = []
    for cat_data in data.get('categories', []):
        products = []
        for prod_data in cat_data.get('products', []):
            product = Product(
                name=prod_data['name'],
                description=prod_data['description'],
                price=prod_data['price'],
                quantity=prod_data['quantity']
            )
            products.append(product)
        category = Category(
            name=cat_data['name'],
            description=cat_data['description'],
            products=products
        )
        categories.append(category)
    return categories

"""
Модуль с классами Product и Category, инкапсуляция, геттеры, сеттеры, класс-методы.
"""

import json
from typing import Any, Dict, List


class Product:
    """Товар с приватной ценой."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self._price = price  # приватный атрибут
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для цены."""
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой на положительность."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self._price = new_price

    @classmethod
    def new_product(cls, product_data: Dict[str, Any]) -> "Product":
        """
        Класс-метод для создания продукта из словаря.
        (Базовый вариант, без проверки дубликатов).
        """
        return cls(
            name=product_data.get("name", ""),
            description=product_data.get("description", ""),
            price=product_data.get("price", 0.0),
            quantity=product_data.get("quantity", 0),
        )


class Category:
    """Категория с приватным списком продуктов."""

    category_count: int = 0
    product_count: int = 0

    def __init__(
        self, name: str, description: str, products: List[Product] = None
    ) -> None:
        self.name = name
        self.description = description
        self._products = products if products is not None else []  # приватный список

        Category.category_count += 1
        Category.product_count += len(self._products)

    @property
    def products(self) -> str:
        """
        Геттер для списка продуктов, возвращает строку по шаблону:
        "Название продукта, X руб. Остаток: X шт.\n"
        """
        result = []
        for prod in self._products:
            result.append(
                f"{prod.name}, {prod.price} руб. Остаток: {prod.quantity} шт."
            )
        return "\n".join(result)

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в категорию и увеличивает счётчик продуктов."""
        self._products.append(product)
        Category.product_count += 1


# ---------- Дополнительная функция загрузки из JSON (не обязательна, но полезна) ----------
def load_categories_from_json(file_path: str) -> List[Category]:
    """
    Загружает категории и продукты из JSON-файла.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data: List[Dict[str, Any]] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    categories = []
    for cat_data in data:
        products = []
        for prod_data in cat_data.get("products", []):
            products.append(Product.new_product(prod_data))  # используем класс-метод
        categories.append(
            Category(
                name=cat_data.get("name", ""),
                description=cat_data.get("description", ""),
                products=products,
            )
        )
    return categories

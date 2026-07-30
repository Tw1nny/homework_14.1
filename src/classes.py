"""
Модуль с классами Product и Category, инкапсуляция, геттеры, сеттеры, класс-методы,
магические методы __str__ и __add__.
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
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data: Dict[str, Any]) -> "Product":
        return cls(
            name=product_data.get("name", ""),
            description=product_data.get("description", ""),
            price=product_data.get("price", 0.0),
            quantity=product_data.get("quantity", 0),
        )

    def __str__(self) -> str:
        """Строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """
        Сложение двух продуктов: сумма произведений цены на количество.
        Возвращает общую стоимость товаров на складе.
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты Product")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Category:
    """Категория с приватным списком продуктов."""

    category_count: int = 0
    product_count: int = 0

    def __init__(
        self, name: str, description: str, products: List[Product] = None
    ) -> None:
        self.name = name
        self.description = description
        self._products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self._products)

    @property
    def products(self) -> str:
        """
        Геттер для списка продуктов, возвращает строку по шаблону:
        "Название продукта, X руб. Остаток: X шт.\n"
        Использует __str__ каждого продукта.
        """
        return "".join(str(prod) + "\n" for prod in self._products)

    def add_product(self, product: Product) -> None:
        self._products.append(product)
        Category.product_count += 1

    def __str__(self) -> str:
        """Строковое представление категории с общим количеством товаров на складе."""
        total_quantity = sum(prod.quantity for prod in self._products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


def load_categories_from_json(file_path: str) -> List[Category]:
    """Загружает категории и продукты из JSON-файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data: List[Dict[str, Any]] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    categories = []
    for cat_data in data:
        products = []
        for prod_data in cat_data.get("products", []):
            products.append(Product.new_product(prod_data))
        categories.append(
            Category(
                name=cat_data.get("name", ""),
                description=cat_data.get("description", ""),
                products=products,
            )
        )
    return categories

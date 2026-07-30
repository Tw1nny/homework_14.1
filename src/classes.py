"""
Модуль с классами Product, Category, Smartphone, LawnGrass,
абстрактным базовым классом BaseProduct и миксином LogMixin.
"""

import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class LogMixin:
    """Миксин для логирования создания объектов."""

    def __init__(self, *args, **kwargs) -> None:
        print(
            f"Создан объект {self.__class__.__name__} с параметрами: {args}, {kwargs}"
        )
        super().__init__()


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @property
    @abstractmethod
    def price(self) -> float:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Product(LogMixin, BaseProduct):
    """Базовый класс для всех товаров."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        # Проверка на нулевое количество
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        super().__init__(name, description, price, quantity)
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
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: str,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


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
        return "".join(str(prod) + "\n" for prod in self._products)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только объекты Product или его наследников"
            )
        self._products.append(product)
        Category.product_count += 1

    def average_price(self) -> float:
        """
        Возвращает среднюю цену всех товаров в категории.
        Если товаров нет, возвращает 0.
        """
        if not self._products:
            return 0.0
        total_price = sum(prod.price for prod in self._products)
        return total_price / len(self._products)

    def __str__(self) -> str:
        total_quantity = sum(prod.quantity for prod in self._products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


def load_categories_from_json(file_path: str) -> List[Category]:
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

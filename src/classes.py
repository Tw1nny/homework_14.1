"""
Модуль с классами Category и Product, а также функцией загрузки из JSON.
"""

import json
from typing import List, Dict, Any


class Product:
    """Товар с названием, описанием, ценой и количеством."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """
        Инициализация продукта.

        Параметры:
            name: название товара
            description: описание
            price: цена (может быть с копейками)
            quantity: количество в наличии (целое)
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """
    Категория товаров с названием, описанием и списком продуктов.
    Автоматически ведёт подсчёт общего количества категорий и товаров.
    """

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        """
        Инициализация категории.

        Параметры:
            name: название категории
            description: описание
            products: список объектов Product
        """
        self.name = name
        self.description = description
        self.products = products

        # Автоматическое обновление счётчиков при создании объекта
        Category.category_count += 1
        Category.product_count += len(products)


def load_categories_from_json(file_path: str) -> List[Category]:
    """
    Загружает данные из JSON-файла и создаёт список объектов Category.

    Ожидаемая структура JSON:
    [
        {
            "name": "Категория 1",
            "description": "Описание",
            "products": [
                {"name": "Товар", "description": "...", "price": 100.5, "quantity": 10},
                ...
            ]
        },
        ...
    ]

    Параметры:
        file_path: путь к JSON-файлу.

    Возвращает:
        список объектов Category.
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
            products.append(
                Product(
                    name=prod_data.get("name", ""),
                    description=prod_data.get("description", ""),
                    price=prod_data.get("price", 0.0),
                    quantity=prod_data.get("quantity", 0),
                )
            )
        categories.append(
            Category(
                name=cat_data.get("name", ""),
                description=cat_data.get("description", ""),
                products=products,
            )
        )
    return categories
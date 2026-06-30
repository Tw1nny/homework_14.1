import pytest
from src.classes import Product, Category, load_categories_from_json


# Фикстуры для тестов
@pytest.fixture
def sample_product():
    return Product("Ноутбук", "Игровой ноутбук", 150000.50, 5)


@pytest.fixture
def sample_category(sample_product):
    return Category("Электроника", "Разная техника", [sample_product])


def test_product_init(sample_product):
    """Проверка инициализации Product."""
    assert sample_product.name == "Ноутбук"
    assert sample_product.description == "Игровой ноутбук"
    assert sample_product.price == 150000.50
    assert sample_product.quantity == 5


def test_category_init(sample_category):
    """Проверка инициализации Category."""
    assert sample_category.name == "Электроника"
    assert sample_category.description == "Разная техника"
    assert len(sample_category.products) == 1
    assert sample_category.products[0].name == "Ноутбук"


def test_category_count():
    """Проверка автоматического подсчёта категорий."""
    Category.category_count = 0  # сброс для теста
    Category.product_count = 0

    cat1 = Category("A", "Описание A", [Product("P1", "desc", 10, 2)])
    cat2 = Category("B", "Описание B", [Product("P2", "desc", 20, 3)])

    assert Category.category_count == 2
    assert cat1.category_count == 2  # доступ через объект тоже работает


def test_product_count():
    """Проверка автоматического подсчёта общего количества продуктов."""
    Category.category_count = 0
    Category.product_count = 0

    cat1 = Category("A", "desc", [Product("P1", "d", 1, 2), Product("P2", "d", 2, 3)])
    cat2 = Category("B", "desc", [Product("P3", "d", 3, 4)])

    assert Category.product_count == 3  # 2 + 1


def test_load_categories_from_json(tmp_path):
    """Тест загрузки из JSON (доп. задание)."""
    import json

    data = [
        {
            "name": "Категория 1",
            "description": "Описание 1",
            "products": [
                {"name": "Товар 1", "description": "desc1", "price": 100.0, "quantity": 10},
                {"name": "Товар 2", "description": "desc2", "price": 200.5, "quantity": 20},
            ]
        },
        {
            "name": "Категория 2",
            "description": "Описание 2",
            "products": [
                {"name": "Товар 3", "description": "desc3", "price": 300.0, "quantity": 30},
            ]
        }
    ]

    file_path = tmp_path / "test_products.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    categories = load_categories_from_json(str(file_path))
    assert len(categories) == 2
    assert categories[0].name == "Категория 1"
    assert len(categories[0].products) == 2
    assert categories[0].products[0].price == 100.0


def test_load_categories_from_json_file_not_found():
    """Ошибка при отсутствии файла -> пустой список."""
    categories = load_categories_from_json("nonexistent.json")
    assert categories == []
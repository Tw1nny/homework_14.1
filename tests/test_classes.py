import pytest

from src.classes import Category, Product, load_categories_from_json


@pytest.fixture(autouse=True)
def reset_category_counts():
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_product():
    return Product("Ноутбук", "Игровой", 150000.50, 5)


@pytest.fixture
def sample_category(sample_product):
    return Category("Электроника", "Техника", [sample_product])


def test_product_init(sample_product):
    assert sample_product.name == "Ноутбук"
    assert sample_product.description == "Игровой"
    assert sample_product.price == 150000.50
    assert sample_product.quantity == 5


def test_product_price_setter_positive(sample_product):
    sample_product.price = 200000.00
    assert sample_product.price == 200000.00


def test_product_price_setter_non_positive(capsys, sample_product):
    sample_product.price = -100
    captured = capsys.readouterr()
    assert captured.out == "Цена не должна быть нулевая или отрицательная\n"
    assert sample_product.price == 150000.50

    sample_product.price = 0
    captured = capsys.readouterr()
    assert captured.out == "Цена не должна быть нулевая или отрицательная\n"
    assert sample_product.price == 150000.50


def test_product_new_classmethod():
    data = {
        "name": "Телефон",
        "description": "Смартфон",
        "price": 50000.0,
        "quantity": 10,
    }
    product = Product.new_product(data)
    assert product.name == "Телефон"
    assert product.price == 50000.0
    assert product.quantity == 10


def test_category_init(sample_category):
    assert sample_category.name == "Электроника"
    assert sample_category.description == "Техника"
    products_str = sample_category.products
    assert "Ноутбук" in products_str
    assert "150000.5" in products_str
    assert "Остаток: 5" in products_str


def test_category_add_product(sample_category, sample_product):
    new_prod = Product("Планшет", "Планшет", 30000, 3)
    sample_category.add_product(new_prod)

    products_str = sample_category.products
    assert "Планшет" in products_str
    assert "30000" in products_str
    assert Category.product_count == 2


def test_category_count():
    cat1 = Category("A", "desc", [Product("P1", "d", 10, 2)])
    cat2 = Category("B", "desc", [Product("P2", "d", 20, 3)])

    assert Category.category_count == 2
    assert Category.product_count == 2
    assert cat1.name == "A"
    assert cat2.name == "B"


def test_load_categories_from_json(tmp_path):
    import json

    data = [
        {
            "name": "Кат1",
            "description": "Описание1",
            "products": [
                {
                    "name": "Товар1",
                    "description": "desc1",
                    "price": 100.0,
                    "quantity": 10,
                }
            ],
        }
    ]
    file_path = tmp_path / "test.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    categories = load_categories_from_json(str(file_path))
    assert len(categories) == 1
    assert categories[0].name == "Кат1"
    assert len(categories[0]._products) == 1
    assert categories[0]._products[0].name == "Товар1"


# ---------- Новые тесты для магических методов ----------
def test_product_str(sample_product):
    expected = "Ноутбук, 150000.5 руб. Остаток: 5 шт."
    assert str(sample_product) == expected


def test_category_str(sample_category):
    # В категории один продукт с quantity=5
    expected = "Электроника, количество продуктов: 5 шт."
    assert str(sample_category) == expected

    # Добавим ещё продукт и проверим сумму quantity
    new_prod = Product("Планшет", "Планшет", 30000, 3)
    sample_category.add_product(new_prod)
    expected2 = "Электроника, количество продуктов: 8 шт."
    assert str(sample_category) == expected2


def test_product_add(sample_product):
    other = Product("Телефон", "desc", 200, 10)
    total = sample_product + other
    # 150000.5 * 5 + 200 * 10 = 750002.5 + 2000 = 752002.5
    assert total == 150000.5 * 5 + 200 * 10

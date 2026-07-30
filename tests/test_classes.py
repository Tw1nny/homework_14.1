import pytest

from src.classes import (
    Category,
    LawnGrass,
    Product,
    Smartphone,
    load_categories_from_json,
)


@pytest.fixture(autouse=True)
def reset_counts():
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_product():
    return Product("Ноутбук", "Игровой", 150000.50, 5)


@pytest.fixture
def sample_category(sample_product):
    return Category("Электроника", "Техника", [sample_product])


@pytest.fixture
def smartphone():
    return Smartphone(
        "iPhone 15",
        "Смартфон Apple",
        120000,
        10,
        "A16 Bionic",
        "iPhone 15",
        256,
        "черный",
    )


@pytest.fixture
def lawn_grass():
    return LawnGrass(
        "Газонная трава",
        "Спортсмен",
        1500,
        50,
        "Россия",
        "7-14 дней",
        "зеленый",
    )


# ---------- Старые тесты (должны проходить) ----------
def test_product_init(sample_product):
    assert sample_product.name == "Ноутбук"
    assert sample_product.price == 150000.50


def test_product_price_setter_positive(sample_product):
    sample_product.price = 200000
    assert sample_product.price == 200000


def test_product_price_setter_non_positive(capsys, sample_product):
    sample_product.price = -10
    captured = capsys.readouterr()
    assert captured.out == "Цена не должна быть нулевая или отрицательная\n"
    assert sample_product.price == 150000.50


def test_product_new_classmethod():
    data = {"name": "Телефон", "description": "desc", "price": 50000, "quantity": 10}
    product = Product.new_product(data)
    assert product.name == "Телефон"


def test_category_init(sample_category):
    assert sample_category.name == "Электроника"


def test_category_add_product(sample_category):
    new_prod = Product("Планшет", "Планшет", 30000, 3)
    sample_category.add_product(new_prod)
    assert Category.product_count == 2


def test_category_count():
    cat1 = Category("A", "desc", [Product("P1", "d", 10, 2)])
    cat2 = Category("B", "desc", [Product("P2", "d", 20, 3)])
    assert Category.category_count == 2
    assert Category.product_count == 2


def test_load_categories_from_json(tmp_path):
    import json

    data = [{"name": "Кат1", "description": "Описание1", "products": []}]
    file_path = tmp_path / "test.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    categories = load_categories_from_json(str(file_path))
    assert len(categories) == 1


def test_product_str(sample_product):
    assert str(sample_product) == "Ноутбук, 150000.5 руб. Остаток: 5 шт."


def test_category_str(sample_category):
    assert str(sample_category) == "Электроника, количество продуктов: 5 шт."


def test_product_add(sample_product):
    other = Product("Телефон", "desc", 200, 10)
    total = sample_product + other
    assert total == 150000.5 * 5 + 200 * 10


# ---------- Новые тесты для наследников ----------
def test_smartphone_init(smartphone):
    assert smartphone.name == "iPhone 15"
    assert smartphone.efficiency == "A16 Bionic"
    assert smartphone.model == "iPhone 15"
    assert smartphone.memory == 256
    assert smartphone.color == "черный"


def test_lawn_grass_init(lawn_grass):
    assert lawn_grass.name == "Газонная трава"
    assert lawn_grass.country == "Россия"
    assert lawn_grass.germination_period == "7-14 дней"
    assert lawn_grass.color == "зеленый"


def test_add_same_class(smartphone):
    other_smartphone = Smartphone(
        "Samsung", "desc", 100000, 5, "Exynos", "S23", 128, "белый"
    )
    total = smartphone + other_smartphone
    expected = 120000 * 10 + 100000 * 5
    assert total == expected


def test_add_different_classes(smartphone, lawn_grass):
    with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
        _ = smartphone + lawn_grass


def test_category_add_product_invalid_type(sample_category):
    with pytest.raises(TypeError, match="Можно добавлять только объекты Product"):
        sample_category.add_product("not a product")

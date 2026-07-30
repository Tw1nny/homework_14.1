import pytest

from src.classes import (
    BaseProduct,
    Category,
    LawnGrass,
    Product,
    Smartphone,
    load_categories_from_json,
)

# ====================== ФИКСТУРЫ ======================


@pytest.fixture(autouse=True)
def reset_category_counts():
    """Сбрасываем счётчики категорий перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def product():
    return Product("Ноутбук", "Игровой ноутбук", 150000.50, 5)


@pytest.fixture
def category_with_product(product):
    return Category("Электроника", "Разная техника", [product])


@pytest.fixture
def smartphone():
    return Smartphone(
        "iPhone 15",
        "Флагманский смартфон",
        120000.0,
        10,
        "A16 Bionic",
        "iPhone 15 Pro",
        256,
        "черный",
    )


@pytest.fixture
def lawn_grass():
    return LawnGrass(
        "Газонная трава",
        "Для спортивных полей",
        1500.0,
        50,
        "Россия",
        "7-14 дней",
        "зеленый",
    )


# ====================== ТЕСТЫ ДЛЯ PRODUCT ======================


def test_product_init(product):
    assert product.name == "Ноутбук"
    assert product.description == "Игровой ноутбук"
    assert product.price == 150000.50
    assert product.quantity == 5


def test_product_price_setter_positive(product):
    product.price = 200000.0
    assert product.price == 200000.0


def test_product_price_setter_zero(capsys, product):
    # Сбрасываем вывод, чтобы убрать сообщение от миксина
    capsys.readouterr()
    product.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 150000.50  # цена не изменилась


def test_product_price_setter_negative(capsys, product):
    capsys.readouterr()
    product.price = -100
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 150000.50


def test_product_new_classmethod():
    data = {
        "name": "Телефон",
        "description": "Смартфон",
        "price": 50000.0,
        "quantity": 10,
    }
    p = Product.new_product(data)
    assert p.name == "Телефон"
    assert p.price == 50000.0
    assert p.quantity == 10


def test_product_str(product):
    assert str(product) == "Ноутбук, 150000.5 руб. Остаток: 5 шт."


def test_product_add_same_class(product):
    other = Product("Телефон", "desc", 200.0, 10)
    total = product + other
    expected = 150000.5 * 5 + 200 * 10
    assert total == expected


def test_product_add_different_class_raises(product, smartphone):
    with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
        _ = product + smartphone


def test_product_add_invalid_type_raises(product):
    with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
        _ = product + "not a product"


# ====================== ТЕСТЫ ДЛЯ CATEGORY ======================


def test_category_init(category_with_product, product):
    assert category_with_product.name == "Электроника"
    assert category_with_product.description == "Разная техника"
    assert category_with_product.products == "Ноутбук, 150000.5 руб. Остаток: 5 шт.\n"


def test_category_add_product(category_with_product):
    new_prod = Product("Планшет", "Планшет", 30000, 3)
    category_with_product.add_product(new_prod)
    assert "Планшет" in category_with_product.products
    assert Category.product_count == 2  # был 1, добавили 1


def test_category_add_product_invalid_type_raises(category_with_product):
    with pytest.raises(TypeError, match="Можно добавлять только объекты Product"):
        category_with_product.add_product("not a product")


def test_category_product_count(category_with_product):
    # Изначально 1 продукт в категории
    assert Category.product_count == 1
    # Добавляем ещё
    category_with_product.add_product(Product("A", "desc", 10, 2))
    assert Category.product_count == 2


def test_category_str(category_with_product):
    assert str(category_with_product) == "Электроника, количество продуктов: 5 шт."
    # Добавим ещё продукт и проверим сумму quantity
    category_with_product.add_product(Product("Планшет", "desc", 30000, 3))
    assert str(category_with_product) == "Электроника, количество продуктов: 8 шт."


def test_category_count():
    Category.category_count = 0
    Category.product_count = 0
    cat1 = Category("A", "desc", [Product("P1", "d", 10, 2)])
    cat2 = Category("B", "desc", [Product("P2", "d", 20, 3)])
    assert Category.category_count == 2
    assert Category.product_count == 2  # два продукта (P1 и P2)


# ====================== ТЕСТЫ ДЛЯ SMARTFON ======================


def test_smartphone_init(smartphone):
    assert smartphone.name == "iPhone 15"
    assert smartphone.description == "Флагманский смартфон"
    assert smartphone.price == 120000.0
    assert smartphone.quantity == 10
    assert smartphone.efficiency == "A16 Bionic"
    assert smartphone.model == "iPhone 15 Pro"
    assert smartphone.memory == 256
    assert smartphone.color == "черный"


def test_smartphone_str(smartphone):
    expected = "iPhone 15, 120000.0 руб. Остаток: 10 шт."
    assert str(smartphone) == expected


def test_smartphone_add_same_class(smartphone):
    other = Smartphone(
        "Samsung Galaxy",
        "desc",
        100000.0,
        5,
        "Exynos",
        "S23",
        128,
        "белый",
    )
    total = smartphone + other
    expected = 120000 * 10 + 100000 * 5
    assert total == expected


def test_smartphone_add_different_class_raises(smartphone, lawn_grass):
    with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
        _ = smartphone + lawn_grass


# ====================== ТЕСТЫ ДЛЯ LAWNGRASS ======================


def test_lawn_grass_init(lawn_grass):
    assert lawn_grass.name == "Газонная трава"
    assert lawn_grass.description == "Для спортивных полей"
    assert lawn_grass.price == 1500.0
    assert lawn_grass.quantity == 50
    assert lawn_grass.country == "Россия"
    assert lawn_grass.germination_period == "7-14 дней"
    assert lawn_grass.color == "зеленый"


def test_lawn_grass_str(lawn_grass):
    expected = "Газонная трава, 1500.0 руб. Остаток: 50 шт."
    assert str(lawn_grass) == expected


def test_lawn_grass_add_same_class(lawn_grass):
    other = LawnGrass(
        "Трава другая",
        "desc",
        2000.0,
        20,
        "США",
        "10 дней",
        "темно-зеленый",
    )
    total = lawn_grass + other
    expected = 1500 * 50 + 2000 * 20
    assert total == expected


def test_lawn_grass_add_different_class_raises(lawn_grass, smartphone):
    with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
        _ = lawn_grass + smartphone


# ====================== ТЕСТЫ ДЛЯ АБСТРАКТНОГО КЛАССА ======================


def test_base_product_abstract():
    with pytest.raises(TypeError):
        BaseProduct()


def test_product_is_subclass_of_base():
    assert issubclass(Product, BaseProduct)


def test_smartphone_is_subclass_of_base():
    assert issubclass(Smartphone, BaseProduct)


def test_lawn_grass_is_subclass_of_base():
    assert issubclass(LawnGrass, BaseProduct)


# ====================== ТЕСТЫ ДЛЯ ЗАГРУЗКИ ИЗ JSON ======================


def test_load_categories_from_json_success(tmp_path):
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
                },
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
    assert categories[0]._products[0].price == 100.0


def test_load_categories_from_json_file_not_found():
    categories = load_categories_from_json("nonexistent.json")
    assert categories == []


def test_load_categories_from_json_invalid_json(tmp_path):
    file_path = tmp_path / "invalid.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("not a json")
    categories = load_categories_from_json(str(file_path))
    assert categories == []


# ====================== ТЕСТЫ ДЛЯ ЛОГИРОВАНИЯ (MIXIN) ======================


def test_log_mixin_output(capsys):
    p = Product("Тест", "Описание", 100, 5)
    captured = capsys.readouterr()
    # Проверяем, что сообщение содержит имя класса и аргументы
    assert (
        "Создан объект Product с параметрами: ('Тест', 'Описание', 100, 5), {}"
        in captured.out
    )
    # Или хотя бы содержит "Тест"
    assert "Тест" in captured.out


def test_log_mixin_for_smartphone(capsys):
    s = Smartphone("A", "B", 100, 2, "C", "D", 128, "red")
    captured = capsys.readouterr()
    # В миксин попадают только базовые аргументы (name, description, price, quantity)
    assert (
        "Создан объект Smartphone с параметрами: ('A', 'B', 100, 2), {}" in captured.out
    )


def test_log_mixin_for_lawn_grass(capsys):
    lg = LawnGrass("A", "B", 100, 2, "RU", "7d", "green")
    captured = capsys.readouterr()
    assert (
        "Создан объект LawnGrass с параметрами: ('A', 'B', 100, 2), {}" in captured.out
    )


def test_product_init_zero_quantity_raises():
    with pytest.raises(
        ValueError, match="Товар с нулевым количеством не может быть добавлен"
    ):
        Product("Товар", "Описание", 100, 0)


def test_category_average_price_with_products(category_with_product):
    # category_with_product уже содержит один продукт с ценой 150000.5
    assert category_with_product.average_price() == 150000.5


def test_category_average_price_empty_category():
    empty_cat = Category("Пустая", "desc", [])
    assert empty_cat.average_price() == 0.0


def test_category_average_price_multiple_products():
    p1 = Product("P1", "d", 100, 10)
    p2 = Product("P2", "d", 200, 20)
    cat = Category("Cat", "desc", [p1, p2])
    assert cat.average_price() == (100 + 200) / 2


def test_smartphone_init_zero_quantity_raises():
    with pytest.raises(
        ValueError, match="Товар с нулевым количеством не может быть добавлен"
    ):
        Smartphone("A", "B", 100, 0, "C", "D", 128, "red")


def test_lawn_grass_init_zero_quantity_raises():
    with pytest.raises(
        ValueError, match="Товар с нулевым количеством не может быть добавлен"
    ):
        LawnGrass("A", "B", 100, 0, "RU", "7d", "green")

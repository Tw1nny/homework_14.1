import pytest
from src.category_product.main import Product, Category


@pytest.fixture
def sample_product():
    return Product("Test Product", "Test Description", 100.0, 10)


@pytest.fixture
def sample_category(sample_product):
    return Category("Test Category", "Test Category Description", [sample_product])


def test_product_init(sample_product):
    assert sample_product.name == "Test Product"
    assert sample_product.description == "Test Description"
    assert sample_product.price == 100.0
    assert sample_product.quantity == 10


def test_category_init(sample_category):
    assert sample_category.name == "Test Category"
    assert sample_category.description == "Test Category Description"
    assert len(sample_category.products) == 1
    assert isinstance(sample_category.products[0], Product)


def test_category_counts():
    # Сбрасываем счетчики для теста
    Category.category_count = 0
    Category.product_count = 0

    _ = Category("Cat1", "Desc1")
    _ = Category("Cat2", "Desc2", [Product("P1", "D1", 50.0, 5)])

    assert Category.category_count == 2
    assert Category.product_count == 1  # Только один продукт во второй категории


def test_product_count_in_category(sample_category):
    assert len(sample_category.products) == 1

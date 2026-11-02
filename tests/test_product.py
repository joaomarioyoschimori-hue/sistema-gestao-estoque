import pytest

from app.models.product import Product


def test_create_product():
    product = Product(
        name="Mouse Gamer",
        code="M2001",
        description="Mouse RGB",
        purchase_price=100,
        sale_price=150,
        quantity=10
    )

    assert product.name == "Mouse Gamer"
    assert product.code == "M2001"
    assert product.quantity == 10


def test_product_name_cannot_be_empty():
    with pytest.raises(ValueError):
        Product(
            name="",
            code="M2002",
            description="Mouse",
            purchase_price=100,
            sale_price=150,
            quantity=10
        )


def test_product_quantity_cannot_be_negative():
    with pytest.raises(ValueError):
        Product(
            name="Teclado",
            code="T1001",
            description="Teclado mecânico",
            purchase_price=100,
            sale_price=200,
            quantity=-5
        )

def test_add_stock():
    product = Product(
        name="Mouse",
        code="M100",
        description="Mouse gamer",
        purchase_price=100,
        sale_price=150,
        quantity=10
    )

    product.add_stock(5)

    assert product.quantity == 15


def test_remove_stock():
    product = Product(
        name="Mouse",
        code="M100",
        description="Mouse gamer",
        purchase_price=100,
        sale_price=150,
        quantity=10
    )

    product.remove_stock(3)

    assert product.quantity == 7


def test_cannot_remove_more_stock_than_available():
    product = Product(
        name="Mouse",
        code="M100",
        description="Mouse gamer",
        purchase_price=100,
        sale_price=150,
        quantity=10
    )

    with pytest.raises(ValueError):
        product.remove_stock(15)
import pytest
import sqlite3
from app.models.product import Product
from app.database import product_repository

@pytest.fixture
def test_database(tmp_path, monkeypatch):
    database_path = tmp_path / "test_estoque.db"

    def get_test_connection():
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        return connection

    monkeypatch.setattr(
        product_repository,
        "get_connection",
        get_test_connection
    )

    connection = get_test_connection()

    connection.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL UNIQUE,
            description TEXT,
            purchase_price REAL NOT NULL,
            sale_price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE stock_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_code TEXT NOT NULL,
            movement_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_code) REFERENCES products(code)
        )
    """)

    connection.commit()
    connection.close()

    return database_path

def test_insert_and_get_product(test_database):
    product = Product(
        name="Teclado Mecânico",
        code="T1001",
        description="Teclado RGB",
        purchase_price=150,
        sale_price=250,
        quantity=10
    )

    product_repository.insert_product(product)

    saved_product = product_repository.get_product_by_code("T1001")

    assert saved_product is not None
    assert saved_product["name"] == "Teclado Mecânico"
    assert saved_product["code"] == "T1001"
    assert saved_product["quantity"] == 10

def test_register_stock_movement(test_database):
    product = Product(
        name="Mouse Gamer",
        code="M2001",
        description="Mouse RGB",
        purchase_price=100,
        sale_price=150,
        quantity=10
    )

    product_repository.insert_product(product)

    product_repository.register_stock_movement(
        code="M2001",
        new_quantity=15,
        movement_type="ENTRADA",
        amount=5
    )

    saved_product = product_repository.get_product_by_code("M2001")
    movements = product_repository.get_stock_movements("M2001")

    assert saved_product["quantity"] == 15
    assert len(movements) == 1
    assert movements[0]["movement_type"] == "ENTRADA"
    assert movements[0]["quantity"] == 5


def test_stock_movement_rollback(test_database, monkeypatch):
    product = Product(
        name="Mouse Gamer",
        code="M3001",
        description="Mouse RGB",
        purchase_price=100,
        sale_price=150,
        quantity=10
    )

    product_repository.insert_product(product)

    original_connection = product_repository.get_connection

    class FailingConnection:
        def __init__(self):
            self.connection = original_connection()

        def execute(self, sql, parameters=()):
            if "INSERT INTO stock_movements" in sql:
                raise sqlite3.IntegrityError("Erro simulado")

            return self.connection.execute(sql, parameters)

        def commit(self):
            self.connection.commit()

        def rollback(self):
            self.connection.rollback()

        def close(self):
            self.connection.close()

    monkeypatch.setattr(
        product_repository,
        "get_connection",
        FailingConnection
    )

    with pytest.raises(sqlite3.IntegrityError):
        product_repository.register_stock_movement(
            "M3001", 15, "ENTRADA", 5
        )

    monkeypatch.setattr(
        product_repository,
        "get_connection",
        original_connection
    )

    saved_product = product_repository.get_product_by_code("M3001")

    assert saved_product["quantity"] == 10
    
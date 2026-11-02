from app.database.connection import get_connection


def insert_product(product):
    connection = get_connection()

    connection.execute("""
        INSERT INTO products (
            name,
            code,
            description,
            purchase_price,
            sale_price,
            quantity
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        product.name,
        product.code,
        product.description,
        product.purchase_price,
        product.sale_price,
        product.quantity
    ))

    connection.commit()
    connection.close()


def get_all_products():
    connection = get_connection()

    products = connection.execute(
        "SELECT * FROM products"
    ).fetchall()

    connection.close()

    return products


def get_product_by_code(code):
    connection = get_connection()

    product = connection.execute(
        "SELECT * FROM products WHERE code = ?",
        (code,)
    ).fetchone()

    connection.close()

    return product


def update_product_stock(code, new_quantity):
    connection = get_connection()

    connection.execute(
        "UPDATE products SET quantity = ? WHERE code = ?",
        (new_quantity, code)
    )

    connection.commit()
    connection.close()

def insert_stock_movement(code, movement_type, quantity):
    connection = get_connection()

    connection.execute("""
        INSERT INTO stock_movements (
            product_code,
            movement_type,
            quantity
        )
        VALUES (?, ?, ?)
    """, (code, movement_type, quantity))

    connection.commit()
    connection.close()

def get_stock_movements(code):
    connection = get_connection()

    movements = connection.execute("""
        SELECT *
        FROM stock_movements
        WHERE product_code = ?
        ORDER BY created_at DESC, id DESC
    """, (code,)).fetchall()

    connection.close()

    return movements

def get_stock_report():
    connection = get_connection()

    report = connection.execute("""
        SELECT
            COUNT(*) AS total_products,
            COALESCE(SUM(quantity), 0) AS total_units,
            COALESCE(SUM(purchase_price * quantity), 0) AS total_invested,
            COALESCE(SUM(sale_price * quantity), 0) AS potential_revenue
        FROM products
    """).fetchone()

    connection.close()

    return report

def get_low_stock_products(limit=5):
    connection = get_connection()

    products = connection.execute("""
        SELECT *
        FROM products
        WHERE quantity <= ?
        ORDER BY quantity ASC
    """, (limit,)).fetchall()

    connection.close()

    return products

def register_stock_movement(code, new_quantity, movement_type, amount):
    connection = get_connection()

    try:
        connection.execute(
            "UPDATE products SET quantity = ? WHERE code = ?",
            (new_quantity, code)
        )

        connection.execute("""
            INSERT INTO stock_movements (
                product_code,
                movement_type,
                quantity
            )
            VALUES (?, ?, ?)
        """, (code, movement_type, amount))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
    
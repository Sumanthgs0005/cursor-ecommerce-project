import csv
import sqlite3
from pathlib import Path
from typing import Iterable, List, Dict

DB_NAME = "ecommerce.db"


def read_csv(path: Path, fieldnames: Iterable[str]) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        missing = set(fieldnames) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path} is missing fields: {', '.join(sorted(missing))}")
        return list(reader)


def read_categories(path: Path = Path("categories.csv")) -> List[Dict[str, str]]:
    return read_csv(path, ["category_id", "category_name"])


def read_users(path: Path = Path("users.csv")) -> List[Dict[str, str]]:
    return read_csv(path, ["user_id", "username", "email", "created_at"])


def read_products(path: Path = Path("products.csv")) -> List[Dict[str, str]]:
    return read_csv(path, ["product_id", "name", "price", "category_id"])


def read_orders(path: Path = Path("orders.csv")) -> List[Dict[str, str]]:
    return read_csv(path, ["order_id", "user_id", "order_date", "status"])


def read_order_items(path: Path = Path("order_items.csv")) -> List[Dict[str, str]]:
    return read_csv(path, ["order_item_id", "order_id", "product_id", "quantity"])


def create_tables(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON;")

    conn.executescript(
        """
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS categories;
        DROP TABLE IF EXISTS users;

        CREATE TABLE users (
            user_id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE categories (
            category_id TEXT PRIMARY KEY,
            category_name TEXT NOT NULL
        );

        CREATE TABLE products (
            product_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category_id TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        );

        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        CREATE TABLE order_items (
            order_item_id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        """
    )


def insert_data(conn: sqlite3.Connection) -> None:
    categories = read_categories()
    users = read_users()
    products = read_products()
    orders = read_orders()
    order_items = read_order_items()

    conn.executemany(
        "INSERT INTO categories (category_id, category_name) VALUES (:category_id, :category_name)",
        categories,
    )
    conn.executemany(
        "INSERT INTO users (user_id, username, email, created_at) VALUES (:user_id, :username, :email, :created_at)",
        users,
    )
    conn.executemany(
        "INSERT INTO products (product_id, name, price, category_id) VALUES (:product_id, :name, :price, :category_id)",
        products,
    )
    conn.executemany(
        "INSERT INTO orders (order_id, user_id, order_date, status) VALUES (:order_id, :user_id, :order_date, :status)",
        orders,
    )
    conn.executemany(
        """
        INSERT INTO order_items (order_item_id, order_id, product_id, quantity)
        VALUES (:order_item_id, :order_id, :product_id, :quantity)
        """,
        order_items,
    )


def main() -> None:
    db_path = Path(DB_NAME)
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(DB_NAME)
    try:
        create_tables(conn)
        insert_data(conn)
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    main()


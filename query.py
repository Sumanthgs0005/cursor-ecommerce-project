import sqlite3
from pathlib import Path

DB_NAME = "ecommerce.db"


def fetch_totals(conn: sqlite3.Connection):
    query = """
        SELECT
            u.username,
            u.email,
            COALESCE(SUM(oi.quantity * p.price), 0) AS total_spent
        FROM users u
        LEFT JOIN orders o ON o.user_id = u.user_id
        LEFT JOIN order_items oi ON oi.order_id = o.order_id
        LEFT JOIN products p ON p.product_id = oi.product_id
        GROUP BY u.user_id
        ORDER BY total_spent DESC, u.username ASC
    """
    return conn.execute(query).fetchall()


def main() -> None:
    if not Path(DB_NAME).exists():
        raise FileNotFoundError(f"{DB_NAME} not found. Run ingest.py first.")

    with sqlite3.connect(DB_NAME) as conn:
        results = fetch_totals(conn)

    print(f"{'Username':<15} {'Email':<30} {'Total Spent':>12}")
    print("-" * 60)
    for username, email, total in results:
        print(f"{username:<15} {email:<30} ${total:>10.2f}")


if __name__ == "__main__":
    main()


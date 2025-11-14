import csv
import random
import string
from datetime import datetime, timedelta


def random_timestamp(start: datetime, *, day_span: int = 900) -> str:
    """Return a randomized timestamp string."""
    delta = timedelta(days=random.randint(0, day_span), seconds=random.randint(0, 86400))
    return (start + delta).strftime("%Y-%m-%d %H:%M:%S")


def build_datasets():
    random.seed(42)

    counts = {
        "users": 60,
        "categories": 50,
        "products": 75,
        "orders": 65,
        "order_items": 90,
    }

    start_date = datetime(2022, 1, 1)

    categories = [
        {"category_id": f"CAT{i:03d}", "category_name": f"Category {i}"}
        for i in range(1, counts["categories"] + 1)
    ]

    users = [
        {
            "user_id": f"U{i:03d}",
            "username": f"user{i:03d}",
            "email": f"user{i:03d}@example.com",
            "created_at": random_timestamp(start_date),
        }
        for i in range(1, counts["users"] + 1)
    ]

    products = [
        {
            "product_id": f"P{i:03d}",
            "name": f"Product {i}",
            "price": round(random.uniform(5, 250), 2),
            "category_id": random.choice(categories)["category_id"],
        }
        for i in range(1, counts["products"] + 1)
    ]

    orders = [
        {
            "order_id": f"O{i:03d}",
            "user_id": random.choice(users)["user_id"],
            "order_date": random_timestamp(start_date),
            "status": random.choice(["completed", "shipped", "processing", "cancelled"]),
        }
        for i in range(1, counts["orders"] + 1)
    ]

    order_items = [
        {
            "order_item_id": f"OI{i:03d}",
            "order_id": random.choice(orders)["order_id"],
            "product_id": random.choice(products)["product_id"],
            "quantity": random.randint(1, 5),
        }
        for i in range(1, counts["order_items"] + 1)
    ]

    return categories, users, products, orders, order_items


def write_csv(filename: str, fieldnames: list[str], rows: list[dict]):
    with open(filename, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    categories, users, products, orders, order_items = build_datasets()

    write_csv("categories.csv", ["category_id", "category_name"], categories)
    write_csv("users.csv", ["user_id", "username", "email", "created_at"], users)
    write_csv("products.csv", ["product_id", "name", "price", "category_id"], products)
    write_csv("orders.csv", ["order_id", "user_id", "order_date", "status"], orders)
    write_csv(
        "order_items.csv",
        ["order_item_id", "order_id", "product_id", "quantity"],
        order_items,
    )


if __name__ == "__main__":
    main()


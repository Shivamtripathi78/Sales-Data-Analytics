import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATABASE = BASE_DIR / "data" / "sales.db"
SQL_FILE = BASE_DIR / "queries" / "sales_analytics.sql"


def get_connection():
    DATABASE.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DATABASE)


def create_database():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.executescript("""
        PRAGMA foreign_keys = ON;

        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            city TEXT,
            email TEXT
        );

        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date DATE NOT NULL,
            payment_method TEXT,
            order_status TEXT,
            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        );

        CREATE TABLE order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id)
                REFERENCES orders(order_id),
            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        );
        """)

        customers = [
            (1, "Aarav Sharma", "Delhi", "aarav@email.com"),
            (2, "Priya Verma", "Mumbai", "priya@email.com"),
            (3, "Rahul Singh", "Lucknow", "rahul@email.com"),
            (4, "Sneha Gupta", "Noida", "sneha@email.com"),
            (5, "Aditya Kumar", "Delhi", "aditya@email.com"),
            (6, "Ananya Patel", "Jaipur", "ananya@email.com"),
            (7, "Rohan Mehta", "Pune", "rohan@email.com"),
            (8, "Kavya Mishra", "Lucknow", "kavya@email.com"),
            (9, "Arjun Yadav", "Kanpur", "arjun@email.com"),
            (10, "Isha Kapoor", "Mumbai", "isha@email.com")
        ]

        products = [
            (1, "Laptop", "Electronics", 55000),
            (2, "Smartphone", "Electronics", 25000),
            (3, "Headphones", "Accessories", 2000),
            (4, "Keyboard", "Accessories", 1500),
            (5, "Office Chair", "Furniture", 8000),
            (6, "Study Table", "Furniture", 12000),
            (7, "Smartwatch", "Electronics", 5000),
            (8, "Mouse", "Accessories", 800)
        ]

        orders = [
            (101, 1, "2026-01-05", "UPI", "Completed"),
            (102, 2, "2026-01-10", "Card", "Completed"),
            (103, 3, "2026-01-15", "Cash", "Completed"),
            (104, 4, "2026-02-02", "UPI", "Completed"),
            (105, 5, "2026-02-08", "Card", "Completed"),
            (106, 6, "2026-02-14", "UPI", "Cancelled"),
            (107, 7, "2026-03-03", "Cash", "Completed"),
            (108, 8, "2026-03-12", "Card", "Completed"),
            (109, 9, "2026-03-18", "UPI", "Completed"),
            (110, 10, "2026-04-01", "Card", "Completed"),
            (111, 1, "2026-04-10", "UPI", "Completed"),
            (112, 2, "2026-04-15", "Cash", "Cancelled"),
            (113, 3, "2026-05-04", "Card", "Completed"),
            (114, 4, "2026-05-11", "UPI", "Completed"),
            (115, 5, "2026-05-20", "Cash", "Completed"),
            (116, 6, "2026-06-02", "Card", "Completed"),
            (117, 7, "2026-06-09", "UPI", "Completed"),
            (118, 8, "2026-06-17", "Card", "Completed"),
            (119, 9, "2026-06-22", "Cash", "Completed"),
            (120, 10, "2026-06-28", "UPI", "Completed")
        ]

        order_items = [
            (1, 101, 1, 1), (2, 101, 3, 2),
            (3, 102, 2, 1), (4, 102, 4, 2),
            (5, 103, 5, 1), (6, 104, 3, 3),
            (7, 104, 8, 2), (8, 105, 6, 1),
            (9, 106, 2, 1), (10, 107, 7, 2),
            (11, 108, 1, 1), (12, 108, 8, 1),
            (13, 109, 4, 3), (14, 110, 2, 2),
            (15, 111, 5, 1), (16, 111, 3, 2),
            (17, 112, 6, 1), (18, 113, 1, 1),
            (19, 114, 7, 1), (20, 114, 3, 2),
            (21, 115, 5, 2), (22, 116, 2, 1),
            (23, 117, 8, 4), (24, 118, 6, 1),
            (25, 119, 4, 2), (26, 120, 1, 1),
            (27, 120, 7, 1)
        ]

        cursor.executemany(
            "INSERT INTO customers VALUES (?, ?, ?, ?)",
            customers
        )

        cursor.executemany(
            "INSERT INTO products VALUES (?, ?, ?, ?)",
            products
        )

        cursor.executemany(
            "INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
            orders
        )

        cursor.executemany(
            "INSERT INTO order_items VALUES (?, ?, ?, ?)",
            order_items
        )

        connection.commit()

    print("\nDatabase created successfully!")
    print("Sample data inserted successfully.")


def execute_queries():
    if not SQL_FILE.exists():
        print("SQL file not found!")
        return

    sql_content = SQL_FILE.read_text(encoding="utf-8")

    with get_connection() as connection:
        cursor = connection.cursor()

        statements = [
            statement.strip()
            for statement in sql_content.split(";")
            if statement.strip()
        ]

        for index, statement in enumerate(statements, start=1):

            if statement.lstrip().startswith("--"):
                continue

            print("\n" + "=" * 60)
            print(f"QUERY {index}")
            print("=" * 60)

            try:
                cursor.execute(statement)

                if cursor.description:
                    columns = [
                        description[0]
                        for description in cursor.description
                    ]

                    print(" | ".join(columns))
                    print("-" * 60)

                    rows = cursor.fetchall()

                    for row in rows:
                        print(" | ".join(str(value) for value in row))

                    print(f"\nTotal records: {len(rows)}")

                else:
                    print("Query executed successfully.")

            except sqlite3.Error as error:
                print("SQL Error:", error)


def main():
    while True:
        print("\n========== SALES DATA ANALYTICS ==========")
        print("1. Create Database and Insert Sample Data")
        print("2. Execute SQL Analytics Queries")
        print("3. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            create_database()

        elif choice == "2":
            execute_queries()

        elif choice == "3":
            print("Exiting application.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
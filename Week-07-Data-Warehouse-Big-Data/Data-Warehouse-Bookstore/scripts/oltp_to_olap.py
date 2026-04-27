import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


# =========================
# Sample OLTP Data
# =========================

customers = pd.DataFrame({
    "customer_id": [1, 2],
    "first_name": ["Ali", "Sara"],
    "last_name": ["Ahmed", "Mohammed"],
    "email": ["ali@example.com", "sara@example.com"],
    "country": ["Yemen", "Saudi Arabia"]
})

books = pd.DataFrame({
    "book_id": [1, 2],
    "title": ["Data Engineering Basics", "SQL for Beginners"],
    "author_name": ["John Smith", "Emily Brown"],
    "publisher_name": ["Tech Books", "Data Press"],
    "language": ["English", "English"],
    "price": [25.00, 18.50]
})

dates = pd.DataFrame({
    "date_id": [1, 2],
    "full_date": ["2026-04-27", "2026-04-28"],
    "year": [2026, 2026],
    "month": [4, 4],
    "day": [27, 28]
})

shipping = pd.DataFrame({
    "shipping_id": [1, 2],
    "method_name": ["Standard Shipping", "Express Shipping"],
    "cost": [5.00, 10.00]
})

status = pd.DataFrame({
    "status_id": [1, 2],
    "status_name": ["Delivered", "Pending"]
})


# =========================
# Fact Table
# =========================

fact_sales = pd.DataFrame({
    "sale_id": [1, 2],
    "customer_id": [1, 2],
    "book_id": [1, 2],
    "date_id": [1, 2],
    "shipping_id": [1, 2],
    "status_id": [1, 2],
    "quantity": [2, 1],
    "price": [25.00, 18.50]
})

fact_sales["total_amount"] = fact_sales["quantity"] * fact_sales["price"]


# =========================
# Export OLAP Tables
# =========================

customers.to_csv(OUTPUT_DIR / "dim_customer.csv", index=False)
books.to_csv(OUTPUT_DIR / "dim_book.csv", index=False)
dates.to_csv(OUTPUT_DIR / "dim_date.csv", index=False)
shipping.to_csv(OUTPUT_DIR / "dim_shipping.csv", index=False)
status.to_csv(OUTPUT_DIR / "dim_status.csv", index=False)
fact_sales.to_csv(OUTPUT_DIR / "fact_sales.csv", index=False)

print("Data Warehouse tables generated successfully.")
print(f"Output path: {OUTPUT_DIR}")
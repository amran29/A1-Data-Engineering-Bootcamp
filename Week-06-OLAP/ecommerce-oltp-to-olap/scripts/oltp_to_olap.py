import os
import pandas as pd
from sqlalchemy import create_engine


DB_USER = "postgres"
DB_PASSWORD = "115599"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ecommerce_db"

OUTPUT_DIR = "output"


def get_engine():
    connection_string = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    return create_engine(connection_string)


def extract_tables(engine):
    tables = {
        "orders": pd.read_sql("SELECT * FROM orders", engine),
        "order_items": pd.read_sql("SELECT * FROM order_items", engine),
        "products": pd.read_sql("SELECT * FROM products", engine),
        "users": pd.read_sql("SELECT * FROM users", engine),
        "payments": pd.read_sql("SELECT * FROM payments", engine),
        "payment_methods": pd.read_sql("SELECT * FROM payment_methods", engine),
        "branches": pd.read_sql("SELECT * FROM branches", engine),
        "categories": pd.read_sql("SELECT * FROM categories", engine),
        "brands": pd.read_sql("SELECT * FROM brands", engine),
        "currencies": pd.read_sql("SELECT * FROM currencies", engine),
    }
    return tables


def clean_orders(orders_df):
    orders = orders_df.copy()

    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    orders["status"] = orders["status"].astype(str).str.strip().str.lower()

    orders = orders.drop_duplicates(subset=["order_id"])
    orders = orders.dropna(
        subset=["order_id", "user_id", "branch_id", "currency_id", "order_date"]
    )

    return orders


def clean_order_items(order_items_df):
    order_items = order_items_df.copy()

    order_items = order_items.drop_duplicates(subset=["order_item_id"])
    order_items = order_items.dropna(
        subset=[
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_sale_price",
            "unit_purchase_price",
        ]
    )

    order_items["quantity"] = pd.to_numeric(order_items["quantity"], errors="coerce")
    order_items["unit_sale_price"] = pd.to_numeric(
        order_items["unit_sale_price"], errors="coerce"
    )
    order_items["unit_purchase_price"] = pd.to_numeric(
        order_items["unit_purchase_price"], errors="coerce"
    )

    order_items = order_items.dropna(
        subset=["quantity", "unit_sale_price", "unit_purchase_price"]
    )

    order_items = order_items[
        (order_items["quantity"] > 0)
        & (order_items["unit_sale_price"] >= 0)
        & (order_items["unit_purchase_price"] >= 0)
    ]

    return order_items


def clean_products(products_df):
    products = products_df.copy()

    products = products.drop_duplicates(subset=["product_id"])
    products = products.dropna(
        subset=["product_id", "product_name", "brand_id", "category_id"]
    )

    products["product_name"] = products["product_name"].astype(str).str.strip()
    products["purchase_price"] = pd.to_numeric(
        products["purchase_price"], errors="coerce"
    )
    products["sale_price"] = pd.to_numeric(products["sale_price"], errors="coerce")
    products["stock_quantity"] = pd.to_numeric(
        products["stock_quantity"], errors="coerce"
    )
    products["min_stock_level"] = pd.to_numeric(
        products["min_stock_level"], errors="coerce"
    )

    products = products.dropna(subset=["purchase_price", "sale_price"])
    products = products[
        (products["purchase_price"] >= 0) & (products["sale_price"] >= 0)
    ]

    return products


def build_dim_time(orders_df):
    dim_time = orders_df[["order_date"]].drop_duplicates().copy()
    dim_time["order_date"] = pd.to_datetime(dim_time["order_date"], errors="coerce")
    dim_time = dim_time.dropna(subset=["order_date"])

    dim_time["date_key"] = dim_time["order_date"].dt.strftime("%Y%m%d").astype(int)
    dim_time["full_date"] = dim_time["order_date"].dt.date
    dim_time["day"] = dim_time["order_date"].dt.day
    dim_time["month"] = dim_time["order_date"].dt.month
    dim_time["month_name"] = dim_time["order_date"].dt.month_name()
    dim_time["quarter"] = dim_time["order_date"].dt.quarter
    dim_time["year"] = dim_time["order_date"].dt.year
    dim_time["week_of_year"] = dim_time["order_date"].dt.isocalendar().week.astype(int)
    dim_time["day_name"] = dim_time["order_date"].dt.day_name()
    dim_time["is_weekend"] = dim_time["order_date"].dt.dayofweek >= 5

    dim_time = dim_time[
        [
            "date_key",
            "full_date",
            "day",
            "month",
            "month_name",
            "quarter",
            "year",
            "week_of_year",
            "day_name",
            "is_weekend",
        ]
    ].drop_duplicates()

    return dim_time.sort_values("date_key").reset_index(drop=True)


def build_dim_product(products_df, brands_df, categories_df):
    dim_product = (
        products_df.merge(
            brands_df,
            on="brand_id",
            how="left",
            suffixes=("_product", "_brand"),
        )
        .merge(categories_df, on="category_id", how="left")
        .copy()
    )

    dim_product["product_key"] = range(1, len(dim_product) + 1)

    dim_product = dim_product[
        [
            "product_key",
            "product_id",
            "product_name",
            "brand_name",
            "country_of_origin",
            "category_name",
            "purchase_price",
            "sale_price",
            "stock_quantity",
            "min_stock_level",
            "created_at_product",
        ]
    ]

    dim_product = dim_product.rename(columns={"created_at_product": "created_at"})

    return dim_product


def build_dim_customer(users_df):
    dim_customer = users_df.copy()
    dim_customer["customer_key"] = range(1, len(dim_customer) + 1)

    dim_customer = dim_customer[
        [
            "customer_key",
            "user_id",
            "full_name",
            "email",
            "phone",
            "address",
            "preferred_currency_id",
            "created_at",
        ]
    ]

    return dim_customer


def build_dim_branch(branches_df):
    dim_branch = branches_df.copy()
    dim_branch["branch_key"] = range(1, len(dim_branch) + 1)

    dim_branch = dim_branch[
        [
            "branch_key",
            "branch_id",
            "branch_name",
            "city",
            "location_details",
            "manager_name",
            "created_at",
        ]
    ]

    return dim_branch


def build_dim_payment_method(payment_methods_df):
    dim_payment_method = payment_methods_df.copy()
    dim_payment_method["payment_method_key"] = range(1, len(dim_payment_method) + 1)

    dim_payment_method = dim_payment_method[
        [
            "payment_method_key",
            "method_id",
            "method_name",
            "is_active",
        ]
    ]

    return dim_payment_method


def build_dim_currency(currencies_df):
    dim_currency = currencies_df.copy()
    dim_currency["currency_key"] = range(1, len(dim_currency) + 1)

    dim_currency = dim_currency[
        [
            "currency_key",
            "currency_id",
            "currency_code",
            "currency_name",
            "exchange_rate_to_sar",
            "created_at",
        ]
    ]

    return dim_currency


def build_fact_sales(
    orders_df,
    order_items_df,
    payments_df,
    dim_product,
    dim_customer,
    dim_branch,
    dim_payment_method,
    dim_currency,
):
    payments_one = (
        payments_df.sort_values("payment_date")
        .drop_duplicates(subset=["order_id"], keep="first")
        .copy()
    )

    fact_sales = order_items_df.merge(orders_df, on="order_id", how="left")
    fact_sales = fact_sales.merge(
        payments_one[["order_id", "method_id"]],
        on="order_id",
        how="left",
    )

    fact_sales["order_date"] = pd.to_datetime(fact_sales["order_date"], errors="coerce")
    fact_sales = fact_sales.dropna(subset=["order_date"])
    fact_sales["date_key"] = fact_sales["order_date"].dt.strftime("%Y%m%d").astype(int)

    fact_sales = fact_sales.merge(
        dim_product[["product_id", "product_key"]],
        on="product_id",
        how="left",
    )
    fact_sales = fact_sales.merge(
        dim_customer[["user_id", "customer_key"]],
        on="user_id",
        how="left",
    )
    fact_sales = fact_sales.merge(
        dim_branch[["branch_id", "branch_key"]],
        on="branch_id",
        how="left",
    )
    fact_sales = fact_sales.merge(
        dim_payment_method[["method_id", "payment_method_key"]],
        on="method_id",
        how="left",
    )
    fact_sales = fact_sales.merge(
        dim_currency[["currency_id", "currency_key"]],
        on="currency_id",
        how="left",
    )

    fact_sales["gross_sales"] = fact_sales["quantity"] * fact_sales["unit_sale_price"]
    fact_sales["total_cost"] = (
        fact_sales["quantity"] * fact_sales["unit_purchase_price"]
    )
    fact_sales["profit"] = fact_sales["gross_sales"] - fact_sales["total_cost"]

    order_counts = fact_sales.groupby("order_id")["order_id"].transform("count")
    fact_sales["allocated_tax_amount"] = fact_sales["tax_amount"] / order_counts
    fact_sales["allocated_total_amount"] = fact_sales["total_amount"] / order_counts

    fact_sales["sales_key"] = range(1, len(fact_sales) + 1)

    fact_sales = fact_sales[
        [
            "sales_key",
            "order_id",
            "order_item_id",
            "date_key",
            "customer_key",
            "product_key",
            "branch_key",
            "payment_method_key",
            "currency_key",
            "quantity",
            "unit_sale_price",
            "unit_purchase_price",
            "gross_sales",
            "total_cost",
            "profit",
            "allocated_tax_amount",
            "allocated_total_amount",
            "status",
        ]
    ]

    return fact_sales


def save_processed_data(dataframes):
    processed_dir = os.path.join("data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    for name, df in dataframes.items():
        file_path = os.path.join(processed_dir, f"{name}.csv")
        df.to_csv(file_path, index=False)
        print(f"Saved processed file: {file_path}")


def save_dataframes(dataframes):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for name, df in dataframes.items():
        file_path = os.path.join(OUTPUT_DIR, f"{name}.csv")
        df.to_csv(file_path, index=False)
        print(f"Saved: {file_path}")


def main():
    engine = get_engine()
    tables = extract_tables(engine)

    orders_clean = clean_orders(tables["orders"])
    order_items_clean = clean_order_items(tables["order_items"])
    products_clean = clean_products(tables["products"])

    save_processed_data(
        {
            "orders_clean": orders_clean,
            "order_items_clean": order_items_clean,
            "products_clean": products_clean,
        }
    )

    dim_time = build_dim_time(orders_clean)
    dim_product = build_dim_product(
        products_clean,
        tables["brands"],
        tables["categories"],
    )
    dim_customer = build_dim_customer(tables["users"])
    dim_branch = build_dim_branch(tables["branches"])
    dim_payment_method = build_dim_payment_method(tables["payment_methods"])
    dim_currency = build_dim_currency(tables["currencies"])

    fact_sales = build_fact_sales(
        orders_clean,
        order_items_clean,
        tables["payments"],
        dim_product,
        dim_customer,
        dim_branch,
        dim_payment_method,
        dim_currency,
    )

    save_dataframes(
        {
            "dim_time": dim_time,
            "dim_product": dim_product,
            "dim_customer": dim_customer,
            "dim_branch": dim_branch,
            "dim_payment_method": dim_payment_method,
            "dim_currency": dim_currency,
            "fact_sales": fact_sales,
        }
    )

    print("\nOLTP to OLAP transformation completed successfully.")


if __name__ == "__main__":
    main()
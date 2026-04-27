import pandas as pd


def extract_customers(sqlite_conn):
    return pd.read_sql("""
        SELECT
            customer_id,
            customer_unique_id,
            customer_city,
            customer_state
        FROM customers
    """, sqlite_conn)


def extract_products(sqlite_conn):
    return pd.read_sql("""
        SELECT
            p.product_id,
            p.product_category_name,
            t.product_category_name_english,
            p.product_weight_g,
            p.product_length_cm,
            p.product_height_cm,
            p.product_width_cm
        FROM products p
        LEFT JOIN product_category_name_translation t
            ON p.product_category_name = t.product_category_name
    """, sqlite_conn)


def extract_sellers(sqlite_conn):
    return pd.read_sql("""
        SELECT
            seller_id,
            seller_city,
            seller_state
        FROM sellers
    """, sqlite_conn)


def extract_orders(sqlite_conn):
    return pd.read_sql("""
        SELECT
            order_id,
            customer_id,
            order_status,
            order_purchase_timestamp,
            order_delivered_customer_date,
            order_estimated_delivery_date
        FROM orders
    """, sqlite_conn)


def extract_order_items(sqlite_conn):
    return pd.read_sql("""
        SELECT
            order_id,
            product_id,
            seller_id,
            price,
            freight_value
        FROM order_items
    """, sqlite_conn)


def extract_order_payments(sqlite_conn):
    return pd.read_sql("""
        SELECT
            order_id,
            payment_sequential,
            payment_type,
            payment_installments,
            payment_value
        FROM order_payments
    """, sqlite_conn)


def extract_order_reviews(sqlite_conn):
    return pd.read_sql("""
        SELECT
            review_id,
            order_id,
            review_score,
            review_creation_date
        FROM order_reviews
    """, sqlite_conn)
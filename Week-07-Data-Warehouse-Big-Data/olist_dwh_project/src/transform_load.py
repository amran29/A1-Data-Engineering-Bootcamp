import pandas as pd
from sqlalchemy import text
from datetime import datetime
from db_config import get_pg_engine

def generate_dim_date(start_date='2016-01-01', end_date='2019-12-31'):
    """Generates a comprehensive Date Dimension for the DWH if it doesn't exist."""
    pg_engine = get_pg_engine()
    print("\n--- Checking dim_date ---")
    
    try:
        with pg_engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM dwh.dim_date")).scalar()
            if count > 0:
                print("✅ dim_date is already populated. Skipping generation.")
                return
    except Exception:
        pass 
    
    print("--- Generating and populating dim_date ---")
    date_range = pd.date_range(start=start_date, end=end_date)
    df_date = pd.DataFrame(date_range, columns=['full_date'])
    
    df_date['date_sk'] = df_date['full_date'].dt.strftime('%Y%m%d').astype(int)
    df_date['day_of_week'] = df_date['full_date'].dt.dayofweek
    df_date['day_name'] = df_date['full_date'].dt.day_name()
    df_date['month_num'] = df_date['full_date'].dt.month
    df_date['month_name'] = df_date['full_date'].dt.month_name()
    df_date['quarter'] = df_date['full_date'].dt.quarter
    df_date['year_num'] = df_date['full_date'].dt.year
    df_date['is_weekend'] = df_date['day_of_week'].isin([5, 6])
    
    df_date.to_sql('dim_date', con=pg_engine, schema='dwh', if_exists='append', index=False)
    print("✅ dim_date populated successfully!")

def update_scd2_dimension(dim_name, stg_table, id_col, check_cols):
    """Generic function to handle SCD Type 2 logic for Customers and Sellers."""
    pg_engine = get_pg_engine()
    print(f"\n--- Updating {dim_name} (SCD Type 2) ---")

    cols_str = f"{id_col}, " + ", ".join(check_cols)
    if dim_name == "dim_customers":
        cols_str = f"{id_col}, customer_unique_id, " + ", ".join(check_cols)

    stg_query = f"SELECT {cols_str} FROM staging.{stg_table}"
    df_stg = pd.read_sql(stg_query, pg_engine)

    dwh_query = f"SELECT {cols_str} FROM dwh.{dim_name} WHERE is_current = TRUE"
    df_dwh = pd.read_sql(dwh_query, pg_engine)

    new_records = df_stg[~df_stg[id_col].isin(df_dwh[id_col])].copy()
    
    comparison = pd.merge(df_stg, df_dwh, on=id_col, suffixes=('_stg', '_dwh'))
    
    changed_mask = pd.Series(False, index=comparison.index)
    for col in check_cols:
        changed_mask |= (comparison[f'{col}_stg'].astype(str) != comparison[f'{col}_dwh'].astype(str))
    
    changed_ids = comparison.loc[changed_mask, id_col].tolist()

    with pg_engine.begin() as conn:
        if changed_ids:
            print(f"🔄 Found {len(changed_ids)} changes in {dim_name}. Expiring old records...")
            expire_sql = text(f"""
                UPDATE dwh.{dim_name} 
                SET valid_to = :now, is_current = FALSE 
                WHERE {id_col} IN :ids AND is_current = TRUE
            """)
            conn.execute(expire_sql, {"now": datetime.now(), "ids": tuple(changed_ids)})

        to_insert = pd.concat([new_records, df_stg[df_stg[id_col].isin(changed_ids)]])

        if not to_insert.empty:
            print(f"✨ Inserting {len(to_insert)} records into {dim_name}...")
            to_insert['valid_from'] = datetime.now()
            to_insert['valid_to'] = None
            to_insert['is_current'] = True
            to_insert.to_sql(dim_name, conn, schema='dwh', if_exists='append', index=False)

    print(f"✅ {dim_name} update completed!")

def update_dim_products():
    """Handles dim_products with translation merge (SCD Type 1 / Upsert logic)"""
    pg_engine = get_pg_engine()
    print("\n--- Updating dim_products ---")
    
    query = text("""
        INSERT INTO dwh.dim_products (
            product_id, product_category_name_english, product_weight_g, 
            product_length_cm, product_height_cm, product_width_cm
        )
        SELECT 
            p.product_id, t.product_category_name_english, p.product_weight_g, 
            p.product_length_cm, p.product_height_cm, p.product_width_cm
        FROM staging.products p
        LEFT JOIN staging.product_category_name_translation t 
            ON p.product_category_name = t.product_category_name
        ON CONFLICT (product_id) DO UPDATE SET
            product_category_name_english = EXCLUDED.product_category_name_english,
            product_weight_g = EXCLUDED.product_weight_g;
    """)
    with pg_engine.begin() as conn:
        conn.execute(query)
    print("✅ dim_products updated successfully!")

def load_fact_tables():
    """Populates all fact tables using data from staging and surrogate keys from DWH."""
    pg_engine = get_pg_engine()
    
    queries = {
        "fact_sales": """
            INSERT INTO dwh.fact_sales (
                order_id, order_item_id, customer_sk, seller_sk, product_sk,
                purchase_date_sk, delivered_customer_date_sk, order_status,
                order_purchase_timestamp, order_delivered_customer_date, 
                order_estimated_delivery_date, shipping_limit_date, price, freight_value
            )
            SELECT 
                oi.order_id, oi.order_item_id, c.customer_sk, s.seller_sk, p.product_sk,
                CAST(TO_CHAR(o.order_purchase_timestamp, 'YYYYMMDD') AS INTEGER),
                CAST(TO_CHAR(o.order_delivered_customer_date, 'YYYYMMDD') AS INTEGER),
                o.order_status, o.order_purchase_timestamp, o.order_delivered_customer_date,
                o.order_estimated_delivery_date, oi.shipping_limit_date, oi.price, oi.freight_value
            FROM staging.order_items oi
            JOIN staging.orders o ON oi.order_id = o.order_id
            JOIN dwh.dim_customers c ON o.customer_id = c.customer_id AND c.is_current = TRUE
            JOIN dwh.dim_sellers s ON oi.seller_id = s.seller_id AND s.is_current = TRUE
            JOIN dwh.dim_products p ON oi.product_id = p.product_id
            ON CONFLICT (order_id, order_item_id) DO NOTHING;
        """,
        "fact_payments": """
            INSERT INTO dwh.fact_payments (
                order_id, payment_sequential, customer_sk, payment_date_sk, 
                payment_type, payment_installments, payment_value
            )
            SELECT 
                op.order_id, op.payment_sequential, c.customer_sk,
                CAST(TO_CHAR(o.order_purchase_timestamp, 'YYYYMMDD') AS INTEGER),
                op.payment_type, op.payment_installments, op.payment_value
            FROM staging.order_payments op
            JOIN staging.orders o ON op.order_id = o.order_id
            JOIN dwh.dim_customers c ON o.customer_id = c.customer_id AND c.is_current = TRUE
            ON CONFLICT (order_id, payment_sequential) DO NOTHING;
        """,
        "fact_reviews": """
            INSERT INTO dwh.fact_reviews (
                review_id, order_id, customer_sk, review_date_sk, review_score, 
                review_comment_title, review_creation_date, review_answer_timestamp
            )
            SELECT 
                r.review_id, r.order_id, c.customer_sk,
                CAST(TO_CHAR(r.review_creation_date, 'YYYYMMDD') AS INTEGER),
                r.review_score, r.review_comment_title, r.review_creation_date, r.review_answer_timestamp
            FROM staging.order_reviews r
            JOIN staging.orders o ON r.order_id = o.order_id
            JOIN dwh.dim_customers c ON o.customer_id = c.customer_id AND c.is_current = TRUE
            ON CONFLICT (review_id, order_id) DO NOTHING;
        """
    }

    with pg_engine.begin() as conn:
        for table, query in queries.items():
            print(f"\n--- Loading {table} ---")
            conn.execute(text(query))
            print(f"✅ {table} populated successfully!")

if __name__ == "__main__":
    print("=== Starting Transformation and Loading Phase (DWH) ===")
    
    generate_dim_date()
    
    update_scd2_dimension(
        dim_name="dim_customers", 
        stg_table="customers", 
        id_col="customer_id", 
        check_cols=['customer_zip_code_prefix', 'customer_city', 'customer_state']
    )
    update_scd2_dimension(
        dim_name="dim_sellers", 
        stg_table="sellers", 
        id_col="seller_id", 
        check_cols=['seller_zip_code_prefix', 'seller_city', 'seller_state']
    )
    
    update_dim_products()
    load_fact_tables()
    
    print("\n=== Data Warehouse Population Completed Successfully! ===")
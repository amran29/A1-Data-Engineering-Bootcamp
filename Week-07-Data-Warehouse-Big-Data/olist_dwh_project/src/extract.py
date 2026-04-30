import pandas as pd
from sqlalchemy import text
from db_config import get_sqlite_engine, get_pg_engine

# List of columns that need to be converted from string to datetime
DATE_COLUMNS = [
    'order_purchase_timestamp', 'order_approved_at',
    'order_delivered_carrier_date', 'order_delivered_customer_date',
    'order_estimated_delivery_date', 'shipping_limit_date',
    'review_creation_date', 'review_answer_timestamp'
]

def load_table_to_staging(table_name, is_incremental=False, watermark_col=None):
    sqlite_engine = get_sqlite_engine()
    pg_engine = get_pg_engine()

    print(f"\n--- Processing Table: {table_name} ---")

    query = f"SELECT * FROM {table_name}"
    if_exists_behavior = 'replace'  # Default for full load tables

    # Incremental Load Logic
    if is_incremental and watermark_col:
        if_exists_behavior = 'append'
        watermark = None
        
        # Check for the latest record in the target PostgreSQL staging area
        try:
            with pg_engine.connect() as conn:
                result = conn.execute(text(f"SELECT MAX({watermark_col}) FROM staging.{table_name}")).scalar()
                watermark = result
        except Exception:
            pass  # Table might not exist in staging yet

        if watermark:
            print(f"📌 Incremental Load: Fetching data after {watermark}")
            query += f" WHERE {watermark_col} > '{watermark}'"
        else:
            print("📌 Initial Load (Full): No prior data found.")

    # 1. Extract Data
    df = pd.read_sql_query(query, sqlite_engine)

    if df.empty:
        print("✅ No new data found to load.")
        return

    # 2. Transform/Clean (Handling Data Quality Issues)
    # Convert string dates to actual datetime objects
    for col in df.columns:
        if col in DATE_COLUMNS:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    print(f"🚀 Extracted {len(df)} rows. Uploading to Staging area...")

    # 3. Load to Target Database
    # Using chunksize to manage memory for large datasets
    df.to_sql(
        name=table_name,
        con=pg_engine,
        schema='staging',
        if_exists=if_exists_behavior,
        index=False,
        chunksize=20000 
    )
    print(f"✅ Table {table_name} uploaded successfully!")

if __name__ == "__main__":
    print("=== Starting Data Pipeline (Extraction Phase) ===")
    
    # Static/Dimension Tables: Always Full Load to staging for easier comparison
    full_load_tables = [
        'customers', 'sellers', 'products', 'product_category_name_translation'
    ]
    for tbl in full_load_tables:
        load_table_to_staging(tbl, is_incremental=False)

    # Transaction/Fact Tables: Incremental Load based on timestamp
    incremental_tables = {
        'orders': 'order_purchase_timestamp',
        'order_reviews': 'review_creation_date',
        # Related tables without specific timestamps (Full load to staging for now)
        'order_items': None, 
        'order_payments': None 
    }

    for tbl, watermark in incremental_tables.items():
        if watermark:
            load_table_to_staging(tbl, is_incremental=True, watermark_col=watermark)
        else:
            load_table_to_staging(tbl, is_incremental=False)
            
    print("\n=== Extraction Phase Completed Successfully! ===")
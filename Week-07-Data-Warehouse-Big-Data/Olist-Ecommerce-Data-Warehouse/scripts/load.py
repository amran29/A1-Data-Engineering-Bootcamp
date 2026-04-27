from sqlalchemy import text


def truncate_tables(engine):
    tables = [
        "fact_order_items",
        "fact_payments",
        "fact_reviews",
        "dim_customer",
        "dim_product",
        "dim_seller",
        "dim_payment_type",
        "dim_date"
    ]

    with engine.connect() as conn:
        for table in tables:
            conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
        conn.commit()


def load_table(df, table_name, engine):
    print(f"🔄 Loading {table_name}...")

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False
    )

    print(f"✅ {table_name}: {len(df)} rows loaded")


def load_dimensions(
    dim_customer,
    dim_product,
    dim_seller,
    dim_payment_type,
    dim_date,
    engine
):
    load_table(dim_customer, "dim_customer", engine)
    load_table(dim_product, "dim_product", engine)
    load_table(dim_seller, "dim_seller", engine)
    load_table(dim_payment_type, "dim_payment_type", engine)
    load_table(dim_date, "dim_date", engine)


def load_facts(
    fact_order_items,
    fact_payments,
    fact_reviews,
    engine
):
    load_table(fact_order_items, "fact_order_items", engine)
    load_table(fact_payments, "fact_payments", engine)
    load_table(fact_reviews, "fact_reviews", engine)
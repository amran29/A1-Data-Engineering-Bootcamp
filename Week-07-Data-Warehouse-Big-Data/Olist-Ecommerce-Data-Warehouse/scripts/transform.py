import pandas as pd


def transform_customer(customers_df):
    dim_customer = customers_df[[
        "customer_unique_id",
        "customer_city",
        "customer_state"
    ]].drop_duplicates(subset=["customer_unique_id"])

    return dim_customer.reset_index(drop=True)


def transform_product(products_df):
    dim_product = products_df[[
        "product_id",
        "product_category_name_english",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]].drop_duplicates(subset=["product_id"])

    dim_product = dim_product.rename(columns={
        "product_category_name_english": "category_name",
        "product_weight_g": "weight_g",
        "product_length_cm": "length_cm",
        "product_height_cm": "height_cm",
        "product_width_cm": "width_cm"
    })

    return dim_product.reset_index(drop=True)


def transform_seller(sellers_df):
    dim_seller = sellers_df[[
        "seller_id",
        "seller_city",
        "seller_state"
    ]].drop_duplicates(subset=["seller_id"])

    return dim_seller.reset_index(drop=True)


def transform_payment_type(payments_df):
    dim_payment_type = payments_df[[
        "payment_type"
    ]].drop_duplicates()

    return dim_payment_type.reset_index(drop=True)


def transform_date(orders_df, reviews_df):
    order_dates = pd.to_datetime(
        orders_df["order_purchase_timestamp"],
        errors="coerce"
    ).dt.date

    review_dates = pd.to_datetime(
        reviews_df["review_creation_date"],
        errors="coerce"
    ).dt.date

    all_dates = pd.concat([order_dates, review_dates]).dropna().drop_duplicates()

    dim_date = pd.DataFrame({"full_date": all_dates})

    dim_date["full_date"] = pd.to_datetime(dim_date["full_date"])
    dim_date["year"] = dim_date["full_date"].dt.year
    dim_date["month"] = dim_date["full_date"].dt.month
    dim_date["day"] = dim_date["full_date"].dt.day
    dim_date["month_name"] = dim_date["full_date"].dt.month_name()
    dim_date["day_name"] = dim_date["full_date"].dt.day_name()
    dim_date["full_date"] = dim_date["full_date"].dt.date

    return dim_date.reset_index(drop=True)


def build_lookup(df, key_name):
    lookup = df.reset_index().rename(columns={"index": key_name})
    lookup[key_name] = lookup[key_name] + 1
    return lookup


def transform_fact_order_items(
    order_items_df,
    orders_df,
    customers_df,
    dim_customer,
    dim_product,
    dim_seller,
    dim_date
):
    fact = order_items_df.merge(
        orders_df[["order_id", "customer_id", "order_purchase_timestamp"]],
        on="order_id",
        how="left"
    )

    fact = fact.merge(
        customers_df[["customer_id", "customer_unique_id"]],
        on="customer_id",
        how="left"
    )

    fact["full_date"] = pd.to_datetime(
        fact["order_purchase_timestamp"],
        errors="coerce"
    ).dt.date

    customer_lookup = build_lookup(dim_customer, "customer_key")
    product_lookup = build_lookup(dim_product, "product_key")
    seller_lookup = build_lookup(dim_seller, "seller_key")
    date_lookup = build_lookup(dim_date, "date_key")

    fact = fact.merge(
        customer_lookup[["customer_key", "customer_unique_id"]],
        on="customer_unique_id",
        how="left"
    )

    fact = fact.merge(
        product_lookup[["product_key", "product_id"]],
        on="product_id",
        how="left"
    )

    fact = fact.merge(
        seller_lookup[["seller_key", "seller_id"]],
        on="seller_id",
        how="left"
    )

    fact = fact.merge(
        date_lookup[["date_key", "full_date"]],
        on="full_date",
        how="left"
    )

    fact["total_amount"] = fact["price"] + fact["freight_value"]

    fact_order_items = fact[[
        "order_id",
        "customer_key",
        "product_key",
        "seller_key",
        "date_key",
        "price",
        "freight_value",
        "total_amount"
    ]].dropna(subset=[
        "customer_key",
        "product_key",
        "seller_key",
        "date_key"
    ])

    return fact_order_items


def transform_fact_payments(
    payments_df,
    orders_df,
    customers_df,
    dim_customer,
    dim_date,
    dim_payment_type
):
    fact = payments_df.merge(
        orders_df[["order_id", "customer_id", "order_purchase_timestamp"]],
        on="order_id",
        how="left"
    )

    fact = fact.merge(
        customers_df[["customer_id", "customer_unique_id"]],
        on="customer_id",
        how="left"
    )

    fact["full_date"] = pd.to_datetime(
        fact["order_purchase_timestamp"],
        errors="coerce"
    ).dt.date

    customer_lookup = build_lookup(dim_customer, "customer_key")
    date_lookup = build_lookup(dim_date, "date_key")
    payment_type_lookup = build_lookup(dim_payment_type, "payment_type_key")

    fact = fact.merge(
        customer_lookup[["customer_key", "customer_unique_id"]],
        on="customer_unique_id",
        how="left"
    )

    fact = fact.merge(
        date_lookup[["date_key", "full_date"]],
        on="full_date",
        how="left"
    )

    fact = fact.merge(
        payment_type_lookup[["payment_type_key", "payment_type"]],
        on="payment_type",
        how="left"
    )

    fact_payments = fact[[
        "order_id",
        "customer_key",
        "date_key",
        "payment_type_key",
        "payment_sequential",
        "payment_installments",
        "payment_value"
    ]].dropna(subset=[
        "customer_key",
        "date_key",
        "payment_type_key"
    ])

    return fact_payments


def transform_fact_reviews(
    reviews_df,
    orders_df,
    customers_df,
    dim_customer,
    dim_date
):
    fact = reviews_df.merge(
        orders_df[["order_id", "customer_id"]],
        on="order_id",
        how="left"
    )

    fact = fact.merge(
        customers_df[["customer_id", "customer_unique_id"]],
        on="customer_id",
        how="left"
    )

    fact["full_date"] = pd.to_datetime(
        fact["review_creation_date"],
        errors="coerce"
    ).dt.date

    customer_lookup = build_lookup(dim_customer, "customer_key")
    date_lookup = build_lookup(dim_date, "date_key")

    fact = fact.merge(
        customer_lookup[["customer_key", "customer_unique_id"]],
        on="customer_unique_id",
        how="left"
    )

    fact = fact.merge(
        date_lookup[["date_key", "full_date"]],
        on="full_date",
        how="left"
    )

    fact_reviews = fact[[
        "review_id",
        "order_id",
        "customer_key",
        "date_key",
        "review_score"
    ]].dropna(subset=[
        "customer_key",
        "date_key"
    ])

    return fact_reviews
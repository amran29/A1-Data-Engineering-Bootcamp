-- =========================
-- DIMENSION TABLES
-- =========================

CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_unique_id VARCHAR(50) NOT NULL,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);

CREATE INDEX idx_dim_customer_unique_id
ON dim_customer(customer_unique_id);


-- -------------------------

CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    category_name VARCHAR(100),
    weight_g DOUBLE PRECISION,
    length_cm DOUBLE PRECISION,
    height_cm DOUBLE PRECISION,
    width_cm DOUBLE PRECISION
);

CREATE INDEX idx_dim_product_id
ON dim_product(product_id);


-- -------------------------

CREATE TABLE dim_seller (
    seller_key SERIAL PRIMARY KEY,
    seller_id VARCHAR(50) NOT NULL,
    seller_city VARCHAR(100),
    seller_state VARCHAR(10)
);

CREATE INDEX idx_dim_seller_id
ON dim_seller(seller_id);


-- -------------------------

CREATE TABLE dim_payment_type (
    payment_type_key SERIAL PRIMARY KEY,
    payment_type VARCHAR(50) UNIQUE
);


-- -------------------------

CREATE TABLE dim_date (
    date_key SERIAL PRIMARY KEY,
    full_date DATE UNIQUE,
    year INT,
    month INT,
    day INT,
    month_name VARCHAR(20),
    day_name VARCHAR(20)
);

CREATE INDEX idx_dim_date_full_date
ON dim_date(full_date);


-- =========================
-- FACT TABLE: ORDER ITEMS
-- =========================

CREATE TABLE fact_order_items (
    order_item_key SERIAL PRIMARY KEY,

    order_id VARCHAR(50) NOT NULL,

    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    seller_key INT NOT NULL,
    date_key INT NOT NULL,

    price NUMERIC(10,2),
    freight_value NUMERIC(10,2),
    total_amount NUMERIC(10,2),

    CONSTRAINT fk_order_items_customer
        FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),

    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_key) REFERENCES dim_product(product_key),

    CONSTRAINT fk_order_items_seller
        FOREIGN KEY (seller_key) REFERENCES dim_seller(seller_key),

    CONSTRAINT fk_order_items_date
        FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

CREATE INDEX idx_fact_order_items_order_id
ON fact_order_items(order_id);


-- =========================
-- FACT TABLE: PAYMENTS
-- =========================

CREATE TABLE fact_payments (
    payment_key SERIAL PRIMARY KEY,

    order_id VARCHAR(50) NOT NULL,

    customer_key INT NOT NULL,
    date_key INT NOT NULL,
    payment_type_key INT NOT NULL,

    payment_sequential INT,
    payment_installments INT,
    payment_value NUMERIC(10,2),

    CONSTRAINT fk_payments_customer
        FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),

    CONSTRAINT fk_payments_date
        FOREIGN KEY (date_key) REFERENCES dim_date(date_key),

    CONSTRAINT fk_payments_type
        FOREIGN KEY (payment_type_key) REFERENCES dim_payment_type(payment_type_key)
);

CREATE INDEX idx_fact_payments_order_id
ON fact_payments(order_id);


-- =========================
-- FACT TABLE: REVIEWS
-- =========================

CREATE TABLE fact_reviews (
    review_key SERIAL PRIMARY KEY,

    review_id VARCHAR(50) NOT NULL,
    order_id VARCHAR(50) NOT NULL,

    customer_key INT NOT NULL,
    date_key INT NOT NULL,

    review_score INT,

    CONSTRAINT fk_reviews_customer
        FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),

    CONSTRAINT fk_reviews_date
        FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

CREATE INDEX idx_fact_reviews_order_id
ON fact_reviews(order_id);
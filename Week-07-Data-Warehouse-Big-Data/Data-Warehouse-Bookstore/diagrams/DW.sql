-- =========================
-- DIMENSION TABLES
-- =========================

CREATE TABLE dim_customer (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(150),
    country VARCHAR(100)
);

CREATE TABLE dim_book (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    author_name VARCHAR(255),
    publisher_name VARCHAR(255),
    language VARCHAR(50),
    price NUMERIC(10,2)
);

CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    full_date DATE,
    year INT,
    month INT,
    day INT
);

CREATE TABLE dim_shipping (
    shipping_id SERIAL PRIMARY KEY,
    method_name VARCHAR(100),
    cost NUMERIC(10,2)
);

CREATE TABLE dim_status (
    status_id SERIAL PRIMARY KEY,
    status_name VARCHAR(100)
);

-- =========================
-- FACT TABLE
-- =========================

CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,

    customer_id INT,
    book_id INT,
    date_id INT,
    shipping_id INT,
    status_id INT,

    quantity INT,
    price NUMERIC(10,2),
    total_amount NUMERIC(10,2),

    CONSTRAINT fk_customer FOREIGN KEY (customer_id)
        REFERENCES dim_customer(customer_id),

    CONSTRAINT fk_book FOREIGN KEY (book_id)
        REFERENCES dim_book(book_id),

    CONSTRAINT fk_date FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id),

    CONSTRAINT fk_shipping FOREIGN KEY (shipping_id)
        REFERENCES dim_shipping(shipping_id),

    CONSTRAINT fk_status FOREIGN KEY (status_id)
        REFERENCES dim_status(status_id)
);
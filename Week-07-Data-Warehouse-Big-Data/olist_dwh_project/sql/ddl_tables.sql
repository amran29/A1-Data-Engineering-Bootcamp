-- ==============================================================================
-- 1. المخططات (Schemas)
-- ==============================================================================
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS dwh;

-- ==============================================================================
-- 2. جداول الأبعاد المشتركة (Conformed Dimensions)
-- ==============================================================================

-- أ. بُعد التاريخ (Date Dimension) - أساسي جداً لأي مستودع بيانات احترافي
CREATE TABLE dwh.dim_date (
    date_sk INT PRIMARY KEY,                     -- مثال: 20231024
    full_date DATE NOT NULL,
    day_of_week INT,
    day_name VARCHAR(10),
    month_num INT,
    month_name VARCHAR(15),
    quarter INT,
    year_num INT,
    is_weekend BOOLEAN
);

-- ب. بُعد العملاء (SCD Type 2)
CREATE TABLE dwh.dim_customers (
    customer_sk SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,            
    customer_unique_id VARCHAR(50) NOT NULL,     
    customer_zip_code_prefix VARCHAR(10),
    customer_city VARCHAR(100),
    customer_state VARCHAR(5),
    -- تتبع التغيرات التاريخية
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP,
    is_current BOOLEAN DEFAULT TRUE
);
CREATE INDEX idx_dim_cust_id ON dwh.dim_customers(customer_id);

-- ج. بُعد البائعين (SCD Type 2)
CREATE TABLE dwh.dim_sellers (
    seller_sk SERIAL PRIMARY KEY,
    seller_id VARCHAR(50) NOT NULL,
    seller_zip_code_prefix VARCHAR(10),
    seller_city VARCHAR(100),
    seller_state VARCHAR(5),
    -- تتبع التغيرات التاريخية
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP,
    is_current BOOLEAN DEFAULT TRUE
);
CREATE INDEX idx_dim_sell_id ON dwh.dim_sellers(seller_id);

-- د. بُعد المنتجات (SCD Type 1) - تم دمج الترجمة هنا
CREATE TABLE dwh.dim_products (
    product_sk SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL UNIQUE,
    product_category_name_english VARCHAR(100), 
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT
);

-- ==============================================================================
-- 3. جداول الحقائق (Fact Tables) - كل عملية تجارية لها جدول
-- ==============================================================================

-- أ. جدول حقائق المبيعات والتوصيل (Fact Sales)
-- Grain: One row per order item
CREATE TABLE dwh.fact_sales (
    order_id VARCHAR(50) NOT NULL,
    order_item_id INT NOT NULL,
    
    -- مفاتيح الربط (Foreign Keys)
    customer_sk INT REFERENCES dwh.dim_customers(customer_sk),
    seller_sk INT REFERENCES dwh.dim_sellers(seller_sk),
    product_sk INT REFERENCES dwh.dim_products(product_sk),
    
    -- مفاتيح التواريخ (للربط مع dim_date)
    purchase_date_sk INT REFERENCES dwh.dim_date(date_sk),
    delivered_customer_date_sk INT REFERENCES dwh.dim_date(date_sk),
    
    -- تواريخ التفاصيل (Timestamps)
    order_status VARCHAR(20),
    order_purchase_timestamp TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,
    shipping_limit_date TIMESTAMP,
    
    -- المقاييس (Measures)
    price NUMERIC(10, 2),
    freight_value NUMERIC(10, 2),
    
    PRIMARY KEY (order_id, order_item_id)
);

-- ب. جدول حقائق المدفوعات (Fact Payments)
-- Grain: One row per payment line per order
-- لاحظ أنه لا يرتبط بالبائع أو المنتج، لأن الدفع يتم للطلب ككل
CREATE TABLE dwh.fact_payments (
    order_id VARCHAR(50) NOT NULL,
    payment_sequential INT NOT NULL,
    
    customer_sk INT REFERENCES dwh.dim_customers(customer_sk),
    payment_date_sk INT REFERENCES dwh.dim_date(date_sk), -- بناءً على تاريخ الطلب
    
    payment_type VARCHAR(50),
    payment_installments INT,
    payment_value NUMERIC(10, 2),
    
    PRIMARY KEY (order_id, payment_sequential)
);

-- ج. جدول حقائق التقييمات (Fact Reviews)
-- Grain: One row per review
CREATE TABLE dwh.fact_reviews (
    review_id VARCHAR(50) NOT NULL,
    order_id VARCHAR(50) NOT NULL,
    
    customer_sk INT REFERENCES dwh.dim_customers(customer_sk),
    review_date_sk INT REFERENCES dwh.dim_date(date_sk),
    
    review_score INT,
    review_comment_title TEXT,
    
    -- تواريخ دقيقة
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,
    
    PRIMARY KEY (review_id, order_id)
);

-- ==============================================================================
-- 4. تحسين الأداء (Performance Optimization)
-- ==============================================================================
CREATE INDEX idx_fact_sales_cust ON dwh.fact_sales(customer_sk);
CREATE INDEX idx_fact_sales_date ON dwh.fact_sales(purchase_date_sk);
CREATE INDEX idx_fact_pay_cust ON dwh.fact_payments(customer_sk);
CREATE INDEX idx_fact_rev_score ON dwh.fact_reviews(review_score);
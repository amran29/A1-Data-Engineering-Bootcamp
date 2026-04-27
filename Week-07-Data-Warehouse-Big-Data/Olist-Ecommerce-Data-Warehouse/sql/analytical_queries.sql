-- =====================================================
-- Olist Data Warehouse - Sample Analytical Queries
-- =====================================================


-- 1. Sales trend over time (monthly revenue)
SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.total_amount) AS total_revenue,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM fact_order_items f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;


-- 2. Top 10 most valuable customers
SELECT
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    SUM(f.total_amount) AS total_spent,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM fact_order_items f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY
    c.customer_unique_id,
    c.customer_city,
    c.customer_state
ORDER BY total_spent DESC
LIMIT 10;


-- 3. Revenue by product category
SELECT
    p.category_name,
    SUM(f.total_amount) AS total_revenue,
    COUNT(*) AS total_items_sold
FROM fact_order_items f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.category_name
ORDER BY total_revenue DESC;


-- 4. Revenue by seller
SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    SUM(f.total_amount) AS total_revenue,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM fact_order_items f
JOIN dim_seller s
    ON f.seller_key = s.seller_key
GROUP BY
    s.seller_id,
    s.seller_city,
    s.seller_state
ORDER BY total_revenue DESC
LIMIT 10;


-- 5. Payment method performance
SELECT
    pt.payment_type,
    COUNT(*) AS payment_count,
    SUM(fp.payment_value) AS total_payment_value,
    AVG(fp.payment_value) AS avg_payment_value
FROM fact_payments fp
JOIN dim_payment_type pt
    ON fp.payment_type_key = pt.payment_type_key
GROUP BY pt.payment_type
ORDER BY total_payment_value DESC;


-- 6. Average review score over time
SELECT
    d.year,
    d.month,
    d.month_name,
    AVG(fr.review_score) AS avg_review_score,
    COUNT(*) AS total_reviews
FROM fact_reviews fr
JOIN dim_date d
    ON fr.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;


-- 7. Review score by customer state
SELECT
    c.customer_state,
    AVG(fr.review_score) AS avg_review_score,
    COUNT(*) AS total_reviews
FROM fact_reviews fr
JOIN dim_customer c
    ON fr.customer_key = c.customer_key
GROUP BY c.customer_state
ORDER BY avg_review_score DESC;


-- 8. Best product categories by review score and revenue
SELECT
    p.category_name,
    SUM(foi.total_amount) AS total_revenue,
    AVG(fr.review_score) AS avg_review_score
FROM fact_order_items foi
JOIN dim_product p
    ON foi.product_key = p.product_key
JOIN fact_reviews fr
    ON foi.order_id = fr.order_id
GROUP BY p.category_name
ORDER BY total_revenue DESC, avg_review_score DESC;


-- 9. Daily revenue
SELECT
    d.full_date,
    SUM(f.total_amount) AS daily_revenue,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM fact_order_items f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.full_date
ORDER BY d.full_date;


-- 10. Orders by weekday
SELECT
    d.day_name,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.total_amount) AS total_revenue
FROM fact_order_items f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.day_name
ORDER BY total_orders DESC;
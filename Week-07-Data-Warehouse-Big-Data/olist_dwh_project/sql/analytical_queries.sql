/* ==============================================================================
   Olist E-Commerce Data Warehouse - Analytical Queries
   Description: These queries answer the core business questions required 
                for the project evaluation, utilizing the Star/Galaxy Schema.
============================================================================== */

-- ------------------------------------------------------------------------------
-- 1. How are sales trending over time?
-- Answers: Monthly revenue and order volume trends.
-- ------------------------------------------------------------------------------
SELECT 
    d.year_num, 
    d.month_name, 
    SUM(f.price) AS total_revenue,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM dwh.fact_sales f
JOIN dwh.dim_date d 
    ON f.purchase_date_sk = d.date_sk
GROUP BY 
    d.year_num, 
    d.month_name, 
    d.month_num
ORDER BY 
    d.year_num ASC, 
    d.month_num ASC;


-- ------------------------------------------------------------------------------
-- 2. Who are the most valuable customers?
-- Answers: Top 10 customers based on their total payment value.
-- ------------------------------------------------------------------------------
SELECT 
    c.customer_unique_id, 
    c.customer_city,
    c.customer_state,
    SUM(p.payment_value) AS total_spent,
    COUNT(p.order_id) AS number_of_payments
FROM dwh.fact_payments p
JOIN dwh.dim_customers c 
    ON p.customer_sk = c.customer_sk
GROUP BY 
    c.customer_unique_id, 
    c.customer_city,
    c.customer_state
ORDER BY 
    total_spent DESC
LIMIT 10;


-- ------------------------------------------------------------------------------
-- 3. Which products/categories drive revenue?
-- Answers: Top 10 product categories by total revenue generated.
-- ------------------------------------------------------------------------------
SELECT 
    p.product_category_name_english AS category_name, 
    SUM(f.price) AS total_revenue,
    COUNT(f.order_item_id) AS total_items_sold
FROM dwh.fact_sales f
JOIN dwh.dim_products p 
    ON f.product_sk = p.product_sk
WHERE 
    p.product_category_name_english IS NOT NULL
GROUP BY 
    p.product_category_name_english
ORDER BY 
    total_revenue DESC
LIMIT 10;


-- ------------------------------------------------------------------------------
-- 4. What affects delivery performance?
-- Answers: Average delay in days categorized by the seller's state, 
--          focusing only on orders that arrived later than estimated.
-- ------------------------------------------------------------------------------
SELECT 
    s.seller_state,
    COUNT(f.order_item_id) AS total_delayed_items,
    ROUND(
        AVG(EXTRACT(EPOCH FROM (f.order_delivered_customer_date - f.order_estimated_delivery_date)) / 86400), 2
    ) AS avg_delay_in_days
FROM dwh.fact_sales f
JOIN dwh.dim_sellers s 
    ON f.seller_sk = s.seller_sk
WHERE 
    f.order_status = 'delivered' 
    AND f.order_delivered_customer_date > f.order_estimated_delivery_date
GROUP BY 
    s.seller_state
ORDER BY 
    avg_delay_in_days DESC;
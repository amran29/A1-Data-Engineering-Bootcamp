-- Create the target table for real-time ingestion
CREATE TABLE IF NOT EXISTS realtime_sales (
    transaction_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    price NUMERIC(10, 2),
    event_time TIMESTAMP
);

-- Note: 'transaction_id' is the PRIMARY KEY. 
-- This is MANDATORY for NiFi to perform an UPSERT operation in PostgreSQL.
-- ============================================================================
-- Script 2: Slowly Changing Dimension (SCD Type 2) Implementation Without Transactions
-- ============================================================================

USE customer_dw;

-- 1. Create and Load the Historical SCD2 Table (from customer_scd2_mixed.csv)
CREATE TABLE IF NOT EXISTS customer_scd2_history (
    CustomerID STRING,
    Name STRING,
    Email STRING,
    Phone_Number STRING,
    Address STRING,
    JOIN_Date STRING,
    Start_Date STRING,
    End_Date STRING,
    Is_Current STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   "separatorChar" = ",", 
   "quoteChar" = "\""
)
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA LOCAL INPATH '/workspace/data/customer_scd2_mixed.csv' INTO TABLE customer_scd2_history;


-- 2. Create and Load the Staging Table for new/updated data
CREATE TABLE IF NOT EXISTS customer_updates_staging (
    CustomerID STRING,
    Name STRING,
    Email STRING,
    Phone_Number STRING,
    Address STRING,
    JOIN_Date STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   "separatorChar" = ",", 
   "quoteChar" = "\""
)
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA LOCAL INPATH '/workspace/data/customer_updated.csv' INTO TABLE customer_updates_staging;


-- 3. Implement SCD Type 2 using INSERT OVERWRITE and UNION ALL
-- This workaround reconstructs the entire dataset without using UPDATE/DELETE
INSERT OVERWRITE TABLE customer_scd2_history
SELECT * FROM (

    -- Query A: Identify completely NEW records from staging that don't exist in history yet
    -- Assign them current_date as Start_Date, NULL as End_Date, and '1' as Is_Current
    SELECT 
        u.CustomerID, u.Name, u.Email, u.Phone_Number, u.Address, u.JOIN_Date,
        CAST(current_date() AS STRING) as Start_Date,
        NULL as End_Date,
        '1' as Is_Current
    FROM customer_updates_staging u
    LEFT JOIN customer_scd2_history h ON u.CustomerID = h.CustomerID
    WHERE h.CustomerID IS NULL

    UNION ALL

    -- Query B: Close out EXISTING records that received an update
    -- Set End_Date to current_date and Is_Current to '0' to track history
    SELECT 
        h.CustomerID, h.Name, h.Email, h.Phone_Number, h.Address, h.JOIN_Date,
        h.Start_Date,
        CAST(current_date() AS STRING) as End_Date,
        '0' as Is_Current
    FROM customer_scd2_history h
    JOIN customer_updates_staging u ON h.CustomerID = u.CustomerID
    WHERE h.Is_Current = '1'

    UNION ALL

    -- Query C: Insert the UPDATED rows as the new active records
    -- Assign current_date as Start_Date, NULL as End_Date, and '1' as Is_Current
    SELECT 
        u.CustomerID, u.Name, u.Email, u.Phone_Number, u.Address, u.JOIN_Date,
        CAST(current_date() AS STRING) as Start_Date,
        NULL as End_Date,
        '1' as Is_Current
    FROM customer_updates_staging u
    JOIN customer_scd2_history h ON u.CustomerID = h.CustomerID
    WHERE h.Is_Current = '1'

    UNION ALL

    -- Query D: Keep untouched historical/active records intact
    -- This includes previously closed records ('0') or active records ('1') that weren't updated
    SELECT 
        h.CustomerID, h.Name, h.Email, h.Phone_Number, h.Address, h.JOIN_Date,
        h.Start_Date,
        h.End_Date,
        h.Is_Current
    FROM customer_scd2_history h
    LEFT JOIN customer_updates_staging u ON h.CustomerID = u.CustomerID
    WHERE u.CustomerID IS NULL OR h.Is_Current = '0'

) scd2_final_result;

-- 4. Verify the final implementation by checking records grouped by CustomerID
SELECT CustomerID, Name, Start_Date, End_Date, Is_Current 
FROM customer_scd2_history 
ORDER BY CustomerID, Is_Current;
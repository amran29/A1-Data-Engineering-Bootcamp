-- ============================================================================
-- Script 1: Internal vs External Tables & Handling CSV Delimiters
-- ============================================================================

-- 1. Create a database for the Data Warehouse
CREATE DATABASE IF NOT EXISTS customer_dw;
USE customer_dw;

-- 2. Create an INTERNAL Table
-- Using OpenCSVSerde to properly parse addresses containing commas
-- Note: OpenCSVSerde requires all columns to be defined as STRING
CREATE TABLE IF NOT EXISTS internal_customers (
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
   "quoteChar"     = "\""
)
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

-- Load data from the mapped docker volume
LOAD DATA LOCAL INPATH '/workspace/data/customer_updated.csv' INTO TABLE internal_customers;


-- 3. Create an EXTERNAL Table
CREATE EXTERNAL TABLE IF NOT EXISTS external_customers (
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
   "quoteChar"     = "\""
)
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/customer_ext_data'
TBLPROPERTIES ("skip.header.line.count"="1");

-- Load data from the mapped docker volume
LOAD DATA LOCAL INPATH '/workspace/data/customer_updated.csv' INTO TABLE external_customers;


-- 4. Drop both tables to demonstrate the difference in behavior
DROP TABLE internal_customers;
DROP TABLE external_customers;

-- ============================================================================
-- OBSERVATION:
-- Dropping 'internal_customers' deletes both Hive metadata and HDFS data.
-- Dropping 'external_customers' deletes ONLY the Hive metadata. Data in HDFS remains.
-- ============================================================================
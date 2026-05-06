# Hive Data Warehouse: SCD Type 2 Implementation

**Author:** Amran Al-gaafari

## Overview
This repository contains the completion of the Data Engineering assignment focusing on Apache Hive. The project addresses core data warehousing challenges including parsing semi-structured CSV delimiters, managing Hive table behaviors (Internal vs. External), and implementing a Slowly Changing Dimension (SCD Type 2) architecture without relying on transactional (ACID) updates or deletes.

## Project Structure

    Customer-SCD2-Pipeline/
    ├── data/
    │   ├── customer_scd2_mixed.csv     # Initial historical dataset
    │   └── customer_updated.csv        # Incoming updates/new records
    ├── notebooks/
    │   └── 00_data_exploration.ipynb   # Pandas profiling to identify data issues
    ├── scripts/
    │   ├── 01_internal_vs_external.hql # Table creation and delimiter fix
    │   └── 02_scd2_implementation.hql  # SCD2 pipeline logic
    ├── docker-compose.yml              # Infrastructure as Code (Hive + Postgres)
    └── .env                            # Environment variables


## Assignment Objectives & Solutions

### 1. Delimiter Issue Resolution
* **The Challenge:** The `Address` column in the source files contained internal commas (e.g., `"123 Main St, Apt 4"`). Standard CSV parsers in Hive would incorrectly split this single column into multiple columns.
* **The Solution:** Implemented `org.apache.hadoop.hive.serde2.OpenCSVSerde` in the Table DDL. This instructed Hive to respect quote boundaries (`"quoteChar" = "\""`) and ignore commas enclosed within them, solving the parsing issue without altering the source files.

### 2. Internal vs. External Tables Observation
As part of the assignment, both Internal (Managed) and External tables were created, populated, and then dropped to observe HDFS behavior:
* **Internal Table:** Executing `DROP TABLE internal_customers;` resulted in the complete deletion of both the table metadata from the Hive Metastore AND the actual physical data stored in HDFS.
* **External Table:** Executing `DROP TABLE external_customers;` only removed the metadata. The underlying data files remained perfectly intact and secure in the HDFS location (`/user/hive/warehouse/customer_ext_data`).

### 3. SCD Type 2 Workaround (Without Transactions)
* **The Challenge:** Native Hive (without ACID transaction configurations) does not support `UPDATE` or `DELETE` row-level operations, making standard SCD Type 2 tracking difficult.
* **The Solution:** Engineered a workaround using the `INSERT OVERWRITE` strategy combined with a multi-part `UNION ALL` query. The logic performs the following in a single pass:
  1. Identifies and inserts entirely **new records** (`is_current='1'`, `end_date=NULL`).
  2. Identifies modified records and **closes historical versions** (`is_current='0'`, `end_date=current_date()`).
  3. Inserts the **updated rows as the new active state** (`is_current='1'`, `end_date=NULL`).
  4. Retains all **untouched historical and active records**.

## How to Run the Project (Docker Environment)

**1. Start the Infrastructure:**
    docker-compose up -d

**2. Initialize the Metastore (First run only):**
    docker exec -it hive_scd2_env bash
    schematool -dbType postgres -initSchema

**3. Execute the Hive Pipelines:**
    hive -f /workspace/scripts/01_internal_vs_external.hql
    hive -f /workspace/scripts/02_scd2_implementation.hql
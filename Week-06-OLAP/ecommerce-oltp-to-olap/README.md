# E-commerce OLTP to OLAP Project

## Overview
This project transforms an e-commerce PostgreSQL database from an OLTP (Online Transaction Processing) model into an OLAP (Online Analytical Processing) model using Python and pandas.

The transformation enables efficient analytical queries and reporting by restructuring transactional data into a Star Schema.

---

## Objective
The main objective of this project is to:

- Extract transactional data from an OLTP database
- Clean and preprocess the data
- Transform it into an OLAP model (Star Schema)
- Enable fast and efficient data analysis

---

## Data Layers

The project follows a structured data pipeline:

- `data/raw/` → Contains original source data (SQL file)
- `data/processed/` → Contains cleaned intermediate datasets
- `output/` → Contains final OLAP tables (Fact & Dimensions)

---

## OLTP Tables
The original database includes transactional tables such as:

- orders
- order_items
- products
- users
- payments
- branches
- brands
- categories
- currencies
- payment_methods

These tables are optimized for transactions but not for analysis.

---

## OLAP Model (Star Schema)

The data was transformed into a Star Schema consisting of:

### ⭐ Fact Table
- `fact_sales`
  - Contains measurable data such as:
    - sales
    - cost
    - profit
    - quantity

### 📊 Dimension Tables
- `dim_time`
- `dim_product`
- `dim_customer`
- `dim_branch`
- `dim_payment_method`
- `dim_currency`

---

## Fact Table Grain
Each row in the fact table represents:

> **One order item (one product in one order)**

This allows detailed analysis at the product level.

---

## Data Processing

The project includes a data cleaning step:

- Handling missing values
- Removing duplicates
- Converting data types
- Filtering invalid records

Cleaned data is stored in:


data/processed/


---

## Tools & Technologies

- Python
- pandas
- PostgreSQL
- SQLAlchemy
- psycopg2
- Jupyter Notebook (for analysis)

---

## Analytical Insights

Using the OLAP model, we can easily perform:

- Total sales analysis
- Profit calculation
- Sales by branch
- Top-selling products
- Monthly sales trends

---

## Output Files

The OLAP tables are saved as CSV files:


output/
├── dim_time.csv
├── dim_product.csv
├── dim_customer.csv
├── dim_branch.csv
├── dim_payment_method.csv
├── dim_currency.csv
└── fact_sales.csv


---

## How to Run

1. Create and activate virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt
Run the ETL script:
python scripts/oltp_to_olap.py
(Optional) Run analysis notebook:
notebooks/analysis.ipynb
Result

The OLTP database was successfully transformed into an OLAP model using a Star Schema, enabling efficient data analysis and reporting.

Key Concepts Demonstrated
OLTP vs OLAP
Star Schema Design
Fact and Dimension Tables
Data Cleaning & Transformation
ETL Pipeline using pandas
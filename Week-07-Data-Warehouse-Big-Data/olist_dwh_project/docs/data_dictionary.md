# 📖 Olist Data Warehouse - Data Dictionary

This document provides a detailed description of the tables and columns available in the **Olist Data Warehouse (DWH)** schema. It is designed to help Data Analysts and BI Developers understand the available data for reporting.

---

## 1. Dimension Tables

### `dim_customers`
Stores customer details and tracks historical geographical changes using SCD Type 2.
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `customer_sk` | Integer | Surrogate Key (Primary Key). |
| `customer_id` | String | Transactional system ID (per order). |
| `customer_unique_id` | String | Unique identifier for a specific customer. |
| `customer_zip_code_prefix` | String | First 5 digits of the customer's zip code. |
| `customer_city` | String | Customer's city. |
| `customer_state` | String | Customer's state code. |
| `valid_from` | Timestamp | Start date of the record's validity (SCD2). |
| `valid_to` | Timestamp | End date of the record's validity (SCD2). NULL if current. |
| `is_current` | Boolean | TRUE if this is the most recent address for the customer. |

### `dim_sellers`
Stores seller details and tracks geographical changes (SCD Type 2).
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `seller_sk` | Integer | Surrogate Key (Primary Key). |
| `seller_id` | String | Original ID from the source system. |
| `seller_city` | String | Seller's city. |
| `seller_state` | String | Seller's state code. |
| `valid_from` | Timestamp | Start date of the record's validity. |
| `valid_to` | Timestamp | End date of the record's validity. |
| `is_current` | Boolean | TRUE if this is the active record. |

### `dim_products`
Stores product attributes. Uses SCD Type 1 (Upsert) to maintain the latest state.
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `product_sk` | Integer | Surrogate Key (Primary Key). |
| `product_id` | String | Original product ID. |
| `product_category_name_english` | String | English translation of the product category. |
| `product_weight_g` | Float | Product weight in grams. |

### `dim_date`
A comprehensive date dimension for time-series analysis.
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `date_sk` | Integer | Date stored as an integer (e.g., 20180125). Primary Key. |
| `full_date` | Date | The actual date value. |
| `year_num` | Integer | Year (e.g., 2018). |
| `month_num` | Integer | Month number (1-12). |
| `month_name` | String | Name of the month (e.g., January). |
| `is_weekend` | Boolean | TRUE if the day is Saturday or Sunday. |

---

## 2. Fact Tables

### `fact_sales`
Captures transactional data at the **Order Item level**.
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `order_id` | String | Unique identifier of the order. |
| `order_item_id` | Integer | Sequential number identifying number of items included in the same order. |
| `customer_sk` | Integer | Foreign key linking to `dim_customers`. |
| `seller_sk` | Integer | Foreign key linking to `dim_sellers`. |
| `product_sk` | Integer | Foreign key linking to `dim_products`. |
| `purchase_date_sk` | Integer | Foreign key linking to `dim_date` (purchase time). |
| `price` | Float | Item price. |
| `freight_value` | Float | Item freight value (shipping cost). |

### `fact_payments`
Captures payment methods and values at the **Payment Sequential level**.
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `order_id` | String | Unique identifier of the order. |
| `payment_sequential` | Integer | Sequence of payment (if an order is paid with multiple methods). |
| `customer_sk` | Integer | Foreign key linking to `dim_customers`. |
| `payment_type` | String | Method of payment (e.g., credit_card, boleto). |
| `payment_value` | Float | Transaction value. |
# 📊 Apache Spark Labs - Week 10

## Developed by **Amran Al-gaafari**

Welcome to the Week 10 repository for the Data Engineering Training Program. This project contains practical data processing labs using **Apache Spark (PySpark)**, running on a local Docker cluster.

## 📂 Project Structure

```text
📁 Week-10-Apache-Spark/
├── 📄 docker-compose.yml                  # Spark Cluster Docker Configuration
├── 📁 01-RDD-Lab-Employees/               # Lab 01: Spark RDDs
│   └── 📓 rdd_lab.ipynb                   # RDD transformations & data quality
└── 📁 02-Spark-DataFrames-Lab/            # Lab 02: Spark DataFrames
    ├── 📓 01_spark_dataframe_basics.ipynb # Schemas & null values handling
    └── 📓 02_dataframe_transformations.ipynb # Joins, deduplication & categorization
```

# 🧪 Labs Overview

---

## 🔹 Lab 01: RDD Employees
**Goal:** Process semi-structured text data using Resilient Distributed Datasets (RDDs).

### Key Tasks:
- ✅ Validated data quality and isolated corrupted records.
- ✅ Calculated the average salary per department.
- ✅ Computed the employee headcount for each department.

---

## 🔹 Lab 02: Spark DataFrames
**Goal:** Process structured relational data using Spark SQL DataFrames.

### Key Tasks:
- ✅ Enforced explicit data schemas.
- ✅ Cleaned data by replacing or dropping null values.
- ✅ Resolved data duplication issues before performing an inner join.
- ✅ Categorized salaries (Low, Medium, High) using `when` / `otherwise` (Case When).

---

## 🚀 How to Run

### 1. Start the Spark environment using Docker:
```bash
docker-compose up -d
```

### 2. Open the Jupyter Notebooks (`.ipynb`) in Visual Studio Code.

### 3. Ensure the kernel is connected to the Spark container and run the cells sequentially.

---


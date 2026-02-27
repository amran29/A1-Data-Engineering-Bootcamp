# Cafe Sales Data Cleaning Project
**Developer:** Amran Algaafari  
**Date:** February 2026

## Project Overview
[cite_start]This project focuses on cleaning and preprocessing a "dirty" dataset of cafe sales[cite: 3]. [cite_start]The dataset contained various data quality issues, including missing values, incorrect data types, and invalid entries[cite: 11, 15]. [cite_start]The goal was to transform this raw data into a clean, structured CSV file ready for analysis[cite: 4, 23].

## Tech Stack
* [cite_start]**Language:** Python [cite: 6]
* [cite_start]**Libraries:** pandas, numpy [cite: 2]
* [cite_start]**Environment:** Jupyter Notebook (VS Code) 

## Data Cleaning Steps
[cite_start]Following the assignment requirements, the pipeline performs the following[cite: 6]:
1. [cite_start]**Data Loading**: Using pandas to load the raw CSV and handling invalid strings like "ERROR" or "UNKNOWN"[cite: 7, 8, 11].
2. [cite_start]**Type Correction**: Converting columns to appropriate types (e.g., Transaction Date to datetime)[cite: 9, 10].
3. **Handling Missing Values**:
    * [cite_start]Categorical columns: Filled with "Unknown" or mode[cite: 14].
    * [cite_start]Numerical columns: Imputed or dropped based on logical relevance[cite: 13].
4. **Consistency Checks**:
    * [cite_start]Restored missing Item names using Price Per Unit mapping[cite: 18].
    * [cite_start]Calculated missing `Total Spent` and `Price Per Unit` using the formula: $Total Spent = Quantity \times Price$[cite: 19, 20].
5. [cite_start]**Feature Engineering**: Derived a new `season` column based on the transaction month[cite: 21, 22].

## How to Run
1. Ensure you have Python installed.
2. Install dependencies: `pip install pandas numpy jupyter`.
3. Open `data_preprocessing.ipynb` in VS Code.
4. [cite_start]Run all cells to generate the `cleaned_cafe_sales.csv` file[cite: 23].

## Final Results
* **Processed Rows**: ~9,022 clean records.
* [cite_start]**Output**: `cleaned_cafe_sales.csv` with zero missing values[cite: 23].
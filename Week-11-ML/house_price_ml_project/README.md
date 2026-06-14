# House Price Prediction using Machine Learning

## Project Overview

This project demonstrates the fundamentals of Machine Learning using a simple house price prediction model.

The goal is to predict the price of a house based on:

* Area
* Number of Bedrooms
* House Age

The project was built as a beginner-friendly introduction to:

* Data Analysis
* Data Visualization
* Linear Regression
* Train/Test Split
* Machine Learning Workflow

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-Learn
* Jupyter Notebook

---

## Dataset

The dataset contains the following columns:

| Column   | Description        |
| -------- | ------------------ |
| area     | House area         |
| bedrooms | Number of bedrooms |
| age      | House age in years |
| price    | House price        |

---

## Machine Learning Workflow

### 1. Data Preparation

The dataset was loaded and explored using Pandas.

### 2. Data Visualization

Relationships between variables were analyzed using:

* Scatter Plots
* Pair Plots
* Correlation Matrix

### 3. Feature Selection

Features (X):

* area
* bedrooms
* age

Target (y):

* price

### 4. Model Training

A Linear Regression model was trained using Scikit-Learn.

```python
model = LinearRegression()
model.fit(X, y)
```

### 5. Prediction

Example prediction:

```python
new_house = pd.DataFrame({
    "area": [220],
    "bedrooms": [4],
    "age": [1]
})

prediction = model.predict(new_house)
```

---

## Key Concepts Learned

* Dataset
* Features
* Target Variable
* Correlation Analysis
* Data Visualization
* Linear Regression
* Model Training
* Prediction
* Train/Test Split
* Model Evaluation

---

## Project Structure

```text
house_price_ml_project/
│
├── data/
│   └── houses.csv
│
├── notebooks/
│   └── 01_house_price_prediction.ipynb
│
├── README.md
│
└── requirements.txt
```

---

## Author

Amran Al-gaafari

Information Systems Graduate

Learning Path:
Data Engineering → Machine Learning → Data Science

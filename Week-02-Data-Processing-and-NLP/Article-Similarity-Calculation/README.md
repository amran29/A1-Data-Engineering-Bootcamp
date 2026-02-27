# Article Similarity Calculation Project

## 👤 Author
**Amran Algaafari**

---

## 📝 Project Description
This project is a Python-based tool designed to analyze text articles, clean their content, and calculate the similarity between them using the **Cosine Similarity** algorithm. It follows a modular structure to ensure clean and maintainable code.

The project implements a **Bag-of-Words (BoW)** representation and utilizes numerical operations to determine how closely related different articles are based on their vocabulary.

## 🛠️ Features & Workflow
The application performs the following steps as per the assignment requirements:
1.  **Data Loading:** Reads article data from a CSV file using Python's built-in `csv` module (No Pandas used).
2.  **Text Cleaning:** 
    *   Converts text to lowercase.
    *   Removes all punctuation and special characters.
    *   Removes numerical digits.
    *   Tokenizes content into individual words.
3.  **Vocabulary Building:** Creates a global unique vocabulary from all articles.
4.  **Vector Representation:** Converts articles into binary vectors (0 or 1) based on word presence.
5.  **Similarity Calculation:** Computes a similarity matrix using **NumPy** for high-performance numerical operations.
6.  **Persistence:** Saves the resulting matrix into a Python pickle file (`similarities.pkl`).
7.  **Search Functionality:** Provides a function to find the top 3 most similar articles to a given article ID.

## 📂 Project Structure
*   `main.py`: The entry point of the application. It orchestrates the workflow.
*   `similarity.py`: Contains all the core logic, functions for text processing, and mathematical calculations.
*   `articles.csv`: The input dataset containing article IDs, titles, and content.
*   `similarities.pkl`: The generated output file containing the similarity matrix.

## 🚀 How to Run
1.  **Install Dependencies:**
    Make sure you have `numpy` installed:
    ```bash
    pip install numpy
    ```
2.  **Execute the Project:**
    Run the main script from your terminal:
    ```bash
    python main.py
    ```

## 🧪 Technologies Used
*   **Python 3.x**
*   **NumPy** (for numerical computations)
*   **Regular Expressions (re)** (for text cleaning)
*   **Pickle** (for data serialization)
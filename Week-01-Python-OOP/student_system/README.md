# 🎓 Student Performance Analyzer System

A professional Python-based system designed to manage and analyze student academic performance. This project demonstrates advanced software engineering principles including Object-Oriented Programming (OOP), Modular Architecture, and Clean Code.

## 👤 Author
**Amran Al-gaafari**

---

## 🚀 Key Features
- **Student Management**: Add, search (by ID or Name), and remove students.
- **Advanced Analytics**:
    - Top and Lowest performing students.
    - Full class ranking from highest to lowest.
    - Grade distribution analysis (A, B, C, D, F).
- **Data Persistence**: Automatic saving and loading from `CSV` files.
- **Robust Validation**: Comprehensive input validation to prevent system crashes.
- **Professional Architecture**: Separation of concerns across multiple modules.

---

## 📂 Project Structure
```text
student_system/
│
├── main.py          # Application Layer (Interactive CLI Menu)
├── models.py        # Domain Layer (OOP Classes: Student & Classroom)
├── analytics.py     # Logic Layer (Statistical Analysis & Ranking)
├── utils.py         # Utility Layer (File I/O & Input Validation)
└── data.csv         # Data Storage (Auto-generated)

🛠️ Technical Concepts Used
Object-Oriented Programming (OOP):
Encapsulation: Private attributes (e.g., __grades) to protect data integrity.
Decorators: Used @staticmethod and @classmethod for specialized logic.
Clean Architecture: Decoupling the business logic from the user interface.
Error Handling: Using try...except blocks to handle file errors and invalid inputs.
File Handling: Using Python's csv module for persistent storage.
💻 How to Run
Ensure you have Python 3.x installed.
Clone or download the project folder.
Open your terminal/command prompt and navigate to the project directory.
Run the application:
paython main.py
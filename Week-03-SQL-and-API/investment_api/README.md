# 📈 Investment Portfolio Tracker - Backend API

A robust and secure RESTful API built to manage financial assets, including stocks, cryptocurrencies, and precious metals. This project is designed with a focus on data integrity, relational mapping, and secure user isolation.

**Developer:** Amran Al-gaafari

## 🚀 Tech Stack
- **FastAPI**: High-performance Python framework for building APIs.
- **PostgreSQL**: Reliable relational database for storing user and asset data.
- **SQLAlchemy**: ORM for managing complex database relationships (One-to-Many).
- **JWT (JSON Web Tokens)**: Secure authentication and session management.
- **Bcrypt**: Industrial-grade password hashing.
- **Pydantic**: Data validation and settings management.

## ✨ Key Features
- **User Authentication**: Secure Register/Login system with encrypted passwords.
- **Data Isolation**: Each user can only access and manage their own portfolio (Strict Ownership).
- **Full Asset CRUD**: Create, Read, Update, and Delete financial assets.
- **Relational Architecture**: Seamless link between users and their diverse asset classes.
- **Auto-Generated Documentation**: Interactive API docs via Swagger UI.

## 📁 Project Structure
- `app/models/`: Database models defining the relational schema.
- `app/schemas/`: Pydantic models for request/response validation.
- `app/controllers/`: Core business logic and database operations.
- `app/routes/`: API endpoints organized by resource (Auth, Assets).
- `app/security.py`: Logic for JWT handling, hashing, and dependency injection.

## ⚙️ Setup & Installation
1. **Clone the repository.**
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
# System Architecture

## Overview

This project is a complete data pipeline that collects, processes, stores, and exposes product data through an API.

It is composed of multiple layers working together:

- Scraping Layer
- Processing Layer
- Storage Layer
- API Layer
- Service Layer

---

## 1. Scraping Layer

Responsible for extracting raw data from the target website.

Tools used:
- requests
- BeautifulSoup

Steps:
1. Send HTTP request to the website
2. Parse HTML content
3. Extract product details (name, price, rating, etc.)

---

## 2. Processing Layer

Responsible for cleaning and transforming raw data.

Tasks:
- Remove extra spaces
- Convert price to numeric format
- Normalize ratings
- Validate fields

This ensures consistent and usable data before storing.

---

## 3. Storage Layer

Responsible for saving data into the database.

Technology:
- PostgreSQL
- SQLAlchemy (ORM)

Why PostgreSQL:
- Better than SQLite for real-world applications
- Supports scalability
- Used widely in production systems

---

## 4. API Layer

Responsible for exposing the data via HTTP endpoints.

Technology:
- FastAPI

Main responsibilities:
- Provide endpoints for data access
- Handle search and filtering
- Accept new data (POST requests)

---

## 5. Service Layer

Responsible for running the application in the background.

Technology:
- systemd

Responsibilities:
- Start the app automatically
- Restart on failure
- Run as a system service

---

## 6. Network Layer

Responsible for allowing access to the API.

Technology:
- UFW (Uncomplicated Firewall)

Configuration:
- Open port 8000 for incoming traffic

---

## 7. Deployment Layer

Responsible for packaging and distributing the application.

Technology:
- Debian packaging (.deb)

Benefits:
- Easy installation on Ubuntu
- Reproducible deployment
- Includes service + dependencies setup

---

## Data Flow Summary

1. Scraper fetches HTML from website
2. Data is parsed and extracted
3. Data is cleaned and normalized
4. Data is stored in PostgreSQL
5. FastAPI serves the data via API
6. systemd keeps the service running
7. UFW allows external access
8. Debian package makes installation easy

---

## Design Advantages

- Modular structure (easy to maintain)
- Clear separation of responsibilities
- Production-like environment
- Scalable architecture
- Automated deployment


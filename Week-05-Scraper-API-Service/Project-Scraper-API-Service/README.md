# Scraper API Service

A complete data engineering mini-project that starts with a web scraping script and ends with a deployable Ubuntu service and Debian package.

## Project Overview

This project scrapes product data from a public e-commerce test website, cleans and normalizes the data, stores it in PostgreSQL, and exposes it through FastAPI endpoints.

The application is designed to run as a background Linux service using `systemd`, with firewall configuration using `ufw`, and can be installed using a `.deb` package.

## Target Website

- Source: Webscraper.io test e-commerce site
- Category used: Laptops

## Main Features

- Scrape product data from the website
- Clean and normalize product records
- Store data in PostgreSQL
- Expose data through FastAPI endpoints
- Search, filter, and sort products
- Run as a background service with `systemd`
- Open API port using `ufw`
- Package the whole application as a `.deb` file

## Tech Stack

- Python
- Requests
- BeautifulSoup
- PostgreSQL
- SQLAlchemy
- FastAPI
- Uvicorn
- systemd
- UFW
- Debian Packaging

## Project Structure

```bash
app/
scripts/
data/
docs/
systemd/
debian/
tests/
main.py
requirements.txt
README.md
.gitignore

Data Flow
The scraper fetches product HTML from the source website
The cleaner transforms raw product data into structured records
The cleaned records are inserted into PostgreSQL
FastAPI exposes the stored data through HTTP endpoints
systemd runs the application as a Linux background service
UFW opens port 8000 for network access
Debian packaging makes the service installable on other Ubuntu systems
Database Schema

Table: products

Fields:

id
name
price
description
rating
category
product_url
image_url
created_at
API Endpoints
GET /health
GET /products
GET /products/{product_id}
GET /products/search?q=...
GET /products/rating/{rating}
GET /products/cheap?limit=...
POST /products
POST /scrape
Example Usage

Health check:

curl http://127.0.0.1:8000/health

Run scraping:

curl -X POST http://127.0.0.1:8000/scrape

Get all products:

curl http://127.0.0.1:8000/products
Service Management

Start service:

sudo systemctl start scraper-api.service

Check service status:

sudo systemctl status scraper-api.service

Enable service on boot:

sudo systemctl enable scraper-api.service
Firewall

Open port 8000:

sudo ufw allow 8000/tcp
Debian Package

The project can be packaged as a Debian package and installed using:

sudo dpkg -i scraper-api-service_1.0.0-1_all.deb
Design Decisions
PostgreSQL was used instead of SQLite because it is closer to production systems and supports the bootcamp SQL topics.
FastAPI was used because it is simple, modern, and automatically provides API documentation.
systemd was used because the project requirement asked for a Linux background service.
A Debian package was created to make deployment easier and reproducible on Ubuntu systems.
Author

Created as part of the Data Engineering Bootcamp weekly project.

# Scraper API Service

A complete data engineering mini-project that starts with a web scraping script and ends with a deployable Ubuntu service.

## Project Idea

This project scrapes product data from an e-commerce test website, cleans and structures the data, stores it in PostgreSQL, and exposes it through FastAPI endpoints.

The final application is designed to run as a background service on Ubuntu using systemd, with firewall configuration and Debian packaging support.

## Main Features

- Scrape product data from a public website
- Clean and normalize the scraped data
- Store data in PostgreSQL
- Expose the data through FastAPI endpoints
- Run as a Linux service using systemd
- Prepare the project for packaging as a `.deb` package

## Tech Stack

- Python
- BeautifulSoup
- Requests
- PostgreSQL
- SQLAlchemy
- FastAPI
- Uvicorn
- systemd
- UFW
- Debian packaging

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
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://webscraper.io"
CATEGORY_URL = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"


def fetch_products():
    response = requests.get(CATEGORY_URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    items = soup.find_all("div", class_="thumbnail")

    for item in items:
        title_tag = item.find("a", class_="title")
        price_tag = item.find("h4", class_="price")
        description_tag = item.find("p", class_="description")

        if not title_tag or not price_tag or not description_tag:
            continue

        name = title_tag.get_text(strip=True)
        price = price_tag.get_text(strip=True)
        description = description_tag.get_text(strip=True)

        product_url = urljoin(BASE_URL, title_tag.get("href", ""))

        image_tag = item.find("img")
        image_url = urljoin(BASE_URL, image_tag.get("src", "")) if image_tag else None

        rating = 0
        rating_tag = item.find("p", attrs={"data-rating": True})
        if rating_tag:
            rating = int(rating_tag.get("data-rating", 0))

        products.append({
            "name": name,
            "price": price,
            "description": description,
            "rating": rating,
            "category": "laptops",
            "product_url": product_url,
            "image_url": image_url,
        })

    return products
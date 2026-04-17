def clean_price(price_str: str) -> float:
    # مثال: "$295.99" → 295.99
    return float(price_str.replace("$", "").strip())


def clean_product(product: dict) -> dict:
    return {
        "name": product["name"],
        "price": clean_price(product["price"]),
        "description": product["description"],
        "rating": int(product["rating"]),
        "category": product["category"],
        "product_url": product["product_url"],
        "image_url": product["image_url"],
    }
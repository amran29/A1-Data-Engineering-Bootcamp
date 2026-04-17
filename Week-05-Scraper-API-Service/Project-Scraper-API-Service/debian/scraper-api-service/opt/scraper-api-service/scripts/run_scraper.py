from app.scraper import fetch_products
from app.cleaner import clean_product
from app.database import SessionLocal
from app import crud, schemas


def main():
    print("Fetching products...")
    raw_products = fetch_products()

    print(f"Fetched {len(raw_products)} products")

    cleaned = [clean_product(p) for p in raw_products]

    db = SessionLocal()

    try:
        products_to_insert = [schemas.ProductCreate(**p) for p in cleaned]
        crud.create_products_bulk(db, products_to_insert)
        print("Products inserted successfully!")
    finally:
        db.close()


if __name__ == "__main__":
    main()
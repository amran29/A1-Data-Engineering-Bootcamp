from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.scraper import fetch_products
from app.cleaner import clean_product

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/products", response_model=list[schemas.ProductResponse])
def read_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)


@router.get("/products/search", response_model=list[schemas.ProductResponse])
def search_products(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return crud.search_products(db, q)


@router.get("/products/rating/{rating}", response_model=list[schemas.ProductResponse])
def read_products_by_rating(rating: int, db: Session = Depends(get_db)):
    return crud.get_products_by_rating(db, rating)


@router.get("/products/cheap", response_model=list[schemas.ProductResponse])
def read_cheapest_products(limit: int = 5, db: Session = Depends(get_db)):
    return crud.get_cheapest_products(db, limit)


@router.get("/products/{product_id}", response_model=schemas.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/products", response_model=schemas.ProductResponse)
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@router.post("/scrape")
def run_scraping(db: Session = Depends(get_db)):
    raw_products = fetch_products()
    cleaned_products = [clean_product(p) for p in raw_products]
    products_to_insert = [schemas.ProductCreate(**p) for p in cleaned_products]

    crud.clear_products(db)
    crud.create_products_bulk(db, products_to_insert)

    return {
        "message": "Scraping completed successfully",
        "inserted_count": len(products_to_insert)
    }
from sqlalchemy import text
from sqlalchemy.orm import Session
from app import models, schemas


def get_all_products(db: Session):
    return db.query(models.Product).order_by(models.Product.id.asc()).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def search_products(db: Session, query: str):
    return (
        db.query(models.Product)
        .filter(models.Product.name.ilike(f"%{query}%"))
        .order_by(models.Product.id.asc())
        .all()
    )


def get_products_by_rating(db: Session, rating: int):
    return (
        db.query(models.Product)
        .filter(models.Product.rating == rating)
        .order_by(models.Product.id.asc())
        .all()
    )


def get_cheapest_products(db: Session, limit: int = 5):
    return (
        db.query(models.Product)
        .order_by(models.Product.price.asc())
        .limit(limit)
        .all()
    )


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def create_products_bulk(db: Session, products: list[schemas.ProductCreate]):
    db_products = [models.Product(**p.model_dump()) for p in products]
    db.add_all(db_products)
    db.commit()
    return db_products


def clear_products(db: Session):
    db.execute(text("TRUNCATE TABLE products RESTART IDENTITY;"))
    db.commit()
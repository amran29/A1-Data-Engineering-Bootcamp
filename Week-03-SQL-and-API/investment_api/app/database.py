import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# إنشاء المحرك (Engine)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# إنشاء جلسة العمل (Session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# الأساس الذي ستورث منه جميع الموديلات (Models)
Base = declarative_base()

# دالة للحصول على الاتصال (Dependency Injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
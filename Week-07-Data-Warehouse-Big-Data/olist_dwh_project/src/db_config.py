import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# تحميل المتغيرات من ملف .env
load_dotenv()

# إعدادات اتصال قاعدة بيانات SQLite (المصدر)
SQLITE_DB_PATH = 'data/raw/olist.sqlite'
SQLITE_CONN_STR = f'sqlite:///{SQLITE_DB_PATH}'

# إعدادات اتصال قاعدة بيانات PostgreSQL (الهدف) من متغيرات البيئة
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_DB = os.getenv('PG_DB')

PG_CONN_STR = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'

def get_sqlite_engine():
    """ينشئ ويعيد محرك اتصال SQLite"""
    return create_engine(SQLITE_CONN_STR)

def get_pg_engine():
    """ينشئ ويعيد محرك اتصال PostgreSQL"""
    return create_engine(PG_CONN_STR)
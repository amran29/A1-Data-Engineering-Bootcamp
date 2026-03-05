from fastapi import FastAPI
from app.database import engine, Base
from app.routes import auth_routes, asset_routes

# إنشاء الجداول في قاعدة البيانات تلقائياً عند التشغيل
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Investment Portfolio API")

# ربط المسارات
app.include_router(auth_routes.router)
app.include_router(asset_routes.router)

@app.get("/")
def home():
    return {"message": "Welcome to Investment API. Go to /docs for Swagger UI"}

#uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
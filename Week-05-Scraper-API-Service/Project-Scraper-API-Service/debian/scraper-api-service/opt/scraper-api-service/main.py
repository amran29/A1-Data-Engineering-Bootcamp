from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="Scraper API Service",
    description="A web scraping project exposed through FastAPI",
    version="1.0.0"
)

app.include_router(router)

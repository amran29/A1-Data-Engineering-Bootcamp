import re
import shutil
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup


BASE_URL = "http://books.toscrape.com/"
START_URL = "http://books.toscrape.com/catalogue/category/books_1/page-1.html"


BASE_DIR = Path(__file__).resolve().parent
RAW_DATA_DIR = BASE_DIR / "raw_data"
RAW_IMAGES_DIR = BASE_DIR / "raw_images"
CLEANED_DATA_DIR = BASE_DIR / "cleaned_data"
CLEANED_IMAGES_DIR = BASE_DIR / "cleaned_images"


def create_folders():
    """
    إنشاء جميع المجلدات المطلوبة للمشروع
    """
    RAW_DATA_DIR.mkdir(exist_ok=True)
    RAW_IMAGES_DIR.mkdir(exist_ok=True)
    CLEANED_DATA_DIR.mkdir(exist_ok=True)
    CLEANED_IMAGES_DIR.mkdir(exist_ok=True)

    for rating in range(1, 6):
        (CLEANED_IMAGES_DIR / str(rating)).mkdir(parents=True, exist_ok=True)


def safe_filename(name: str) -> str:
    """
    تنظيف اسم الملف من الرموز غير المناسبة
    """
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip()


def clean_price(price_text: str) -> float:
    """
    تحويل السعر من نص مثل £51.77 إلى float
    """
    cleaned = re.sub(r"[^\d.]", "", price_text)
    return float(cleaned)


def convert_rating_to_int(rating_text: str) -> int:
    """
    تحويل التقييم من نص إلى رقم
    """
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }
    return rating_map[rating_text]


def get_soup(url: str) -> BeautifulSoup:
    """
    إرسال الطلب وإرجاع BeautifulSoup object
    """
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def download_image(img_url: str, image_path: Path):
    """
    تحميل الصورة وحفظها داخل المسار المحدد
    """
    response = requests.get(img_url, timeout=30)
    response.raise_for_status()

    with open(image_path, "wb") as file:
        file.write(response.content)


def scrape_books(max_pages: int = 3) -> list[dict]:
    """
    سحب البيانات الخام من الموقع
    """
    raw_books = []
    current_page = 1
    url = START_URL

    while url and current_page <= max_pages:
        soup = get_soup(url)
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            name = book.h3.a["title"].strip()
            price = book.find("p", class_="price_color").text.strip()
            rating = book.find("p", class_="star-rating")["class"][1]

            img_src = book.find("img")["src"]
            img_url = urljoin(url, img_src)

            image_name = safe_filename(name) + ".jpg"
            image_path = RAW_IMAGES_DIR / image_name

            download_image(img_url, image_path)

            raw_books.append({
                "name": name,
                "price": price,
                "rating": rating,
                "image_path": str(image_path)
            })

        print(f"Page {current_page} scraped successfully.")

        current_page += 1
        next_button = soup.find("li", class_="next")

        if next_button and current_page <= max_pages:
            url = f"http://books.toscrape.com/catalogue/category/books_1/page-{current_page}.html"
        else:
            url = None

    return raw_books


def save_raw_data(raw_books: list[dict]) -> pd.DataFrame:
    """
    حفظ البيانات الخام في CSV
    """
    raw_df = pd.DataFrame(raw_books)
    raw_csv_path = RAW_DATA_DIR / "raw_data.csv"
    raw_df.to_csv(raw_csv_path, index=False, encoding="utf-8-sig")
    print(f"Raw data saved to: {raw_csv_path}")
    return raw_df


def clean_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    تنظيف البيانات وتحويل الأنواع
    """
    cleaned_df = raw_df.copy()

    cleaned_df["name"] = cleaned_df["name"].astype(str)
    cleaned_df["price"] = cleaned_df["price"].apply(clean_price)
    cleaned_df["rating"] = cleaned_df["rating"].apply(convert_rating_to_int).astype(int)

    return cleaned_df


def organize_images_by_rating(cleaned_df: pd.DataFrame):
    """
    نسخ الصور إلى مجلدات منفصلة حسب التقييم
    """
    for _, row in cleaned_df.iterrows():
        rating = row["rating"]
        old_image_path = Path(row["image_path"])

        new_image_path = CLEANED_IMAGES_DIR / str(rating) / old_image_path.name
        shutil.copy2(old_image_path, new_image_path)

    print("Images organized by rating successfully.")


def save_cleaned_data_by_rating(cleaned_df: pd.DataFrame):
    """
    حفظ البيانات المنظفة في ملفات CSV منفصلة حسب التقييم
    مع تحديث image_path إلى المسار الجديد
    """
    for rating_value in sorted(cleaned_df["rating"].unique()):
        rating_df = cleaned_df[cleaned_df["rating"] == rating_value].copy()

        updated_paths = []
        for _, row in rating_df.iterrows():
            old_image_path = Path(row["image_path"])
            new_image_path = CLEANED_IMAGES_DIR / str(rating_value) / old_image_path.name
            updated_paths.append(str(new_image_path))

        rating_df["image_path"] = updated_paths

        output_csv = CLEANED_DATA_DIR / f"{rating_value}.csv"
        rating_df.to_csv(output_csv, index=False, encoding="utf-8-sig")

        print(f"Cleaned data saved to: {output_csv}")


def run_pipeline(max_pages: int = 3):
    """
    تشغيل المشروع كاملًا
    """
    print("Creating folders...")
    create_folders()

    print("Scraping books...")
    raw_books = scrape_books(max_pages=max_pages)

    print("Saving raw data...")
    raw_df = save_raw_data(raw_books)

    print("Cleaning data...")
    cleaned_df = clean_data(raw_df)

    print("Organizing images...")
    organize_images_by_rating(cleaned_df)

    print("Saving cleaned data by rating...")
    save_cleaned_data_by_rating(cleaned_df)

    print("Pipeline completed successfully.")
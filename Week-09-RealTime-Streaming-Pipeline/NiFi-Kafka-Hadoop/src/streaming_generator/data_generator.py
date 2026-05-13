import random
from faker import Faker
from datetime import datetime

fake = Faker()

class ECommerceGenerator:
    def __init__(self):
        self.products = ['Laptop', 'Smartphone', 'Headphones', 'Smartwatch', 'Tablet', 'Monitor']
        self.timestamp_formats = ["%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M", "%Y/%m/%d", "Invalid-Date"]

    def generate_row(self):
        # تحديد نوع السجل (صحيح أم متسخ)
        anomaly_type = random.choices(
            ['valid', 'missing', 'duplicate', 'invalid_format', 'corrupted_numeric', 'corrupted_row'],
            weights=[70, 5, 5, 10, 5, 5] # توزيع الاحتمالات
        )[0]

        # البيانات الأساسية
        transaction_id = random.randint(10000, 99999)
        customer_id = f"CUST-{random.randint(100, 999)}"
        product = random.choice(self.products)
        amount = round(random.uniform(10.0, 2000.0), 2)
        ts = datetime.now().strftime(self.timestamp_formats[0])

        # حقن الأخطاء بناءً على النوع
        if anomaly_type == 'missing':
            customer_id = "" # قيمة مفقودة
        
        elif anomaly_type == 'invalid_format':
            ts = datetime.now().strftime(random.choice(self.timestamp_formats[1:]))
        
        elif anomaly_type == 'corrupted_numeric':
            amount = "ERROR_PRICE" # خطأ رقمي
        
        elif anomaly_type == 'corrupted_row':
            return "NULL,NULL,STOLEN_DATA,000,UNKNOWN" # سطر تالف تماماً

        return [transaction_id, customer_id, product, amount, ts]

    def get_headers(self):
        return ["transaction_id", "customer_id", "product_name", "amount", "timestamp"]
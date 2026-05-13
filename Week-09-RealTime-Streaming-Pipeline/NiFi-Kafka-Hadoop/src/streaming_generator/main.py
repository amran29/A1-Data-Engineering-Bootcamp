import pandas as pd
import time
import os
from data_generator import ECommerceGenerator

# إعداد المسارات
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

generator = ECommerceGenerator()

def start_streaming(file_count=100, records_per_file=10):
    print(f"🚀 Starting Real-Time Data Generation in: {OUTPUT_DIR}")
    
    for i in range(file_count):
        records = []
        # توليد مجموعة من السجلات لكل ملف
        for _ in range(records_per_file):
            row = generator.generate_row()
            records.append(row)
        
        # تحويل البيانات إلى DataFrame وحفظها كـ CSV
        file_name = f"stream_batch_{int(time.time())}.csv"
        file_path = os.path.join(OUTPUT_DIR, file_name)
        
        df = pd.DataFrame(records) # دع بانداز يحدد عدد الأعمدة تلقائياً
        df.to_csv(file_path, index=False)
        
        print(f"✅ Generated: {file_name} with {records_per_file} records.")
        
        # محاكاة الاستمرارية (انتظر 5 ثوانٍ قبل توليد الملف التالي)
        time.sleep(5)

if __name__ == "__main__":
    try:
        start_streaming()
    except KeyboardInterrupt:
        print("\n🛑 Generation stopped by user.")
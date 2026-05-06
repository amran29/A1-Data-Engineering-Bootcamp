import os
import time
import random
import csv
from datetime import datetime

# Define the output directory for NiFi to ingest from
OUTPUT_DIR = "./nifi_input_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Sample data for simulation
PRODUCTS = ["Laptop", "Smartphone", "Headphones", "Monitor", "Keyboard", "Tablet"]

def generate_messy_record():
    """Generates a single record with intentional messy data for transformation practice."""
    # Generate a random ID between 100 and 999
    record_id = random.randint(100, 999)
    product = random.choice(PRODUCTS)
    price = round(random.uniform(50.0, 2000.0), 2)
    
    # Introduce messy data (15% chance for each error type)
    error_chance = random.random()
    
    if error_chance < 0.15:
        price = None  # Missing value
    elif error_chance < 0.30:
        product = product.lower()  # Inconsistent formatting (lowercase instead of Title Case)
        
    # Timestamp of the event
    event_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return [record_id, product, price, event_timestamp]

def create_data_file():
    """Creates a CSV file with a timestamped filename containing random records."""
    # Instructor Requirement: Filename must include a timestamp
    current_time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sales_stream_{current_time_str}.csv"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    records = []
    num_records = random.randint(10, 25)
    
    for _ in range(num_records):
        record = generate_messy_record()
        records.append(record)
        
        # Introduce duplicates (10% chance)
        if random.random() < 0.10:
            records.append(record)
            
    # Write records to the CSV file
    with open(filepath, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write Header
        writer.writerow(["transaction_id", "product_name", "price", "event_time"])
        # Write Data
        writer.writerows(records)
        
    print(f"[SUCCESS] Generated {filename} containing {len(records)} records.")

if __name__ == "__main__":
    print(f"[*] Starting Real-Time Data Simulation...")
    print(f"[*] Destination Directory: {OUTPUT_DIR}")
    print(f"[*] Press Ctrl+C to stop.")
    print("-" * 40)
    
    try:
        while True:
            create_data_file()
            # Wait for 5 seconds before generating the next file
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[*] Data simulation stopped by user. Exiting gracefully.")
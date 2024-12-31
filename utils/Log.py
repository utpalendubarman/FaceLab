import csv
import os
from datetime import datetime

def Log(type, message):
    file_path="log.csv"
    log_entry = {
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Type': type,
        'Message': message
    }
    file_exists = os.path.exists(file_path)
    
    # Open the file in append mode
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Timestamp', 'Type', 'Message'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)
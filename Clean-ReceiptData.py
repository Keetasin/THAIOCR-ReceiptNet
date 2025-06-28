import csv
import json
import os
from rapidfuzz import process, fuzz

product_list = []
with open('dataset/product_list.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        product_list.append(row['product_name'])

input_folder = 'data/json_data'
output_folder = 'data/cleaned_data'
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(input_folder, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            receipt = json.load(f)

        output_lines = [f"📂 ไฟล์: {filename}\n"]

        if 'items' in receipt:
            for item in receipt['items']:
                item_name = item['name'].replace("|", "").strip()
                match_tuple = process.extractOne(item_name, product_list, scorer=fuzz.token_sort_ratio)

                if match_tuple is not None:
                    match, score, _ = match_tuple
                    if score >= 35:
                        item['name'] = match  # แก้ไขชื่อโดยตรง
                    output_lines.append(f"📦 จากใบเสร็จ: {item_name}")
                    output_lines.append(f"🎯 ใกล้เคียงที่สุด: {match} (score: {score})\n")
                else:
                    output_lines.append(f"📦 จากใบเสร็จ: {item_name}")
                    output_lines.append("❌ ไม่พบ match ที่เหมาะสม\n")

        output_path = os.path.join(output_folder, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(receipt, f, ensure_ascii=False, indent=4)

        print('\n'.join(output_lines))
        print(f"✅ Cleaned data saved to: {output_path}")

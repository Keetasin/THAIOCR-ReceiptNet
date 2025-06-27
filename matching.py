import csv
import json
import os
from rapidfuzz import process, fuzz

# โหลดรายการสินค้าอ้างอิงจาก CSV
product_list = []
with open('dataset/product_list.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        product_list.append(row['product_name'])

# โฟลเดอร์ที่เก็บ JSON
json_folder = 'data/json_data'

# โฟลเดอร์สำหรับเก็บผลลัพธ์ที่ match
output_folder = 'data/matching'
os.makedirs(output_folder, exist_ok=True)

# วนลูปอ่านไฟล์ .json ทั้งหมด
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(json_folder, filename)

        with open(file_path, 'r', encoding='utf-8') as f:
            receipt = json.load(f)

        output_lines = [f"📂 ไฟล์: {filename}\n"]

        if 'items' in receipt:
            for item in receipt['items']:
                item_name = item['name'].replace("|", "").strip()

                # หา match ที่ใกล้เคียงที่สุด
                match, score, _ = process.extractOne(
                    item_name,
                    product_list,
                    scorer=fuzz.token_sort_ratio
                )

                output_lines.append(f"📦 จากใบเสร็จ: {item_name}")
                output_lines.append(f"🎯 ใกล้เคียงที่สุด: {match} (score: {score})\n")
        else:
            output_lines.append("⚠️ ไม่พบข้อมูล items ในไฟล์นี้\n")

        # เขียนผลลัพธ์ลงไฟล์ .txt
        output_txt_filename = os.path.splitext(filename)[0] + '.txt'
        output_txt_path = os.path.join(output_folder, output_txt_filename)

        with open(output_txt_path, 'w', encoding='utf-8') as out_file:
            out_file.write('\n'.join(output_lines))

        print(f"✅ บันทึกผลลัพธ์ไว้ที่: {output_txt_path}")

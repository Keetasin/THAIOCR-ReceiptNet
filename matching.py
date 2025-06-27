from rapidfuzz import fuzz, process
import json

# ตัวอย่างรายการสินค้าอ้างอิง (คุณอาจดึงจากฐานข้อมูลหรือไฟล์ CSV ก็ได้)
product_list = [
    "Hนมพาสฯเมจิกาแฟ",
    "แซนวิชเดนิชผักโขมแ"
]

# โหลด JSON ที่มี items
with open('json_data/output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# เปรียบเทียบแต่ละ item กับรายการสินค้าใน product_list
for item in data['items']:
    item_name = item['name'].replace("|", "").strip()

    # ใช้ process.extractOne เพื่อหาสินค้าที่ใกล้เคียงที่สุด
    match, score, _ = process.extractOne(item_name, product_list, scorer=fuzz.token_sort_ratio)

    print(f"ชื่อในใบเสร็จ: {item_name}")
    print(f"ใกล้เคียงที่สุด: {match} (score: {score})\n")

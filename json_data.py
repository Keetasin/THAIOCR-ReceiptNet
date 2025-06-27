import os
import re
import json

def parse_receipt_text(text):
    data = {}

    # ร้านค้า
    store_match = re.search(r'CP ALL, 7-Eleven Booth (.+)', text)
    if store_match:
        data['store'] = store_match.group(0).strip()

    # TAX number
    tax_match = re.search(r'TAX#(\d+)', text)
    if tax_match:
        data['tax_number'] = tax_match.group(1)

    # VAT Code
    vat_match = re.search(r'Vat Code (\d+)', text)
    if vat_match:
        data['vat_code'] = vat_match.group(1)

    # POS number
    pos_match = re.search(r'POS#(\w+)', text)
    if pos_match:
        data['pos_number'] = pos_match.group(1)

    # รายการสินค้าและราคา
    items = []
    item_pattern = re.compile(r'(\d+)\s+([^\d\n]+)\s+([\d]+\.\d{2})')
    for match in item_pattern.finditer(text):
        item = {
            "quantity": int(match.group(1)),
            "name": match.group(2).strip(),
            "price": float(match.group(3))
        }
        items.append(item)
    data['items'] = items[:-2]

    # ยอดสุทธิ
    total_match = re.search(r'ยอดสุทธิ.*?([\d]+\.\d{2})', text)
    if total_match:
        data['total'] = float(total_match.group(1))

    # ช่องทางจ่ายเงิน
    payment_match = re.search(r'ทรูวอลเล็ท 7 App ([\d]+\.\d{2})', text)
    if payment_match:
        data['payment'] = {
            "method": "ทรูวอลเล็ท 7 App",
            "amount": float(payment_match.group(1))
        }

    # TID
    tid_match = re.search(r'TID#(\d+)', text)
    if tid_match:
        data['tid'] = tid_match.group(1)

    # หมายเลขใบเสร็จ และวันที่เวลา
    receipt_match = re.search(r'R#(\S+)\s*:(\d+)\s*(\d{2}/\d{2}/\d{2})\s*(\d{2}:\d{2})', text)
    if receipt_match:
        data['receipt_number'] = receipt_match.group(1)
        data['receipt_code'] = receipt_match.group(2)
        data['date'] = receipt_match.group(3)
        data['time'] = receipt_match.group(4)

    # สมาชิก
    member_match = re.search(r'ข้อมูลสมาชิก (.+)', text)
    if member_match:
        data['member_name'] = member_match.group(1).strip()

    # คะแนนสมาชิก
    points_match = re.search(r'All Member Point\s*\| \+(\d+) \| (\d+) \| (\d+)', text)
    if points_match:
        data['member_points'] = {
            "earned": int(points_match.group(1)),
            "used": int(points_match.group(2)),
            "balance": int(points_match.group(3))
        }

    return data

# โฟลเดอร์ต้นทางและปลายทาง
input_folder = 'data/result'
output_folder = 'data/json_data'

# สร้างโฟลเดอร์ผลลัพธ์ถ้ายังไม่มี
os.makedirs(output_folder, exist_ok=True)

# วนลูปอ่านไฟล์ .txt ทั้งหมดในโฟลเดอร์ result
for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        input_path = os.path.join(input_folder, filename)
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # แปลงข้อมูล
        data = parse_receipt_text(text)

        # ตั้งชื่อไฟล์ JSON ตามชื่อไฟล์ .txt
        json_filename = os.path.splitext(filename)[0] + '.json'
        output_path = os.path.join(output_folder, json_filename)

        # บันทึกไฟล์ JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Processed {filename} -> {json_filename}")

print("All files processed.")

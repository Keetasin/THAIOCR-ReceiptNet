import json
import os
import csv
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams

# โฟลเดอร์ cleaned_data
input_folder = 'data/cleaned_data'

# ตัวแปรเก็บสถิติ
product_sales = defaultdict(lambda: {'count': 0, 'total_sales': 0.0})

# อ่านไฟล์ .json ทั้งหมด
for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as f:
            receipt = json.load(f)

        if 'items' in receipt:
            for item in receipt['items']:
                name = item['name']
                price = float(item['price']) * int(item['quantity'])
                product_sales[name]['count'] += int(item['quantity'])
                product_sales[name]['total_sales'] += price

# วิเคราะห์ยอดขาย
products = []
quantities = []
total_sales = []

print("สรุปยอดขายสินค้าทั้งหมด")
for product, stats in sorted(product_sales.items(), key=lambda x: x[1]['total_sales'], reverse=True):
    print(f"{product}: จำนวน {stats['count']} ชิ้น, ยอดขายรวม {stats['total_sales']:.2f}")
    products.append(product)
    quantities.append(stats['count'])
    total_sales.append(stats['total_sales'])

# บันทึกเป็น CSV
output_file = 'data/product_sales_summary.csv'
with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Product Name', 'Quantity Sold', 'Total Sales'])
    for p, q, s in zip(products, quantities, total_sales):
        writer.writerow([p, q, f"{s:.2f}"])

print(f"\nบันทึกไฟล์ CSV เรียบร้อย: {output_file}")


# โหลดฟอนต์ TH Sarabun New จากไฟล์ .ttf
font_path = 'THSarabunNew.ttf'  # เปลี่ยนเป็นที่อยู่ไฟล์จริง
font_prop = font_manager.FontProperties(fname=font_path)

# ตั้งค่าให้ matplotlib ใช้ฟอนต์นี้
rcParams['font.family'] = font_prop.get_name()
rcParams['axes.unicode_minus'] = False  # แก้ปัญหาเครื่องหมายลบไม่แสดง

# ตัดข้อมูล 10 อันดับแรกสำหรับกราฟ
top_n = 10
top_products = products[:top_n]
top_total_sales = total_sales[:top_n]

# Plot กราฟแค่ 10 อันดับแรก
plt.figure(figsize=(10,6))
plt.bar(top_products, top_total_sales)
plt.xticks(rotation=45, ha='right', fontproperties=font_prop)
plt.xlabel('สินค้า', fontproperties=font_prop)
plt.ylabel('ยอดขายรวม', fontproperties=font_prop)
plt.title('ยอดขายรวม 10 อันดับแรก', fontproperties=font_prop)
plt.tight_layout()
plt.savefig('data/product_sales_top10_chart.png')
plt.show()


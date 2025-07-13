from flask import Flask, render_template, request, url_for
import os
from typhoon_ocr import ocr_document
import csv
from rapidfuzz import process, fuzz
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  
from matplotlib import font_manager, rcParams
from collections import defaultdict
from models import Session, SaleItem


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
SUMMARY_FOLDER = 'static/summary'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SUMMARY_FOLDER, exist_ok=True)

# โหลดรายการสินค้า
product_list = []
with open('static/product_list.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        product_list.append(row['product_name'])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')):
            ext = os.path.splitext(file.filename)[1]
            filepath = os.path.join(UPLOAD_FOLDER, 'uploaded_file' + ext)
            file.save(filepath)

            try:
                result_text = ocr_document(pdf_or_image_path=filepath, task_type="default", page_num=1)
                data = parse_receipt_text(result_text)
            except Exception as e:
                return f"เกิดข้อผิดพลาดในการเรียกใช้ OCR: {str(e)}"


            if 'items' in data:
                for item in data['items']:
                    item_name = item['name'].replace("|", "").strip()
                    match_tuple = process.extractOne(item_name, product_list, scorer=fuzz.token_sort_ratio)
                    if match_tuple and match_tuple[1] >= 35:
                        item['name'] = match_tuple[0]

            product_sales = defaultdict(lambda: {'count': 0, 'total_sales': 0.0})
            for item in data['items']:
                name = item['name']
                price = float(item['price']) * int(item['quantity'])
                product_sales[name]['count'] += int(item['quantity'])
                product_sales[name]['total_sales'] += price

            font_path = 'static/THSarabunNew.ttf'
            font_prop = font_manager.FontProperties(fname=font_path)
            rcParams['font.family'] = font_prop.get_name()
            rcParams['axes.unicode_minus'] = False

            products = list(product_sales.keys())
            totals = [v['total_sales'] for v in product_sales.values()]

            plt.figure(figsize=(10,6))
            plt.bar(products, totals)
            plt.xticks(rotation=45, ha='right', fontproperties=font_prop)
            plt.xlabel('สินค้า', fontproperties=font_prop)
            plt.ylabel('ยอดขายรวม (บาท)', fontproperties=font_prop)
            plt.title('ยอดขายรวม', fontproperties=font_prop)
            plt.tight_layout()
            chart_path = os.path.join(SUMMARY_FOLDER, 'chart.png')
            plt.savefig(chart_path)
            plt.close()

            summary_list = []
            for name, v in product_sales.items():
                summary_list.append({
                    'name': name,
                    'quantity': v['count'],
                    'total_sales': f"{v['total_sales']:.2f}"
                })

            return render_template('result.html', chart_url=url_for('static', filename='summary/chart.png'), summary=summary_list)

    return render_template('upload.html')

def parse_receipt_text(text):
    import re
    data = {}
    store_match = re.search(r'CP ALL, 7-Eleven Booth (.+)', text)
    if store_match:
        data['store'] = store_match.group(0).strip()
    tax_match = re.search(r'TAX#(\d+)', text)
    if tax_match:
        data['tax_number'] = tax_match.group(1)
    vat_match = re.search(r'Vat Code (\d+)', text)
    if vat_match:
        data['vat_code'] = vat_match.group(1)
    pos_match = re.search(r'POS#(\w+)', text)
    if pos_match:
        data['pos_number'] = pos_match.group(1)
    total_match = re.search(r'ยอดสุทธิ(?:.|\n)*?([\d]+\.\d{2})', text)
    if total_match:
        data['total'] = float(total_match.group(1))
    else:
        data['total'] = 0

    items = []
    item_pattern = re.compile(r'(\d+)\s+([^\n]+)\s+([\d]+\.\d{2})')
    count = sum(1 for _ in item_pattern.finditer(text))
    for match in item_pattern.finditer(text):
        item = {
            "quantity": int(match.group(1)),
            "name": match.group(2).strip(),
            "price": float(match.group(3))
        }
        if count <= 3:
            items.append(item)
            break
        elif (count > 3) and (item['price'] != data['total']):
            items.append(item)
    data['items'] = items
    return data


from flask import Flask, render_template, request, url_for, redirect  # เพิ่ม redirect

@app.route('/save-edits', methods=['POST'])
def save_edits():
    try:
        num_items = int(request.form['num_items'])

        # เปิด Session ใหม่
        db_session = Session()
        # db_session.query(SaleItem).delete()

        for i in range(num_items):
            name = request.form[f'name_{i}']
            quantity = int(request.form[f'quantity_{i}'])
            total_sales = float(request.form[f'total_sales_{i}'])

            # บันทึกลงฐานข้อมูล
            item = SaleItem(name=name, quantity=quantity, total_sales=total_sales)
            db_session.add(item)

        db_session.commit()
        db_session.close()

        # ✅ ไปยังหน้าใหม่หลังบันทึก
        return redirect(url_for('saved_page'))

    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"

@app.route('/saved')
def saved_page():
    return render_template('saved.html')

@app.route('/history')
def show_history():
    from models import Session, SaleItem
    session = Session()
    items = session.query(SaleItem).all()
    session.close()

    return render_template('history.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)

# THAIOCR-ReceiptNet

โปรเจกต์นี้ใช้ Typhoon OCR สำหรับอ่านข้อความจากไฟล์ PDF หรือรูปภาพ

---

## ขั้นตอนการติดตั้งและรันโปรเจกต์

### 0. Clone โปรเจกต์ และเข้าโฟลเดอร์โปรเจกต์
```bash
git clone <repository_url>
cd THAIOCR-ReceiptNet
```

### 1. สร้าง Virtual Environment (venv)
```bash
python -m venv venv
```

### 2. เปิดใช้งาน Virtual Environment
- window
```bash
venv\Scripts\activate
```

### 3. ติดตั้ง dependencies จาก requirements.txt
```bash
pip install -r requirements.txt
```

### 4. ตั้งค่า API Key สำหรับ Typhoon OCR 
- ใส่ API Key ของคุณใน api_key.ps1
- รันคำสั่งนี้เพื่อโหลด API Key
```bash
.\api_key.ps1
```

### 5. รันโปรแกรม OCR
```bash
python main.py
```

### 6. เก็บข้อมูลที่สนใจใน json
```bash
python json_data.py
```

### 7. matching items กับข้อมูลสิ้นค้าที่มี
```bash
python Clean-ReceiptData.py
```

### 8. สรุป วาดกราฟ วิเคราะห์ข้อมูล
```bash
python analysis.py
```

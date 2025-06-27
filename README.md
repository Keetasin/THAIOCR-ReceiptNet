# THAIOCR-ReceiptNet
โปรเจกต์นี้ใช้ Typhoon OCR สำหรับอ่านข้อความจากไฟล์ PDF หรือรูปภาพ

## ขั้นตอนการติดตั้งและรันโปรเจกต์

### 1. สร้าง Virtual Environment (venv)
```bash
python -m venv venv
```

### 2. เปิดใช้งาน Virtual 
- window
```bash
venv\Scripts\activate
```

### 3. ติดตั้ง dependencies จาก requirements.txt
```bash
pip install -r requirements.txt
```

## 4. ตั้งค่า API Key สำหรับ Typhoon OCR 
- ใส่ API Key ของคุณใน api_key.ps1
- รันคำสั่งนี้เพื่อโหลด API Key
```bash
.\api_key.ps1
```

5. รันโปรแกรม OCR
```bash
python main.py
```


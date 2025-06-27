from typhoon_ocr import ocr_document
import os

# สร้างโฟลเดอร์ 'result' ถ้ายังไม่มี
os.makedirs("result", exist_ok=True)

# OCR จาก PDF
result_markdown = ocr_document(
    pdf_or_image_path="dataset/seven-eleven/01541_2_1_20250426_600096_4000.pdf", 
    task_type="default",   # หรือ "structure"
    page_num=1
)

# กำหนดชื่อไฟล์สำหรับบันทึกผลลัพธ์
output_path = "result/output.txt"

# เขียนผลลัพธ์ลงไฟล์
with open(output_path, "w", encoding="utf-8") as f:
    f.write(result_markdown)

print(f"OCR result saved to: {output_path}")

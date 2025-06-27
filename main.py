from typhoon_ocr import ocr_document
import os

# เส้นทางโฟลเดอร์
input_folder = "dataset/seven-eleven"
output_folder = "data/result"

# สร้างโฟลเดอร์สำหรับเก็บผลลัพธ์ ถ้ายังไม่มี
os.makedirs(output_folder, exist_ok=True)

# วนลูปทุกไฟล์ในโฟลเดอร์ input
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
        input_path = os.path.join(input_folder, filename)
        print(f"🔍 OCR กำลังประมวลผล: {filename}")

        try:
            # เรียก Typhoon OCR
            result_markdown = ocr_document(
                pdf_or_image_path=input_path,
                task_type="default",
                page_num=1
            )

            # สร้างชื่อไฟล์ผลลัพธ์ เช่น 01541_2_1_20250426.txt
            output_filename = os.path.splitext(filename)[0] + ".txt"
            output_path = os.path.join(output_folder, output_filename)

            # บันทึกไฟล์ผลลัพธ์
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result_markdown)

            print(f"✅ OCR result saved to: {output_path}\n")

        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดกับไฟล์ {filename}: {e}\n")

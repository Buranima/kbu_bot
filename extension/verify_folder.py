import os
import json

# อ่านข้อมูลจากไฟล์ JSON
def load_folder_structure(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

# ฟังก์ชันสำหรับสร้างเฉพาะโฟลเดอร์
def create_folders(base_path, structure):
    for key, value in structure.items():
        folder_path = os.path.join(base_path, key)
        if isinstance(value, dict):
            # สร้างโฟลเดอร์ถ้าเป็น dict (มีโฟลเดอร์ย่อย)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created folder: {folder_path}")
            create_folders(folder_path, value)  # เรียกใช้ฟังก์ชันอีกครั้งในโฟลเดอร์ย่อย
        else:
            # สร้างโฟลเดอร์หลัก
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created folder: {folder_path}")

# ระบุ path ของโฟลเดอร์ extension (ปัจจุบัน)
base_directory = os.getcwd()  # โฟลเดอร์ extension คือโฟลเดอร์ปัจจุบัน

# โหลดโครงสร้างโฟลเดอร์จากไฟล์ JSON
json_file = 'static/config/folder_config.json'  # ระบุชื่อไฟล์ JSON ที่ต้องการใช้
folder_structure = load_folder_structure(json_file)

# สร้างโฟลเดอร์ตามโครงสร้างที่อ่านได้จาก JSON
create_folders(base_directory, folder_structure)
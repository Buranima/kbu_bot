import json
import subprocess
import sys

# อ่านไฟล์ JSON
with open('static/config/install_config.json', 'r') as file:
    data = json.load(file)

# ตรวจสอบว่าใน JSON มีคีย์ "extension_install" หรือไม่
if "extension_install" in data:
    packages = data["extension_install"]
    
    # ติดตั้งไลบรารีทั้งหมดที่ระบุในรายการ
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package])
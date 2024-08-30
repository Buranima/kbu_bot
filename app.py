from flask import Flask, render_template
import mysql.connector
import json

# เชื่อมต่อกับฐานข้อมูล
conn = mysql.connector.connect(
    host="localhost",  # หรือ IP ของเซิร์ฟเวอร์
    user="root",
    password="1234",
    database="kbu_bot",
    charset='utf8mb4',
    collation='utf8mb4_unicode_ci'
)

cursor = conn.cursor()

# ดึงข้อมูลจากฐานข้อมูล
cursor.execute("SELECT name_sound FROM sound")
rows = cursor.fetchall()

# สร้างรายการในรูปแบบที่ต้องการ
sound_list = [row[0] for row in rows]

# สร้างโครงสร้าง JSON
json_data = {
    "sound_list": sound_list
}

# ระบุเส้นทางที่ต้องการบันทึกไฟล์
file_path = 'static/json/sound_list.json'

# บันทึกเป็นไฟล์ JSON ในตำแหน่งที่กำหนด
with open(file_path, 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

# ปิดการเชื่อมต่อกับฐานข้อมูล
cursor.close()
conn.close()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
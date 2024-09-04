from flask import Flask, render_template
import mysql.connector
import json
import os

# โหลดข้อมูลจากไฟล์ JSON
with open('static/config/database_config.json', 'r') as file:
    config = json.load(file)

# เชื่อมต่อกับฐานข้อมูล
conn = mysql.connector.connect(
    host=config["host"][0],
    user=config["user"][0],
    password=config["password"][0],
    database=config["database"][0],
    charset=config["charset"][0],
    collation=config["collation"][0]
)

cursor = conn.cursor()

# ระบุเส้นทางของโฟลเดอร์ที่ต้องการอ่าน
folder_path = 'static/sound'

# อ่านรายการไฟล์ในโฟลเดอร์
file_list = os.listdir(folder_path)

# สร้างโครงสร้างข้อมูล JSON
sound_list = {"sound_list": [f"static/sound/{file_name}" for file_name in file_list]}

# ระบุเส้นทางที่ต้องการบันทึกไฟล์
json_file_path = 'static/temp/sound_list.json'

# บันทึกข้อมูลเป็นไฟล์ JSON
with open(json_file_path, 'w') as json_file:
    json.dump(sound_list, json_file, indent=4)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
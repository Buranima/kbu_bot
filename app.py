from flask import Flask, render_template
import mysql.connector
import json
import os

folders = ['static/sound', 'static/base/sound']

allowed_extensions = {'.mp3'}

file_list = []

for folder in folders:
    for file_name in os.listdir(folder):
        _, extension = os.path.splitext(file_name)
        if extension.lower() in allowed_extensions:
            file_list.append(f"{folder}/{file_name}")

sound_list = {"sound_list": file_list}

json_file_path = 'static/temp/sound_list.json'

with open(json_file_path, 'w') as json_file:
    json.dump(sound_list, json_file, indent=4)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
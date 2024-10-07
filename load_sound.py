import json
import os

def loadSound():
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

    if os.path.exists(json_file_path):
        os.remove(json_file_path)

    with open(json_file_path, 'w') as json_file:
        json.dump(sound_list, json_file, indent=4)

if __name__ == "__main__":
    loadSound()
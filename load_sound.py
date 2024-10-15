import json
import os

def loadSound():
    folders = ["static/config/sound", "static/base/sound"]

    allowed_extensions = {".mp3"}

    file_list = []

    for folder in folders:
        for file_name in os.listdir(folder):
            _, extension = os.path.splitext(file_name)
            if extension.lower() in allowed_extensions:
                file_list.append(f"{folder}/{file_name}?v=")

    sound_list = {"sound": file_list}

    json_file_path = "static/temp/sound_list.json"

    # if os.path.exists(json_file_path):
    #     os.remove(json_file_path)

    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(sound_list, json_file, indent=4)
    
    return sound_list

if __name__ == "__main__":
    list_sound = loadSound()
    print(list_sound)
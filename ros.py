import json
import os

config_ros = None
config_ros_full = None

config_ros_file_path = "static/config/json/ros_config.json"
config_ros_temp_file_path = "static/temp/ros_config_temp.json"

def f_write_config():
    global config_ros_file_path, config_ros, config_ros_temp_file_path, config_ros_full
    with open(config_ros_file_path, "r", encoding="utf-8") as file_config_ros:
        config_ros = json.load(file_config_ros)
    config_ros_full = {
        "id-route":config_ros["id-route"],
        "name-route":config_ros["name-route"],
        "route":config_ros["route"],
        "status-route":["ใช้งาน", "ใช้งาน"],
        "status": "stop",
        "control": "stop",
        "command": "dance",
        "battery": 0,
        "microphone": False
    }
    with open(config_ros_temp_file_path, "w", encoding="utf-8") as file_config_ros:
        json.dump(config_ros_full, file_config_ros, ensure_ascii=False, indent=4)

def f_check_config_ros():
    global config_ros_temp_file_path
    if os.path.exists(config_ros_temp_file_path):
        pass
    else:
        f_write_config()

def f_load_config():
    global config_ros_temp_file_path, config_ros_full
    f_check_config_ros()
    with open(config_ros_temp_file_path, "r", encoding="utf-8") as file_config_ros:
        config_ros_full = json.load(file_config_ros)

def f_read_config():
    f_load_config()
    return config_ros_full

def f_update_config(key, data):
    global config_ros_temp_file_path, config_ros_full
    f_load_config()
    config_ros_full[key] = data
    with open(config_ros_temp_file_path, "w", encoding="utf-8") as file_config_ros:
        json.dump(config_ros_full, file_config_ros, ensure_ascii=False, indent=4)

def f_update_config_arry(key, index, data):
    global config_ros_temp_file_path, config_ros_full
    f_load_config()
    config_ros_full[key][index] = data
    with open(config_ros_temp_file_path, "w", encoding="utf-8") as file_config_ros:
        json.dump(config_ros_full, file_config_ros, ensure_ascii=False, indent=4)

def f_default():
    global config_ros_temp_file_path, config_ros_full
    f_load_config()
    for index in range(len(config_ros_full["status-route"])):
        config_ros_full["status-route"][index] = "ใช้งาน"
    config_ros_full["status"] = "start"
    config_ros_full["control"] = "stop"
    config_ros_full["microphone"] = False
    with open(config_ros_temp_file_path, "w", encoding="utf-8") as file_config_ros:
        json.dump(config_ros_full, file_config_ros, ensure_ascii=False, indent=4)

def f_route(id):
    global config_ros_temp_file_path, config_ros_full
    f_load_config()
    for index in range(len(config_ros_full["status-route"])):
        config_ros_full["status-route"][index] = "ใช้งาน"
    config_ros_full["status-route"][id-1] = "กำลังใช้งาน"
    with open(config_ros_temp_file_path, "w", encoding="utf-8") as file_config_ros:
        json.dump(config_ros_full, file_config_ros, ensure_ascii=False, indent=4)
    return config_ros_full["route"][id-1]

if __name__ == "__main__":
    f_write_config()
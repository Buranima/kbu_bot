import json

config_ros = None

config_ros_file_path = "static/config/json/ros_config.json"

def f_load_config():
    global config_ros_file_path, config_ros
    with open(config_ros_file_path, "r", encoding="utf-8") as file_config_ros:
        config_ros = json.load(file_config_ros)

def f_read_config():
    f_load_config()
    return config_ros

def f_update_config(key, data):
    global config_ros_file_path, config_ros
    f_load_config()
    config_ros[key] = data
    with open(config_ros_file_path, "w", encoding="utf-8") as file_config_ros:
        json.dump(config_ros, file_config_ros, ensure_ascii=False, indent=4)

def f_update_config_arry(key, index, data):
    global config_ros_file_path, config_ros
    f_load_config()
    config_ros[key][index] = data
    with open(config_ros_file_path, "w", encoding="utf-8") as file_config_ros:
        json.dump(config_ros, file_config_ros, ensure_ascii=False, indent=4)

def f_default():
    global config_ros_file_path, config_ros
    f_load_config()
    for index in range(len(config_ros["status-route"])):
        config_ros["status-route"][index] = "ใช้งาน"
    config_ros["status"] = "start"
    config_ros["control"] = "stop"
    config_ros["microphone"] = False
    with open(config_ros_file_path, "w", encoding="utf-8") as file_config_ros:
        json.dump(config_ros, file_config_ros, ensure_ascii=False, indent=4)

def f_route(id):
    global config_ros_file_path, config_ros
    f_load_config()
    for index in range(len(config_ros["status-route"])):
        config_ros["status-route"][index] = "ใช้งาน"
    config_ros["status-route"][id-1] = "กำลังใช้งาน"
    with open(config_ros_file_path, "w", encoding="utf-8") as file_config_ros:
        json.dump(config_ros, file_config_ros, ensure_ascii=False, indent=4)
    return config_ros["route"][id-1]

if __name__ == "__main__":
    f_route(2)
import json

config_ros = None

config_ros_file_path = "static/config/json/ros_config.json"

def f_load_config():
    global config_ros_file_path, config_ros
    with open(config_ros_file_path, "r", encoding="utf-8") as file_config_ros:
        config_ros = json.load(file_config_ros)


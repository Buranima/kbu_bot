import os
import json

def verifyFolder():
    def load_folder_structure(json_file):
        with open(json_file, "r") as f:
            return json.load(f)

    def create_folders(base_path, structure):
        for key, value in structure.items():
            folder_path = os.path.join(base_path, key)
            if isinstance(value, dict):
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    print(f"Created folder: {folder_path}")
                create_folders(folder_path, value)
            else:
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    print(f"Created folder: {folder_path}")

    base_directory = os.getcwd()

    json_file = "extension/config/folder_config.json"
    folder_structure = load_folder_structure(json_file)

    create_folders(base_directory, folder_structure)

if __name__ == "__main__":
    verifyFolder()
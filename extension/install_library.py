import json
import subprocess
import sys

def installLibrary():
    with open('static/config/install_config.json', 'r') as file:
        data = json.load(file)

    if "extension_install" in data:
        packages = data["extension_install"]

        for package in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    installLibrary()
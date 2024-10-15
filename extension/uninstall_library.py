import json
import subprocess
import sys

def uninstallLibrary():
    with open("extension/config/install_config.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    if "extension_install" in data:
        packages = data["extension_install"]

        for package in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package])

if __name__ == "__main__":
    uninstallLibrary()
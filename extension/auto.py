from install_library import installLibrary
from verify_folder import verifyFolder
from uninstall_library import uninstallLibrary

def autoHelp():
    uninstallLibrary()
    installLibrary()
    verifyFolder()
    print("\nติดตั้งไลบราลีและสร้างโฟลเดอร์สำเร็จ")

if __name__ == "__main__":
    autoHelp()
import sounddevice as sd
import numpy as np

def check_microphone():
    duration = 1
    try:
        # print("เริ่มการบันทึก...")
        recording = sd.rec(int(duration * 44100), samplerate=44100, channels=2, dtype='float64')
        sd.wait()
        if np.any(recording): 
            # print("ไมโครโฟนทำงานได้")
            return True
        else:
            # print("ไม่มีข้อมูลเสียง ไมโครโฟนอาจไม่ทำงาน")
            return False
    except Exception as e:
        # print(f"เกิดข้อผิดพลาด: {e}")
        return False

if __name__ == "__main__":
    check_microphone()
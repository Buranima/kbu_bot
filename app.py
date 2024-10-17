from flask import Flask, render_template
from flask_socketio import SocketIO
import pyautogui
import json
import webbrowser
import time
import subprocess
import threading

from load_sound import loadSound
from text_to_speech import textToSpeech
from database import requestDataFormDataQuestionAnswer, updateDataFormDataQuestionAnswer, insertDataToQuestionAnswer, deleteDataFromQuestionAnswer
from analyze_questions import findAnswer
from search_by_typhoon import chatByTyphoon, setLatestQuestionsByTyphoon
from microphone import check_microphone

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/test")
def f_test():
    return render_template("test.html")

@app.route("/db")
def managementDB():
    return render_template("management_db.html")

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")
    time.sleep(1)
    pyautogui.press("f11")

def startROS():
    commandROS = "ros2 launch test_pkg laser.launch.py"
    processROS = subprocess.Popen(commandROS, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = processROS.communicate()
    # print("Output:\n", stdout.decode())
    # print("Error:\n", stderr.decode())

@socketio.on("KBUBOT")
def f_KBU_mode(message):
    message_json = json.dumps(message, ensure_ascii=False)
    message_dictionary = json.loads(message_json)
    print(f"กำลังทำงาน... {message_dictionary['mode']}\n")
    result = {
        "mode": message_dictionary["mode"],
        "result": None
    }
    
    if str(message_dictionary["mode"]) == "TTS-WAKE-WORD":
        result["result"] = textToSpeech(message_dictionary["speech"])
    
    elif str(message_dictionary["mode"]) == "TTS-LISTEN-WORD":
        result["result"] = textToSpeech(message_dictionary["speech"])
    
    elif str(message_dictionary["mode"]) == "TTS-QUESTION":
        result_answer = findAnswer(message_dictionary["speech"])
        if str(result_answer) == "หนูไม่เข้าใจคำถามนี้":
            result["result"] = textToSpeech(result_answer + "ค่ะ")
        elif str(result_answer) == "หนูยังไม่มั่นใจในคำตอบของคำถามนี้":
            result["result"] = textToSpeech(result_answer + "ค่ะ กรุณาระบุรายละเอียดของคำถามให้ชัดเจนมากขึ้น เพื่อให้หนูสามารถตอบคำถามนี้ได้ค่ะ")
        else:
            result["result"] = textToSpeech(result_answer + "ค่ะ มีอะไรถามเพิ่มเติมอีกมั้ยคะ")
    
    elif str(message_dictionary["mode"]) == "LOAD-LIST-SOUND":
        result["result"] = loadSound()
    
    elif str(message_dictionary["mode"]) == "TTS-CHAT-BOT":
        result_answer = chatByTyphoon(message_dictionary["speech"])
        result["result"] = textToSpeech(result_answer + "ค่ะ")
    
    elif str(message_dictionary["mode"]) == "CLEAR-CHAT":
        setLatestQuestionsByTyphoon()
        result["result"] = "OK"
    
    elif str(message_dictionary["mode"]) == "CONSOLE-LOG":
        pyautogui.press("f12")
        result["result"] = "OK"
    
    elif str(message_dictionary["mode"]) == "DATABASE-READ":
        result["result"] = requestDataFormDataQuestionAnswer()
    
    elif str(message_dictionary["mode"]) == "DATABASE-UP-DATE":
        updateDataFormDataQuestionAnswer(message_dictionary)
        result["result"] = requestDataFormDataQuestionAnswer()
    
    elif str(message_dictionary["mode"]) == "DATABASE-INSERT":
        insertDataToQuestionAnswer(message_dictionary)
        result["result"] = requestDataFormDataQuestionAnswer()
    
    elif str(message_dictionary["mode"]) == "DATABASE-DELETE":
        deleteDataFromQuestionAnswer(message_dictionary)
        result["result"] = requestDataFormDataQuestionAnswer()

    elif str(message_dictionary["mode"]) == "STATUS":
        result["result"] = message_dictionary["status"]
        socketio.emit("SERVER-ROS", result)
        # socketio.emit("SERVER-CONTROI-PANEL", result)
        return
    
    elif str(message_dictionary["mode"]) == "COMMAND":
        result["result"] = message_dictionary["command"]
        socketio.emit("SERVER-ROS", result)
        # socketio.emit("SERVER-CONTROI-PANEL", result)
        return

    socketio.emit("KBUBOT", result)

@socketio.on("DATA-BASE")
def f_control_panel_mode(message):
    message_json = json.dumps(message, ensure_ascii=False)
    message_dictionary = json.loads(message_json)
    print(f"กำลังทำงาน... {message_dictionary['mode']}\n")
    result = {
        "mode": message_dictionary["mode"],
        "result": None
    }

    if str(message_dictionary["mode"]) == "DATABASE-READ":
        result["result"] = requestDataFormDataQuestionAnswer()
    
    elif str(message_dictionary["mode"]) == "DATABASE-UP-DATE":
        updateDataFormDataQuestionAnswer(message_dictionary)
        result["result"] = requestDataFormDataQuestionAnswer()
    
    elif str(message_dictionary["mode"]) == "DATABASE-INSERT":
        insertDataToQuestionAnswer(message_dictionary)
        result["result"] = requestDataFormDataQuestionAnswer()
    
    elif str(message_dictionary["mode"]) == "DATABASE-DELETE":
        deleteDataFromQuestionAnswer(message_dictionary)
        result["result"] = requestDataFormDataQuestionAnswer()

    socketio.emit("DATA-BASE", result)

# @socketio.on("SERVER-ROS")
# def f_server_ros_mode(message):
#     # message_json = json.dumps(message, ensure_ascii=False)
#     # message_dictionary = json.loads(message_json)
#     message_dictionary = message
#     print(f"กำลังทำงาน... {message_dictionary['mode']}\n")
#     result = {
#         "mode": message_dictionary["mode"],
#         "result": None
#     }

#     if str(message_dictionary["mode"]) == "BATTERY":
#         result["result"] = message_dictionary["result"]

#     socketio.emit("SERVER-CONTROI-PANEL", result)

# @socketio.on("SERVER-CONTROI-PANEL")
# def f_server_controi_panel_mode(message):
#     message_json = json.dumps(message, ensure_ascii=False)
#     message_dictionary = json.loads(message_json)
#     print(f"กำลังทำงาน... {message_dictionary['mode']}\n")
#     result = {
#         "mode": message_dictionary["mode"],
#         "result": None
#     }

#     if str(message_dictionary["mode"]) == "ROUTE":
#         result["result"] = requestDataFormDataQuestionAnswer()
    
#     elif str(message_dictionary["mode"]) == "STATUS":
#         deleteDataFromQuestionAnswer(message_dictionary)
#         result["result"] = requestDataFormDataQuestionAnswer()

#     elif str(message_dictionary["mode"]) == "CONTROL":
#         deleteDataFromQuestionAnswer(message_dictionary)
#         result["result"] = requestDataFormDataQuestionAnswer()

#     elif str(message_dictionary["mode"]) == "COMMAND":
#         deleteDataFromQuestionAnswer(message_dictionary)
#         result["result"] = requestDataFormDataQuestionAnswer()

#     elif str(message_dictionary["mode"]) == "BATTERY":
#         deleteDataFromQuestionAnswer(message_dictionary)
#         result["result"] = requestDataFormDataQuestionAnswer()

if __name__ == "__main__":
    # threading.Timer(0, startROS).start()
    # threading.Timer(1.25, open_browser).start()
    socketio.run(app, debug=False, host="0.0.0.0")
from flask import Flask, render_template
from flask_socketio import SocketIO
import json

from load_sound import loadSound
from text_to_speech import textToSpeech
from database import requestDataFormDataQuestionAnswer, updateDataFormDataQuestionAnswer, insertDataToQuestionAnswer, deleteDataFromQuestionAnswer
from analyze_questions import findAnswer
from search_by_typhoon import chatByTyphoon, setLatestQuestionsByTyphoon

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/db")
def managementDB():
    return render_template("management_db.html")

@app.route("/control")
def controlKBUBot():
    return render_template("control.html")

@socketio.on("data-form-database")
def dataFormDataBase(data_form_database_text):
    print(f"ข้อมูลที่ได้รับจาก data-form-database คือ {data_form_database_text}")
    data_form_database_string_data = json.dumps(data_form_database_text, ensure_ascii=False)
    data_form_database_dictionary_data = json.loads(data_form_database_string_data)
    print(f'โหมดที่ต้องดำเนินการคือ {data_form_database_dictionary_data["mode"]} mode\n')
    if str(data_form_database_dictionary_data["mode"]) == "read":
        # print(requestDataFormDataQuestionAnswer())
        socketio.emit("data-form-database", requestDataFormDataQuestionAnswer())
        print("ส่งข้อมูลไปยังไคลเอนต์สำเร็จ")
    elif str(data_form_database_dictionary_data["mode"]) == "update":
        updateDataFormDataQuestionAnswer(data_form_database_dictionary_data)
        # print(requestDataFormDataQuestionAnswer())
        socketio.emit("data-form-database", requestDataFormDataQuestionAnswer())
        print("ส่งข้อมูลไปยังไคลเอนต์สำเร็จ")
    elif str(data_form_database_dictionary_data["mode"]) == "insert":
        # เพิ่มข้อมูลใหม่ลงในฐานข้อมูล
        insertDataToQuestionAnswer(data_form_database_dictionary_data)
        socketio.emit("data-form-database", requestDataFormDataQuestionAnswer())
        print("ส่งข้อมูลไปยังไคลเอนต์สำเร็จ")
    elif str(data_form_database_dictionary_data["mode"]) == "delete":
        deleteDataFromQuestionAnswer(data_form_database_dictionary_data["id"])
        socketio.emit("data-form-database", requestDataFormDataQuestionAnswer())
        print("ลบข้อมูลและจัดเรียง ID ใหม่สำเร็จ")

@socketio.on("data-form-sound")
def dataFormSound():
    pass

@socketio.on("data-form-config")
def dataFormConfig():
    pass

@socketio.on("tts-wake-word")
def ttsWakeWord(tts_wake_word_text):
    print(f"ข้อมูลที่ได้รับจาก tts-wake-word คือ {tts_wake_word_text}")
    tts_wake_word_json_string_data = json.dumps(tts_wake_word_text, ensure_ascii=False)
    tts_wake_word_json_dictionary_data = json.loads(tts_wake_word_json_string_data)
    print(tts_wake_word_json_dictionary_data["speech"])
    socketio.emit("play-tts-wake-word", textToSpeech(tts_wake_word_json_dictionary_data["speech"]))

@socketio.on("tts-listen-word")
def ttsListenWord(tts_listen_word_text):
    print(f"ข้อมูลที่ได้รับจาก tts-listen-word คือ {tts_listen_word_text}")
    tts_listen_word_json_string_data = json.dumps(tts_listen_word_text, ensure_ascii=False)
    tts_listen_word_json_dictionary_data = json.loads(tts_listen_word_json_string_data)
    print(tts_listen_word_json_dictionary_data["speech"])
    socketio.emit("play-tts-listen-word", textToSpeech(tts_listen_word_json_dictionary_data["speech"]))

@socketio.on("tts-question")
def ttsQuestion(tts_question):
    print(f"ข้อมูลที่ได้รับจาก tts-question คือ {tts_question}")
    tts_question_json_string_data = json.dumps(tts_question, ensure_ascii=False)
    tts_question_json_dictionary_data = json.loads(tts_question_json_string_data)
    print(tts_question_json_dictionary_data["speech"])
    tts_question_txt = findAnswer(tts_question_json_dictionary_data["speech"])
    if str(tts_question_txt) == "หนูไม่เข้าใจคำถามนี้":
        socketio.emit("tts-question", textToSpeech(tts_question_txt + "ค่ะ"))
    elif str(tts_question_txt) == "หนูยังไม่มั่นใจในคำตอบของคำถามนี้":
        socketio.emit("tts-question", textToSpeech(tts_question_txt + "ค่ะ กรุณาระบุรายละเอียดของคำถามให้ชัดเจนมากขึ้น เพื่อให้หนูสามารถตอบคำถามนี้ได้ค่ะ"))
    else:
        socketio.emit("tts-question", textToSpeech(tts_question_txt + "ค่ะ ต้องการสอบถามเพิ่มเติมมั้ยคะ"))

@socketio.on("tts-chat-bot")
def ttsChatBot(tts_chat_bot):
    print(f"ข้อมูลที่ได้รับจาก tts-chat-bot คือ {tts_chat_bot}")
    tts_chat_bot_json_string_data = json.dumps(tts_chat_bot, ensure_ascii=False)
    tts_chat_bot_json_dictionary_data = json.loads(tts_chat_bot_json_string_data)
    if str(tts_chat_bot_json_dictionary_data["mode"]) == "TTS":
        print(tts_chat_bot_json_dictionary_data["speech"])
        tts_chat_bot_txt = chatByTyphoon(tts_chat_bot_json_dictionary_data["speech"])
        socketio.emit("tts-chat-bot", textToSpeech(tts_chat_bot_txt + "ค่ะ"))
    else:
        setLatestQuestionsByTyphoon()

@socketio.on("load-list-sound")
def loadListSound(text_sound):
    print(f"ข้อมูลที่ได้รับจาก load-list-sound คือ {text_sound}")
    text_sound_string_data = json.dumps(text_sound, ensure_ascii=False)
    text_sound_dictionary_data = json.loads(text_sound_string_data)
    print(f'โหมดที่ต้องดำเนินการคือ {text_sound_dictionary_data["mode"]} mode\n')
    if str(text_sound_dictionary_data["mode"]) == "read":
        socketio.emit("load-list-sound", loadSound())

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")
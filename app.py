from flask import Flask, render_template
from flask_socketio import SocketIO
import json

from load_sound import loadSound
from text_to_speech import textToSpeech

loadSound()

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/management")
def management():
    return render_template("management.html")

@app.route("/management_db")
def managementDB():
    return render_template("management_db.html")

@app.route("/management_sound")
def managementSound():
    return render_template("management_sound.html")

@app.route("/management_config")
def managementConfig():
    return render_template("management_config.html")

@socketio.on("tts-wake-word")
def ttsWakeWord(tts_wake_word_text):
    print(f"ข้อมูลที่ได้รับจาก tts-wake-word คือ {tts_wake_word_text}")
    tts_wake_word_json_string_data = json.dumps(tts_wake_word_text, ensure_ascii=False)
    tts_wake_word_json_dictionary_data = json.loads(tts_wake_word_json_string_data)
    print(tts_wake_word_json_dictionary_data["speech"])
    textToSpeech(tts_wake_word_json_dictionary_data["speech"])
    socketio.emit("play-tts-wake-word", '{"directory":"static/temp/text_to_speech.mp3?v="}')

@socketio.on("tts-listen-word")
def ttsListenWord(tts_listen_word_text):
    print(f"ข้อมูลที่ได้รับจาก tts-listen-word คือ {tts_listen_word_text}")
    tts_listen_word_json_string_data = json.dumps(tts_listen_word_text, ensure_ascii=False)
    tts_listen_word_json_dictionary_data = json.loads(tts_listen_word_json_string_data)
    print(tts_listen_word_json_dictionary_data["speech"])
    textToSpeech(tts_listen_word_json_dictionary_data["speech"])
    socketio.emit("play-tts-listen-word", '{"directory":"static/temp/text_to_speech.mp3?v="}')

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")
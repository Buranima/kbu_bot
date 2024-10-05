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

@socketio.on("tts-command")
def ttsCommand(tts_command_text):
    print(f"ข้อมูลที่ได้รับจาก tts-command คือ {tts_command_text}")
    tts_command_json_string_data = json.dumps(tts_command_text, ensure_ascii=False)
    tts_command_json_dictionary_data = json.loads(tts_command_json_string_data)
    print(tts_command_json_dictionary_data["speech"])
    textToSpeech(tts_command_json_dictionary_data["speech"])
    socketio.emit("play-tts-command", '{"directory":"static/temp/text_to_speech.mp3"}')

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")
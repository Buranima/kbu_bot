from gtts import gTTS
import os

def textToSpeech(tts_text):
    text_to_speech_language = "th"
    text_to_speech_slow = False
    text_to_speech = gTTS(text=tts_text, lang=text_to_speech_language, slow=text_to_speech_slow)
    text_to_speech_output = os.path.join("static/temp", "text_to_speech.mp3")

    # if os.path.exists(text_to_speech_output):
    #     os.remove(text_to_speech_output)
    
    text_to_speech.save(text_to_speech_output)
    text_to_speech_output = None
    text_to_speech_output = "static/temp/text_to_speech.mp3?v="
    # text_to_speech_json = {"directory": text_to_speech_output}
    return text_to_speech_output
    # return text_to_speech_json

if __name__ == "__main__":
    print(textToSpeech("ทดสอบ ทดสอบ ทดสอบ 1234567890"))
    
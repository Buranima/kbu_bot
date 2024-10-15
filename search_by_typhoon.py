import requests
import os
import json

from database import requestDataFormDataQuestionAnswer

config_kbubot_file_path = "static/config/json/kbubot_config.json"
latest_questions_by_typhoon_file_path = "static/temp/latest_questions_by_typhoon.json"

latest_questions_by_typhoon = None

with open(config_kbubot_file_path, "r", encoding="utf-8") as file_config_kbubot:
    config_kbubot = json.load(file_config_kbubot)

data_database = None
content_system = ""

def loadData():
    global data_database, content_system
    data_database = json.loads(requestDataFormDataQuestionAnswer())
    content_system = f"จงใช้ข้อมูลต่อไปนี้ในการตอบคำถาม\n"
    for id_text in data_database["id"]:
        content_system = content_system + f"{id_text}. {data_database['question'][id_text-1]} คำตอบ {data_database['answer'][id_text-1]}\n"
    content_system = content_system + "หากสิ่งที่ถามไม่อยู่ในข้อมูลที่ให้ ให้ตอบว่าหนูไม่ทราบคำตอบของคำถามนี้"

endpoint = "https://api.opentyphoon.ai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {config_kbubot['apikey']}"
}

def setLatestQuestionsByTyphoon():
    set_latest_questions_by_typhoon = {"latest":[]}

    with open(latest_questions_by_typhoon_file_path, "w", encoding="utf-8") as json_file:
        json.dump(set_latest_questions_by_typhoon, json_file, ensure_ascii=False, indent=4)

if os.path.exists(latest_questions_by_typhoon_file_path):
    pass
else:
    setLatestQuestionsByTyphoon()


def findAnswerByTyphoon(text_questions_message):
    loadData()
    data_answer = {
        "model": "typhoon-v1.5-instruct",
        "max_tokens": 512,
        "messages": [
            {"role": "system", "content": f"คุณชื่อ{config_kbubot['wakeword'][0]} ถูกพัฒนาและสร้างขึ้นโดยคณะวิศวกรรมศาสตร์ คุณมีหน้าที่ตอบคำถามที่เกี่ยวข้องมหาวิทยาลัยเกษมบัณฑิต และคุณจะตอบเป็นภาษาไทยเท่านั้น"},
            {"role": "user", "content": content_system}
        ],
        "temperature": 0.4,
        "top_p": 0.9,
        "top_k": 0,
        "repetition_penalty": 1.05,
        "min_p": 0.05
    }

    with open(latest_questions_by_typhoon_file_path, "r", encoding="utf-8") as file_latest_questions_by_typhoon:
        latest_questions_by_typhoon = json.load(file_latest_questions_by_typhoon)

    new_message = {"role": "user", "content": f"{text_questions_message}"}

    if latest_questions_by_typhoon["latest"] != []:
        for latest_data in latest_questions_by_typhoon["latest"]:
            data_answer["messages"].append(latest_data)
        data_answer["messages"].append(new_message)
    else:
        data_answer["messages"].append(new_message)

    response = requests.post(endpoint, json=data_answer, headers=headers)

    if response.status_code == 200:
        result = response.json()
        answer_result = result["choices"][0]["message"]["content"]
        latest_questions_by_typhoon["latest"].append(new_message)
        new_message = {"role": "assistant", "content": f"{answer_result}"}
        latest_questions_by_typhoon["latest"].append(new_message)
        with open(latest_questions_by_typhoon_file_path, "w", encoding="utf-8") as json_file:
            json.dump(latest_questions_by_typhoon, json_file, ensure_ascii=False, indent=4)
    else:
        answer_result = "เกิดข้อผิดพลาดในการหาคำตอบของคุณ"
        print(f"Error: {response.status_code}, {response.text}")

    print(f"คำถาม คือ {text_questions_message}")
    print(f"คำตอบ คือ {answer_result}")

    return answer_result

def chatByTyphoon(text_questions_message_chat):
    data_chat = {
        "model": "typhoon-v1.5x-70b-instruct",
        "max_tokens": 256,
        "messages": [
            {"role": "system", "content": f"คุณชื่อ{config_kbubot['wakeword'][0]} ถูกพัฒนาและสร้างขึ้นโดยคณะวิศวกรรมศาสตร์ คุณจะตอบเป็นภาษาไทยเท่านั้น และคุณสามารถพูดคุยมีอารมณ์ความรู้สึกต่างๆเหมือนมนุษย์"}
        ],
        "temperature": 0.3,
        "top_p": 0.9,
        "top_k": 0,
        "repetition_penalty": 1.05,
        "min_p": 0
    }

    with open(latest_questions_by_typhoon_file_path, "r", encoding="utf-8") as file_latest_questions_by_typhoon:
        latest_questions_by_typhoon = json.load(file_latest_questions_by_typhoon)

    new_message = {"role": "user", "content": f"{text_questions_message_chat}"}

    if latest_questions_by_typhoon["latest"] != []:
        for latest_data in latest_questions_by_typhoon["latest"]:
            data_chat["messages"].append(latest_data)
        data_chat["messages"].append(new_message)
    else:
        data_chat["messages"].append(new_message)

    response = requests.post(endpoint, json=data_chat, headers=headers)

    if response.status_code == 200:
        result = response.json()
        answer_result = result["choices"][0]["message"]["content"]
        latest_questions_by_typhoon["latest"].append(new_message)
        new_message = {"role": "assistant", "content": f"{answer_result}"}
        latest_questions_by_typhoon["latest"].append(new_message)
        with open(latest_questions_by_typhoon_file_path, "w", encoding="utf-8") as json_file:
            json.dump(latest_questions_by_typhoon, json_file, ensure_ascii=False, indent=4)
    else:
        answer_result = "เกิดข้อผิดพลาดในการหาคำตอบของคุณ"
        print(f"Error: {response.status_code}, {response.text}")

    print(f"คำถาม คือ {text_questions_message_chat}")
    print(f"คำตอบ คือ {answer_result}")

    text_tts = answer_result
    
    new_text_tts = text_tts.replace("ครับ", "")
    new_text_tts = new_text_tts.replace("ค่ะ", "")
    new_text_tts = new_text_tts.replace("คะ", "")
    new_text_tts = new_text_tts.replace("!", "")
    new_text_tts = new_text_tts.replace(":", "")
    new_text_tts = new_text_tts.replace(",", "")
    new_text_tts = new_text_tts.replace("ผม", "หนู")
    new_text_tts = new_text_tts.replace("ฉัน", "หนู")
    new_text_tts = new_text_tts.replace("\n", " ")
    new_text_tts = new_text_tts.replace("\t", " ")
    
    return new_text_tts
    
if __name__ == "__main__":
    findAnswerByTyphoon("หัวหน้าสาขาคอมคือใคร")
    # chatByTyphoon("ขอสถานที่เที่ยวในน่าน")
    # setLatestQuestionsByTyphoon()
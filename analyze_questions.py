from pythainlp.tokenize import word_tokenize
import os
import json

from database import requestDataFormDataQuestionAnswer

latest_questions_file_path = "static/temp/latest_questions.json"
questions_tokenize_file_path = "static/temp/questions_tokenize.json"
result_questions_file_path = "static/temp/result_questions.json"
kbubot_config_file_path = "static/config/json/kbubot_config.json"
list_data_file_path = "static/temp/list_data.json"

text_tts = ""

list_data_json_answer = {
    "question":[],
    "answer": [],
    "result":[]
}

if os.path.exists(questions_tokenize_file_path):
    pass
else:
    requestDataFormDataQuestionAnswer()

def setLatestQuestions(set_latest_questions):
    global latest_questions_file_path
    set_latest_questions_data = {"latest": set_latest_questions}
    with open(latest_questions_file_path, "w", encoding="utf-8") as json_file:
        json.dump(set_latest_questions_data, json_file, ensure_ascii=False, indent=4)

if os.path.exists(latest_questions_file_path):
    pass
else:
    setLatestQuestions("")

def findOne(text_questions_find_one):
    global questions_tokenize_file_path, result_questions_file_path, latest_questions_file_path

    with open(kbubot_config_file_path, "r", encoding="utf-8") as json_kbubot_config_file:
                json_kbubot_config = json.load(json_kbubot_config_file)

    len_questions_score = 0.0
    like_questions_score = 0.0
    position_questions_score = 0.0
    sum_score = 0.0

    data_json = {
        "id":[],
        "result": []
    }

    with open(questions_tokenize_file_path, "r", encoding="utf-8") as file_questions_tokenize:
        questions_tokenize_json = json.load(file_questions_tokenize)
    list_text_questions = word_tokenize(text_questions_find_one, engine="deepcut")
    for id in range(len(questions_tokenize_json["id"])):
        list_json_questions = questions_tokenize_json["tokenize"][id]
        len_questions_score = (len(list_text_questions) / len(list_json_questions)) * json_kbubot_config["lenpass"]
        if len_questions_score > 10.0:
            len_questions_score = 10.0
        for data in range(len(list_json_questions)):
            for info in list_text_questions:
                if info == list_json_questions[data]:
                    like_questions_score = like_questions_score + 1.0
                    if list_text_questions.index(info) == list_json_questions.index(info):
                        position_questions_score = position_questions_score + 1.0
                    break
        like_questions_score = (like_questions_score / len(list_json_questions)) * json_kbubot_config["likepass"]
        position_questions_score = (position_questions_score / len(list_json_questions)) * json_kbubot_config["positionpass"]
        sum_score = len_questions_score + like_questions_score + position_questions_score

        # print(list_json_questions)
        # print(list_text_questions)
        # print(f"Len: {len_questions_score}/10")
        # print(f"Like: {like_questions_score}/45")
        # print(f"Position: {position_questions_score}/45")
        # print(f"Score: {sum_score}/100")

        data_json["id"].append(questions_tokenize_json["id"][id])
        data_json["result"].append(sum_score)
        len_questions_score = 0.0
        like_questions_score = 0.0
        position_questions_score = 0.0
        sum_score = 0.0
    with open(result_questions_file_path, "w") as json_file:
        json.dump(data_json, json_file, indent=4)

def resultAnswer(text_result_answer):
    global text_tts

    with open(questions_tokenize_file_path, "r", encoding="utf-8") as file_questions_tokenize:
        questions_tokenize_json = json.load(file_questions_tokenize)

    with open(result_questions_file_path, "r") as json_file:
        result_questions_json = json.load(json_file)

    with open(kbubot_config_file_path, "r", encoding="utf-8") as json_kbubot_config_file:
        json_kbubot_config = json.load(json_kbubot_config_file)
    
    max_result = max(result_questions_json["result"])
    max_index = result_questions_json["result"].index(max_result)
    max_id = result_questions_json['id'][max_index]
    if max_result == 100.0:
        # print(f"\nคำถามคือ {text_result_answer}")
        # print(f'คำตอบคือ {questions_tokenize_json["answer"][max_id-1]}')
        # print(f"ID ที่มี Result score มากที่สุดคือ ID: {max_id} ด้วยค่า Result score ที่: {max_result}")
        setLatestQuestions(questions_tokenize_json["question"][max_id-1])
        text_tts = questions_tokenize_json["answer"][max_id-1]
        return max_result
    elif max_result >= json_kbubot_config["passscore"]:
        # print(f"\nคำถามคือ {text_result_answer}")
        # print(f'คำตอบคือ {questions_tokenize_json["answer"][max_id-1]}')
        # print(f"ID ที่มี Result score มากที่สุดคือ ID: {max_id} ด้วยค่า Result score ที่: {max_result}")
        setLatestQuestions(questions_tokenize_json["question"][max_id-1])
        return max_result
    else:
        # print(f"\nคำถามคือ {text_result_answer}")
        # print(f'คำตอบที่ไกล้เคียงมากที่สุดคือ {questions_tokenize_json["answer"][max_id-1]}')
        # print(f"ID ที่มี Result score มากที่สุดคือ ID: {max_id} ด้วยค่า Result score ที่: {max_result}")
        setLatestQuestions("")
        return max_result

def findAnswer(text_questions):
    global questions_tokenize_file_path, result_questions_file_path, latest_questions_file_path, text_tts

    list_text_questions = word_tokenize(text_questions, engine="deepcut")

    result_score = 0.0

    with open(latest_questions_file_path, "r", encoding="utf-8") as file_questions_latest:
        questions_latest_json = json.load(file_questions_latest)

    with open(questions_tokenize_file_path, "r", encoding="utf-8") as file_questions_tokenize:
        questions_tokenize_json = json.load(file_questions_tokenize)

    with open(kbubot_config_file_path, "r", encoding="utf-8") as json_kbubot_config_file:
                json_kbubot_config = json.load(json_kbubot_config_file)

    if os.path.exists(result_questions_file_path):
        if questions_latest_json["latest"] == "":
            findOne(text_questions)
            result_score = resultAnswer(text_questions)
            if result_score == json_kbubot_config["resultpass"]:
                return text_tts
            elif result_score >= json_kbubot_config["passscore"]:
                setLatestQuestions("")
                text_tts = "หนูไม่พบคำตอบสำหรับคำถามนี้"
                return text_tts
            else:
                text_tts = "หนูไม่เข้าใจคำถาม"
                return text_tts

        else:
            findOne(text_questions)

            with open(result_questions_file_path, "r") as json_file:
                result_questions_json = json.load(json_file)
            
            max_result = max(result_questions_json["result"])
            max_index = result_questions_json["result"].index(max_result)
            max_id = result_questions_json['id'][max_index]
            if max_result >= json_kbubot_config["passscore"]:

                # print(f"คำถามคือ {text_questions}")
                # print(f'คำตอบคือ {questions_tokenize_json["answer"][max_id-1]}')
                # print(f"ID ที่มี Result score มากที่สุดคือ ID: {max_id} ด้วยค่า Result score ที่: {max_result}")

                setLatestQuestions(questions_tokenize_json["question"][max_id-1])
                text_tts = questions_tokenize_json["answer"][max_id-1]
                return text_tts
            else:
                questions_index = questions_tokenize_json["question"].index(questions_latest_json["latest"])
                edit_questions_tokenize_json = questions_tokenize_json["tokenize"][questions_index]
                # print(edit_questions_tokenize_json)
                for edit_list_text_questions in list_text_questions:
                    for i in range(len(edit_questions_tokenize_json)):
                        temp_list = edit_questions_tokenize_json.copy()
                        temp_list[i] = edit_list_text_questions
                        # print(temp_list)
                        findOne("".join(temp_list))
                        result_score = resultAnswer("".join(temp_list))

                        with open(result_questions_file_path, "r") as json_file:
                            result_questions_json = json.load(json_file)

                        max_result = max(result_questions_json["result"])
                        max_index = result_questions_json["result"].index(max_result)

                        if "".join(temp_list) in questions_tokenize_json["question"]:
                            max_index = questions_tokenize_json["question"].index("".join(temp_list))
                            list_data_json_answer["answer"].append(questions_tokenize_json["answer"][max_index])
                        else:
                            list_data_json_answer["answer"].append(questions_tokenize_json["answer"][max_index])

                        list_data_json_answer["question"].append(temp_list.copy())
                        list_data_json_answer["result"].append(result_score)
                        if result_score == json_kbubot_config["resultpass"]:
                            break
                    if result_score == json_kbubot_config["resultpass"]:
                        break

                # print(f"{list_data_json_answer}\n")

                max_result = max(list_data_json_answer["result"])
                max_index = list_data_json_answer["result"].index(max_result)

                # print(f'คำถามคือ {list_data_json_answer["question"][max_index]}')
                # print(f'คำตอบคือ {list_data_json_answer["answer"][max_index]}')
                # print(f"ID ที่มี Result score มากที่สุดคือ ID: {max_index + 1} ด้วยค่า Result score ที่: {max_result}")

                with open(list_data_file_path, "w", encoding="utf-8") as json_file:
                                    json.dump(list_data_json_answer, json_file, ensure_ascii=False, indent=4)

                if result_score == json_kbubot_config["resultpass"]:
                    setLatestQuestions("".join(list_data_json_answer["question"][max_index]))
                    text_tts = list_data_json_answer["answer"][max_index]
                    return text_tts
                elif result_score >= json_kbubot_config["passscore"]:
                    setLatestQuestions("")
                    text_tts = "หนูไม่พบคำตอบสำหรับคำถามนี้"
                    return text_tts
                else:
                    setLatestQuestions("")
                    text_tts = "หนูไม่เข้าใจคำถาม"
                    return text_tts

    else:
        findOne(text_questions)
        result_score = resultAnswer(text_questions)
        if result_score == json_kbubot_config["resultpass"]:
            return text_tts
        else:
            text_tts = "หนูไม่เข้าใจคำถาม"
            return text_tts

if __name__ == "__main__":
    tts_result = findAnswer("เครื่องกลล่ะ")
    print(f"\n{tts_result}")
    # print(word_tokenize("วิศวกรรมโยธา", engine="deepcut"))
    # print(word_tokenize("แล้ววิศวกรรมซ่อมบำรุงล่ะ", engine="deepcut"))
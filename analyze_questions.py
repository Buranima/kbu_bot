from pythainlp.tokenize import word_tokenize
import os
import json

from database import requestDataFormDataQuestionAnswer

latest_questions_file_path = "static/temp/latest_questions.json"
questions_tokenize_file_path = "static/temp/questions_tokenize.json"
result_questions_file_path = "static/temp/result_questions.json"
kbubot_config_file_path = "static/config/json/kbubot_config.json"

if os.path.exists(questions_tokenize_file_path):
    pass
else:
    json_database = json.loads(requestDataFormDataQuestionAnswer())
    data_json = {
        "id":[],
        "question": [],
        "tokenize": [],
        "answer":[]
    }
    for id in range(len(json_database["id"])):
        data_json["id"].append(json_database["id"][id])
        data_json["question"].append(json_database["question"][id])
        data_arry = word_tokenize(json_database["question"][id], engine="newmm")
        data_json["tokenize"].append(data_arry)
        data_json["answer"].append(json_database["answer"][id])
    with open(questions_tokenize_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data_json, json_file, ensure_ascii=False, indent=4)

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
    list_text_questions = word_tokenize(text_questions_find_one, engine="newmm")
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

        print(list_json_questions)
        print(list_text_questions)
        print(f"Len: {len_questions_score}/10")
        print(f"Like: {like_questions_score}/45")
        print(f"Position: {position_questions_score}/45")
        print(f"Score: {sum_score}/100")

        data_json["id"].append(questions_tokenize_json["id"][id])
        data_json["result"].append(sum_score)
        len_questions_score = 0.0
        like_questions_score = 0.0
        position_questions_score = 0.0
        sum_score = 0.0
    with open(result_questions_file_path, "w") as json_file:
        json.dump(data_json, json_file, indent=4)

def resultAnswer(text_result_answer):

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
        print(f"\nคำถามคือ {text_result_answer}")
        print(f'คำตอบคือ {questions_tokenize_json["answer"][max_id-1]}')
        print(f"ID ที่มี Result score มากที่สุดคือ ID: {max_id} ด้วยค่า Result score ที่: {max_result}")
        setLatestQuestions(questions_tokenize_json["question"][max_id-1])
        return max_result
    elif max_result >= json_kbubot_config["passscore"]:
        print(f"\nคำถามคือ {text_result_answer}")
        print(f'คำตอบคือ {questions_tokenize_json["answer"][max_id-1]}')
        print(f"ID ที่มี Result score มากที่สุดคือ ID: {max_id} ด้วยค่า Result score ที่: {max_result}")
        setLatestQuestions(questions_tokenize_json["question"][max_id-1])
        return max_result
    else:
        print(f"\nคำถามคือ {text_result_answer}")
        print(f'คำตอบที่ไกล้เคียงมากที่สุดคือ {questions_tokenize_json["answer"][max_id-1]}')
        print(f"ID ที่มี Result score มากที่สุดคือ ID: {max_id} ด้วยค่า Result score ที่: {max_result}")
        setLatestQuestions("")
        return max_result

def findAnswer(text_questions):
    global questions_tokenize_file_path, result_questions_file_path, latest_questions_file_path

    list_text_questions = word_tokenize(text_questions, engine="newmm")

    result_score = 0.0

    with open(latest_questions_file_path, "r", encoding="utf-8") as file_questions_latest:
        questions_latest_json = json.load(file_questions_latest)

    with open(questions_tokenize_file_path, "r", encoding="utf-8") as file_questions_tokenize:
        questions_tokenize_json = json.load(file_questions_tokenize)

    if os.path.exists(result_questions_file_path):
        if questions_latest_json["latest"] == "":
            findOne(text_questions)
            result_score = resultAnswer(text_questions)

        else:
            findOne(text_questions)

            with open(result_questions_file_path, "r") as json_file:
                result_questions_json = json.load(json_file)

            with open(kbubot_config_file_path, "r", encoding="utf-8") as json_kbubot_config_file:
                json_kbubot_config = json.load(json_kbubot_config_file)
            
            max_result = max(result_questions_json["result"])
            max_index = result_questions_json["result"].index(max_result)
            max_id = result_questions_json['id'][max_index]
            if max_result >= json_kbubot_config["resultpass"]:
                print(f"คำถามคือ {text_questions}")
                print(f'คำตอบคือ {questions_tokenize_json["answer"][max_id-1]}')
                print(f"ID ที่มี Result score มากที่สุดคือ ID: {max_id} ด้วยค่า Result score ที่: {max_result}")
                setLatestQuestions(questions_tokenize_json["question"][max_id-1])
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
                        if result_score > json_kbubot_config["resultpass"]:
                            break
                    if result_score > json_kbubot_config["resultpass"]:
                        break
    else:
        findOne(text_questions)
        result_score = resultAnswer(text_questions)

if __name__ == "__main__":
    findAnswer("คณะวิศวกรรมศาสตร์มีทั้งหมดกี่สาขา")
    # print(word_tokenize("แล้ววิศวกรรมเครื่องกลล่ะ", engine="newmm"))
    # print(word_tokenize("แล้ววิศวกรรมซ่อมบำรุงล่ะ", engine="newmm"))
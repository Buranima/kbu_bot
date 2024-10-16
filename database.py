import mysql.connector
from pythainlp.tokenize import word_tokenize
import json

connect_database = None
cursor_database = None
config_database = None
config_kbubot = None

questions_tokenize_file_path = "static/temp/questions_tokenize.json"
config_database_file_path = "static/config/json/database_config.json"
config_kbubot_file_path = "static/config/json/kbubot_config.json"

def f_load_config():
    global config_database, config_kbubot
    with open(config_database_file_path, "r", encoding="utf-8") as file_config_database:
        config_database = json.load(file_config_database)
    with open(config_kbubot_file_path, "r", encoding="utf-8") as file_config_kbubot:
        config_kbubot = json.load(file_config_kbubot)

def f_auto_id():
    global connect_database, cursor_database
    connectDataBase()
    try:
        cursor_database.execute("SELECT MAX(id) FROM data_question_answer")
        max_id = cursor_database.fetchone()[0]
    except mysql.connector.Error as err:
        # print(f"เกิดข้อผิดพลาด: {err}")
        return
    if max_id is not None:
        try:
            cursor_database.execute(f"ALTER TABLE data_question_answer AUTO_INCREMENT = {max_id + 1};")
            connect_database.commit()
        except mysql.connector.Error as err:
            # print(f"เกิดข้อผิดพลาด: {err}")
            return
        finally:
            cursor_database.close()
            connect_database.close()
    else:
        cursor_database.close()
        connect_database.close()

def loadQuestionsTokenize(json_database):
    global config_kbubot
    data_json = {
        "id":[],
        "question": [],
        "tokenize": [],
        "answer":[]
    }
    for id in range(len(json_database["id"])):
        data_json["id"].append(json_database["id"][id])
        data_json["question"].append(json_database["question"][id])
        data_arry = word_tokenize(json_database["question"][id], engine=config_kbubot["engine"][0])
        data_json["tokenize"].append(data_arry)
        data_json["answer"].append(json_database["answer"][id])
    with open(questions_tokenize_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data_json, json_file, ensure_ascii=False, indent=4)
    # print(data_json)

def connectDataBase():
    global connect_database, cursor_database, config_database
    f_load_config()
    try:
        connect_database = mysql.connector.connect(
            host=config_database["host"][0],
            user=config_database["user"][0],
            password=config_database["password"][0],
            database=config_database["database"][0],
            charset=config_database["charset"][0],
            collation=config_database["collation"][0]
        )
        cursor_database = connect_database.cursor()
        # print("เชื่อมต่อกับฐานข้อมูลได้สำเร็จ\n")
    except mysql.connector.Error as err:
        # print(f"เกิดข้อผิดพลาด: {err}")
        return

def requestDataFormDataQuestionAnswer():
    global connect_database, cursor_database
    connectDataBase()
    cursor_database.execute("SELECT * FROM data_question_answer")
    results_request_data_form_data_question_answer = cursor_database.fetchall()
    data_json = {
        "id": [],
        "question": [],
        "answer": []
    }
    for row_form_data_question_answer in results_request_data_form_data_question_answer:
        data_json["id"].append(row_form_data_question_answer[0])
        data_json["question"].append(row_form_data_question_answer[1])
        data_json["answer"].append(row_form_data_question_answer[2])
    json_data = json.dumps(data_json, ensure_ascii=False, indent=4)
    loadQuestionsTokenize(json.loads(json_data))
    cursor_database.close()
    connect_database.close()
    return json_data

def updateDataFormDataQuestionAnswer(update_data_form_data_question_answer_data):
    global connect_database, cursor_database
    connectDataBase()
    update_data_form_data_question_answer_json_string_data = json.dumps(update_data_form_data_question_answer_data, ensure_ascii=False)
    update_data_form_data_question_answer_json_dictionary_data = json.loads(update_data_form_data_question_answer_json_string_data)
    sql_update_query = """UPDATE data_question_answer SET question = %s, answer = %s WHERE id = %s"""
    values_update_query = (str(update_data_form_data_question_answer_json_dictionary_data["question"]), str(update_data_form_data_question_answer_json_dictionary_data["answer"]), str(update_data_form_data_question_answer_json_dictionary_data["id"]))
    try:
        cursor_database.execute(sql_update_query, values_update_query)
        connect_database.commit()
        # print(f"ข้อมูลที่มี id {int(update_data_form_data_question_answer_json_dictionary_data['id'])} ถูกอัปเดตเรียบร้อยแล้ว")
    except mysql.connector.Error as err:
        # print(f"เกิดข้อผิดพลาด: {err}")
        return
    finally:
        cursor_database.close()
        connect_database.close()

def insertDataToQuestionAnswer(insert_data_question_answer_data):
    global connect_database, cursor_database
    connectDataBase()

    insert_data_question_answer_json_string_data = json.dumps(insert_data_question_answer_data, ensure_ascii=False)
    insert_data_question_answer_json_dictionary_data = json.loads(insert_data_question_answer_json_string_data)

    sql_insert_query = """INSERT INTO data_question_answer (question, answer) VALUES (%s, %s)"""
    values_insert_query = (str(insert_data_question_answer_json_dictionary_data["question"]), str(insert_data_question_answer_json_dictionary_data["answer"]))
    try:
        cursor_database.execute(sql_insert_query, values_insert_query)
        connect_database.commit()
        # print(f"ข้อมูลใหม่ถูกเพิ่มเรียบร้อยแล้ว: {insert_data_question_answer_json_dictionary_data['question']}")
    except mysql.connector.Error as err:
        # print(f"เกิดข้อผิดพลาด: {err}")
        return
    finally:
        cursor_database.close()
        connect_database.close()

def deleteDataFromQuestionAnswer(delete_data_question_answer_data):
    global connect_database, cursor_database
    connectDataBase()
    delete_data_question_answer_json_string_data = json.dumps(delete_data_question_answer_data, ensure_ascii=False)
    delete_data_question_answer_json_dictionary_data = json.loads(delete_data_question_answer_json_string_data)
    sql_delete_query = f"DELETE FROM data_question_answer WHERE id = {delete_data_question_answer_json_dictionary_data['id']}"
    try:
        cursor_database.execute(sql_delete_query)
        connect_database.commit()
        # print(f"ข้อมูลที่มี id {id_to_delete} ถูกลบเรียบร้อยแล้ว")
    except mysql.connector.Error as err:
        # print(f"เกิดข้อผิดพลาดในการลบ: {err}")
        return
    finally:
        cursor_database.close()
        connect_database.close()
    connectDataBase()
    sql_update_query = f"""UPDATE data_question_answer SET id = id - 1 WHERE id > {delete_data_question_answer_json_dictionary_data["id"]}"""
    try:
        cursor_database = connect_database.cursor()
        cursor_database.execute(sql_update_query)
        connect_database.commit()
    except mysql.connector.Error as err:
        # print(f"เกิดข้อผิดพลาดในการอัปเดต ID: {err}")
        return
    finally:
        cursor_database.close()
        connect_database.close()
    f_auto_id()

if __name__ == "__main__":
    # a = {"id":46}
    # deleteDataFromQuestionAnswer(a)
    # a = {"id":46}
    # deleteDataFromQuestionAnswer(a)
    # connectDataBase()
    # sql_update_query = f"""UPDATE data_question_answer SET id = id - 1 WHERE id > 29"""
    # cursor_database = connect_database.cursor()
    # cursor_database.execute(sql_update_query)
    # connect_database.commit()
    # f_auto_id()

    database_view = requestDataFormDataQuestionAnswer()
    print(database_view)
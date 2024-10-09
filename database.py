import mysql.connector
import json

connect_database = None
cursor_database = None
def connectDataBase():
    global connect_database, cursor_database
    try:
        with open("static/config/json/database_config.json", "r") as file_config_database:
            config_database = json.load(file_config_database)
        connect_database = mysql.connector.connect(
            host=config_database["host"][0],
            user=config_database["user"][0],
            password=config_database["password"][0],
            database=config_database["database"][0],
            charset=config_database["charset"][0],
            collation=config_database["collation"][0]
        )
        cursor_database = connect_database.cursor()
        print("เชื่อมต่อกับฐานข้อมูลได้สำเร็จ\n")
    except mysql.connector.Error as err:
        print(f"เกิดข้อผิดพลาด: {err}")

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
        print(f"ข้อมูลที่มี id {int(update_data_form_data_question_answer_json_dictionary_data['id'])} ถูกอัปเดตเรียบร้อยแล้ว")
    except mysql.connector.Error as err:
        print(f"เกิดข้อผิดพลาด: {err}")
    finally:
        cursor_database.close()
        connect_database.close()

if __name__ == "__main__":
    a = requestDataFormDataQuestionAnswer()
    print(str(a))
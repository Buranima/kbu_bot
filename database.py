import mysql.connector
import json

connect_database = None
cursor_database = None
def connectDataBase():
    global connect_database, cursor_database
    connect_database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="kbu_bot",
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
    cursor_database = connect_database.cursor()

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
    # print(str(json_data))
    cursor_database.close()
    connect_database.close()
    return json_data

if __name__ == "__main__":
    a = requestDataFormDataQuestionAnswer()
    print(str(a))
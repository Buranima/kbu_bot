var kbu_bot_socket = io();

kbu_bot_socket.on("data-form-database", (on_data_form_database_json) => {
    console.log(JSON.parse(on_data_form_database_json));
});

var data_form_database_json = { mode: "update", id: 1, question: "", answer: "" };
kbu_bot_socket.emit("data-form-database", data_form_database_json);
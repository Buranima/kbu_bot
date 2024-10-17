var kbu_bot_socket = io();

var data_form_database_json = null
var id = null
var button_l = document.getElementById('left-button');
var button_f = document.getElementById('forward-button');
var button_s = document.getElementById('stop-button');
var button_b = document.getElementById('backward-button');
var button_r = document.getElementById('right-button');

function fetchData() {
    data_form_database_json = { mode: "READ-DATA" };
    kbu_bot_socket.emit("SERVER-CONTROL-PANEL", data_form_database_json);
    // data_form_database_json = { mode: "MICROPHONE" };
    // kbu_bot_socket.emit("SERVER-CONTROL-PANEL", data_form_database_json);
}

function setBatteryLevel(level) {
    var batteryBar = document.getElementById('battery-bar');
    var batteryLabel = document.getElementById('battery-label');
    level = Math.max(0, Math.min(100, level));
    batteryBar.style.width = level + '%';
    if (level > 60) {
        batteryBar.style.backgroundColor = '#4caf50';
    } else if (level > 30) {
        batteryBar.style.backgroundColor = '#ffeb3b';
    } else {
        batteryBar.style.backgroundColor = '#f44336';
    }
    batteryLabel.textContent = "Battery " + level + '%';
}

setBatteryLevel(40);

function setMicrophoneStatus(isMicOn) {
    var micStatus = document.getElementById('microphone-status');

    if (isMicOn) {
        micStatus.textContent = '🎙️ Microphone Normal';
        micStatus.classList.add('mic-on');
    } else {
        micStatus.textContent = '🎙️ Microphone Error!';
        micStatus.classList.remove('mic-on');
    }
}

function toggleLight(buttonId, isLightOn) {
    var button = document.getElementById(buttonId);
    if (isLightOn) {
        button.classList.add('no-light');
        button.disabled = isLightOn;
    } else {
        button.classList.remove('no-light');
        button.disabled = isLightOn;
    }
}

kbu_bot_socket.on("SERVER-CONTROL-PANEL", (on_data_form_database_json) => {
    data = on_data_form_database_json["result"]

    var table = $('#routes-table').DataTable();
    table.clear();

    for (let i = 0; i < data["id-route"].length; i++) {
        const name = data["name-route"][i];
        const statuss = data["status-route"][i];
        id = data["id-route"][i];
        if (statuss == "กำลังใช้งาน") {
            table.row.add([
                name,
                `<button type="button" id="${id}" class="btn btn-primary btn-sm editBtn" style="width: 10vh;" disabled>${statuss}</button>`
            ]);
        }
        else {
            table.row.add([
                name,
                `<button type="button" id="${id}" class="btn btn-primary btn-sm editBtn" style="width: 10vh;">${statuss}</button>`
            ]);
        }
    }
    table.draw();

    if (data["status"] == "stop") {
        toggleLight('left-button', true);
        toggleLight('forward-button', true);
        toggleLight('stop-button', true);
        toggleLight('backward-button', true);
        toggleLight('right-button', true);
    }
    else {
        if (data["control"] == "stop") {
            toggleLight('left-button', false);
            toggleLight('forward-button', false);
            toggleLight('stop-button', true);
            toggleLight('backward-button', false);
            toggleLight('right-button', false);
        }
        else if (data["control"] == "left") {
            toggleLight('left-button', false);
            toggleLight('forward-button', true);
            toggleLight('stop-button', false);
            toggleLight('backward-button', true);
            toggleLight('right-button', true);
        }
        else if (data["control"] == "forward") {
            toggleLight('left-button', true);
            toggleLight('forward-button', false);
            toggleLight('stop-button', false);
            toggleLight('backward-button', true);
            toggleLight('right-button', true);
        }
        else if (data["control"] == "backward") {
            toggleLight('left-button', true);
            toggleLight('forward-button', true);
            toggleLight('stop-button', false);
            toggleLight('backward-button', false);
            toggleLight('right-button', true);
        }
        else if (data["control"] == "right") {
            toggleLight('left-button', true);
            toggleLight('forward-button', true);
            toggleLight('stop-button', false);
            toggleLight('backward-button', true);
            toggleLight('right-button', false);
        }
    }
    
    setMicrophoneStatus(data["microphone"]);
});

$(document).on('click', '.editBtn', function () {
    let buttonIdeditBtn = $(this).attr('id');
    data_form_database_json = { mode: "ROUTE", id_route: Number(buttonIdeditBtn) };
    kbu_bot_socket.emit("SERVER-CONTROL-PANEL", data_form_database_json);
});

$('#left-button').on('click', function () {
    data_form_database_json = { mode: "CONTROL", control: "left" };
    kbu_bot_socket.emit("SERVER-CONTROL-PANEL", data_form_database_json);
});
$('#forward-button').on('click', function () {
    data_form_database_json = { mode: "CONTROL", control: "forward" };
    kbu_bot_socket.emit("SERVER-CONTROL-PANEL", data_form_database_json);
});
$('#stop-button').on('click', function () {
    data_form_database_json = { mode: "CONTROL", control: "stop" };
    kbu_bot_socket.emit("SERVER-CONTROL-PANEL", data_form_database_json);
});
$('#backward-button').on('click', function () {
    data_form_database_json = { mode: "CONTROL", control: "backward" };
    kbu_bot_socket.emit("SERVER-CONTROL-PANEL", data_form_database_json);
});
$('#right-button').on('click', function () {
    data_form_database_json = { mode: "CONTROL", control: "right" };
    kbu_bot_socket.emit("SERVER-CONTROL-PANEL", data_form_database_json);
});

fetchData();
var wake_word = new webkitSpeechRecognition();
wake_word.lang = "th-TH";
wake_word.interimResults = true;
wake_word.continuous = false;
wake_word.maxAlternatives = 1;

var listen_word = new webkitSpeechRecognition();
listen_word.lang = "th-TH";
listen_word.interimResults = false;
listen_word.continuous = false;
listen_word.maxAlternatives = 1;

var kbu_bot_socket = io();

function resetWakeWord() {
    wake_word.onend = function () {
        wake_word.start();
    }
    wake_word.onresult = function (wake_word_event) {
        for (var event_wake_word = wake_word_event.resultIndex; event_wake_word < wake_word_event.results.length; ++event_wake_word) {
            var speechRecognitionAlternative1 = wake_word_event.results[event_wake_word][0];
            var wake_word_script = speechRecognitionAlternative1.transcript;
            var wake_word_script_edit = wake_word_script.replace("ครับ", "");
            wake_word_script_edit = wake_word_script_edit.replace("ค่ะ", "");
            wake_word_script_edit = wake_word_script_edit.replace("จ้า", "");
            wake_word_script_edit = wake_word_script_edit.replace("จ้ะ", "");
            wake_word_script_edit = wake_word_script_edit.replace(" ", "");
            console.log(wake_word_script_edit);
            if (wake_word_script_edit.includes("สวัสดีน้องเกษม")) {
                wake_word.onend = null;
                wake_word.onresult = null;
                wake_word.stop();
                ttsWakeWord("สวัสดีค่ะ มีอะไรให้หนูช่วยมั้ยคะ");
                break;
            }
            else if (wake_word_script_edit.includes("น้องเกษม")) {
                wake_word.onend = null;
                wake_word.onresult = null;
                wake_word.stop();
                ttsWakeWord("ค่าา");
                break;
            }
        }
    }
}

function resetListenWord() {
    listen_word.onend = function () {
        listen_word.onend = null;
        listen_word.onresult = null;
        listen_word.stop();
    }
    listen_word.onresult = function (listen_word_event) {
        var listen_word_script = listen_word_event.results[0][0].transcript;
        var listen_word_script_edit = listen_word_script.replace("ครับ", "");
        listen_word_script_edit = listen_word_script_edit.replace("ค่ะ", "");
        listen_word_script_edit = listen_word_script_edit.replace("จ้า", "");
        listen_word_script_edit = listen_word_script_edit.replace("จ้ะ", "");
        listen_word_script_edit = listen_word_script_edit.replace(" ", "");
        console.log(listen_word_script_edit);
        listen_word.onresult = null;
    }
}

function ttsWakeWord(tts_wake_word_text) {
    var tts_wake_word_json_data = { speech: tts_wake_word_text };
    kbu_bot_socket.emit("tts-wake-word", tts_wake_word_json_data);
}

function ttsListenWord(tts_listen_word_text) {
    var tts_listen_word_json_data = { speech: tts_listen_word_text };
    kbu_bot_socket.emit("tts-listen-word", tts_listen_word_json_data);
}

function playTTSWakeWord(play_tts_wake_word_directory) {
    var play_tts_wake_word_audio = new Audio(play_tts_wake_word_directory);
    play_tts_wake_word_audio.play();
    play_tts_wake_word_audio.addEventListener('ended', function () {
        resetListenWord();
        listen_word.start();
    });
}

function playTTSListenWord(play_tts_listen_word_directory) {
    var play_tts_listen_word_audio = new Audio(play_tts_listen_word_directory);
    play_tts_listen_word_audio.play();
    play_tts_listen_word_audio.addEventListener('ended', function () {
        resetWakeWord();
        wake_word.start();
    });
}

kbu_bot_socket.on("play-tts-wake-word", (play_tts_wake_word_json_data) => {
    console.log(JSON.parse(play_tts_wake_word_json_data).directory);
    playTTSWakeWord(JSON.parse(play_tts_wake_word_json_data).directory);
});

kbu_bot_socket.on("play-tts-listen-word", (play_tts_listen_word_json_data) => {
    console.log(JSON.parse(play_tts_listen_word_json_data).directory);
    playTTSListenWord(JSON.parse(play_tts_listen_word_json_data).directory);
});

resetWakeWord();
wake_word.start();
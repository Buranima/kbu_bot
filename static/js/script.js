var kbu_bot_socket = io();

var wake_word = new webkitSpeechRecognition();
wake_word.lang = "th-TH";
wake_word.interimResults = true;
wake_word.continuous = false;
wake_word.maxAlternatives = 1;

var wake_stop = new webkitSpeechRecognition();
wake_stop.lang = "th-TH";
wake_stop.interimResults = true;
wake_stop.continuous = false;
wake_stop.maxAlternatives = 1;

var listen_word = new webkitSpeechRecognition();
listen_word.lang = "th-TH";
listen_word.interimResults = false;
listen_word.continuous = false;
listen_word.maxAlternatives = 1;

var chat_word = new webkitSpeechRecognition();
chat_word.lang = "th-TH";
chat_word.interimResults = false;
chat_word.continuous = false;
chat_word.maxAlternatives = 1;

var play_text_continue_audio = new Audio("static/base/sound/march_KBU.mp3");
var list_sound_background = null;
var continue_play = 1;
var continue_animation = 1;
var config_bot_json = null;
var play_tts_question_audio = new Audio("static/base/sound/march_KBU.mp3");
var play_chat_bot_audio = new Audio("static/base/sound/march_KBU.mp3");

function resetWakeWord() {
    changeText('พูดว่า "สวัสดีน้องเกษม"');
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

            if (wake_word_script_edit.includes("สวัสดี" + config_bot_json["wakeword"][0])) {
                continue_animation = 0;
                autoAnimationEye();
                playAudioBackground("no");
                wake_word.onend = null;
                wake_word.onresult = null;
                wake_word.stop();
                ttsWakeWord("สวัสดีค่ะ มีอะไรให้หนูช่วยมั้ยคะ");
                break;
            }
            else if (wake_word_script_edit.includes(config_bot_json["wakeword"][0])) {
                continue_animation = 0;
                autoAnimationEye();
                playAudioBackground("no");
                wake_word.onend = null;
                wake_word.onresult = null;
                wake_word.stop();
                ttsWakeWord("ค่าา");
                break;
            }
        }
    }
}

function resetWakeStop() {
    wake_stop.onend = function () {
        wake_stop.start();
    }
    wake_stop.onresult = function (wake_stop_event) {
        for (var event_wake_stop = wake_stop_event.resultIndex; event_wake_stop < wake_stop_event.results.length; ++event_wake_stop) {
            var speechRecognitionAlternative2 = wake_stop_event.results[event_wake_stop][0];
            var wake_stop_script = speechRecognitionAlternative2.transcript;
            var wake_stop_script_edit = wake_stop_script.replace("ครับ", "");
            wake_stop_script_edit = wake_stop_script_edit.replace("ค่ะ", "");
            wake_stop_script_edit = wake_stop_script_edit.replace("จ้า", "");
            wake_stop_script_edit = wake_stop_script_edit.replace("จ้ะ", "");
            wake_stop_script_edit = wake_stop_script_edit.replace(" ", "");
            console.log(wake_stop_script_edit);

            if (wake_stop_script_edit.includes(config_bot_json["wakeword"][0] + "หยุด")) {
                continue_animation = 0;
                autoAnimationEye();
                playAudioBackground("no");
                wake_stop.onend = null;
                wake_stop.onresult = null;
                wake_stop.stop();
                if (!play_tts_question_audio.paused) {
                    play_tts_question_audio.pause();
                    setLatestChatBot();
                    ttsWakeWord("โอเคค่ะ มีอะไรสอบถามเพิ่มเติมมั้ยคะ");
                }
                if (!play_chat_bot_audio.paused) {
                    play_chat_bot_audio.pause();
                    setLatestChatBot();
                    ttsListenWord("โอเคค่ะ แล้วเจอกันใหม่ค่าา");
                }
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
        setLatestChatBot();
        ttsListenWord("หากมีคำถามที่ต้องการถามสามารถเรียกหนูได้เลยนะคะ");
    }
    listen_word.onresult = function (listen_word_event) {
        var listen_word_script = listen_word_event.results[0][0].transcript;
        var listen_word_script_edit = listen_word_script.replace("ครับ", "");
        listen_word_script_edit = listen_word_script_edit.replace("ค่ะ", "");
        listen_word_script_edit = listen_word_script_edit.replace("จ้า", "");
        listen_word_script_edit = listen_word_script_edit.replace("จ้ะ", "");
        listen_word_script_edit = listen_word_script_edit.replace(" ", "");
        console.log(listen_word_script_edit);
        changeText(listen_word_script_edit);
        listen_word.onend = null;
        listen_word.onresult = null;
        listen_word.stop();
        if (listen_word_script_edit == "เปิดเสียงพื้นหลัง") {
            continue_play = 1;
            ttsListenWord("หนูเปิดเสียงพื้นหลังให้แล้วค่ะ");
        }
        else if (listen_word_script_edit == "ปิดเสียงพื้นหลัง") {
            continue_play = 0;
            ttsListenWord("หนูปิดเสียงพื้นหลังให้แล้วค่ะ");
        }
        else if (listen_word_script_edit == "เปิดเพลงประกอบ") {
            continue_play = 1;
            ttsListenWord("หนูเปิดเพลงประกอบให้แล้วค่ะ");
        }
        else if (listen_word_script_edit == "ปิดเพลงประกอบ") {
            continue_play = 0;
            ttsListenWord("หนูปิดเพลงประกอบให้แล้วค่ะ");
        }
        else if (listen_word_script_edit == "คุยกับ" + config_bot_json["wakeword"][0]) {
            changeImage("process");
            changeText('ยินดีต้นรับสู่แชท' + config_bot_json["wakeword"][0]);
            chatBot();
        }
        else if (listen_word_script_edit == "โหลดโปรแกรมใหม่") {
            location.reload();
        }
        else if (listen_word_script_edit == "โหลดแชทใหม่") {
            setLatestChatBot();
            chatBot();
        }
        else if (listen_word_script_edit == "ไม่มี") {
            ttsListenWord("แล้วเจอกันใหม่นะคะ");
        }
        else if (listen_word_script_edit == "ไม่") {
            ttsListenWord("แล้วเจอกันใหม่นะคะ");
        }
        else {
            changeImage("process");
            ttsQuestion(listen_word_script_edit);
        }
    }
}

function resetChat() {
    chat_word.onend = function () {
        chat_word.onend = null;
        chat_word.onresult = null;
        chat_word.stop();
        setLatestChatBot();
        ttsListenWord("หากมีคำถามที่ต้องการถามสามารถเรียกหนูได้เลยนะคะ");
    }
    chat_word.onresult = function (chat_word_event) {
        var chat_word_script = chat_word_event.results[0][0].transcript;
        var chat_word_script_edit = chat_word_script.replace("ครับ", "");
        chat_word_script_edit = chat_word_script_edit.replace("ค่ะ", "");
        chat_word_script_edit = chat_word_script_edit.replace("จ้า", "");
        chat_word_script_edit = chat_word_script_edit.replace("จ้ะ", "");
        chat_word_script_edit = chat_word_script_edit.replace(" ", "");
        console.log(chat_word_script_edit);
        changeText(chat_word_script_edit);
        chat_word.onend = null;
        chat_word.onresult = null;
        chat_word.stop();
        if (chat_word_script_edit == "หยุดคุยกับ" + config_bot_json["wakeword"][0]) {
            continue_play = 0;
            setLatestChatBot();
            ttsListenWord("แล้วกลับมาคุยกับหนูใหม่นะคะ");
        }
        else if (chat_word_script_edit == "โหลดโปรแกรมใหม่") {
            continue_play = 0;
            location.reload();
        }
        else {
            changeImage("process");
            ttsChatBot(chat_word_script_edit);
        }
    }
}

function loadConfigJson() {
    fetch("static/config/json/kbubot_config.json")
        .then(response => {
            if (!response.ok) {
                throw new Error("การตอบสนองของเครือข่ายไม่ถูกต้อง " + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            config_bot_json = data;
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

function ttsWakeWord(tts_wake_word_text) {
    var tts_wake_word_json_data = { speech: tts_wake_word_text };
    kbu_bot_socket.emit("tts-wake-word", tts_wake_word_json_data);
}

function ttsListenWord(tts_listen_word_text) {
    var tts_listen_word_json_data = { speech: tts_listen_word_text };
    kbu_bot_socket.emit("tts-listen-word", tts_listen_word_json_data);
}

function ttsQuestion(tts_question) {
    var tts_listen_word_json_data = { speech: tts_question };
    kbu_bot_socket.emit("tts-question", tts_listen_word_json_data);
}

function loadListSound(text_sound) {
    var text_sound_json_data = { mode: text_sound };
    kbu_bot_socket.emit("load-list-sound", text_sound_json_data);
}

function chatBot() {
    ttsChatBot("สวัสดี");
}

function ttsChatBot(tts_chat_bot) {
    var tts_chat_bot_json_data = { mode: "TTS", speech: tts_chat_bot };
    kbu_bot_socket.emit("tts-chat-bot", tts_chat_bot_json_data);
}

function playTTSWakeWord(play_tts_wake_word_directory) {
    changeImage("speak");
    var play_tts_wake_word_audio = new Audio(play_tts_wake_word_directory + new Date().getTime());
    play_tts_wake_word_audio.play();
    play_tts_wake_word_audio.addEventListener("ended", function () {
        changeImage("listen");
        listen_word.start();
        changeText('กำลังฟัง...');
        resetListenWord();
        continue_animation = 0;
        autoAnimationEye();
    });
}

function playTTSListenWord(play_tts_listen_word_directory) {
    changeImage("speak");
    changeText('กำลังตอบ...');
    var play_tts_listen_word_audio = new Audio(play_tts_listen_word_directory + new Date().getTime());
    play_tts_listen_word_audio.play();
    play_tts_listen_word_audio.addEventListener("ended", function () {
        changeImage("still");
        wake_word.start();
        resetWakeWord();
        playAudioBackground("yes");
        continue_animation = 1;
        autoAnimationEye();
    });
}

function playTTSQuestion(play_tts_question_directory) {
    changeImage("speak");
    changeText('กำลังตอบ...');
    play_tts_question_audio = new Audio(play_tts_question_directory + new Date().getTime());
    play_tts_question_audio.play();

    resetWakeStop();
    wake_stop.start();

    play_tts_question_audio.addEventListener("ended", function () {
        wake_stop.onend = null;
        wake_stop.onresult = null;
        wake_stop.stop();

        changeImage("listen");
        listen_word.start();
        changeText('กำลังฟัง...');
        resetListenWord();
        continue_animation = 0;
        autoAnimationEye();
    });
}

function playTTSChatBot(play_chat_bot_directory) {
    changeImage("speak");
    changeText('กำลังตอบ...');
    play_chat_bot_audio = new Audio(play_chat_bot_directory + new Date().getTime());
    play_chat_bot_audio.play();

    resetWakeStop();
    wake_stop.start();

    play_chat_bot_audio.addEventListener("ended", function () {
        wake_stop.onend = null;
        wake_stop.onresult = null;
        wake_stop.stop();

        changeImage("listen");
        chat_word.start();
        changeText('กำลังฟัง...');
        resetChat();
        continue_animation = 0;
        autoAnimationEye();
    });
}

function playAudioBackground(text_continue) {
    if (text_continue == "yes") {
        // console.log(continue_play);
        if (continue_play == 1) {
            var length_num = (list_sound_background["sound"].length) - 1;
            var random_num = Math.floor(Math.random() * ((length_num - 0) + 1)) + 0;
            play_text_continue_audio = new Audio(list_sound_background["sound"][random_num] + new Date().getTime());
            play_text_continue_audio.play();
            play_text_continue_audio.addEventListener("ended", function () {
                setTimeout(() => {
                    playAudioBackground("yes");
                }, Math.floor(Math.random() * ((3 * 60 * 1000) - (1 * 60 * 1000) + 1)) + (1 * 60 * 1000));
            });
        }
    }
    else if (text_continue == "no") {
        // console.log(continue_play);
        if (!play_text_continue_audio.paused) {
            play_text_continue_audio.addEventListener("ended", function () {
            });
            play_text_continue_audio.pause();
        }
    }
}

function changeImage(action_bot) {
    var image_action_left = document.getElementById("eye_image_left");
    image_action_left.style.opacity = "1";
    var image_action_right = document.getElementById("eye_image_right");
    image_action_right.style.opacity = "1";
    if (action_bot == "still") {
        image_action_left.src = "static/base/img/eyes.gif";
        image_action_right.src = "static/base/img/eyes.gif";
    }
    else if (action_bot == "speak") {
        image_action_left.src = "static/config/img/speaking.gif";
        image_action_right.src = "static/config/img/speaking.gif";
    }
    else if (action_bot == "listen") {
        image_action_left.src = "static/config/img/microphone.gif";
        image_action_right.src = "static/config/img/microphone.gif";
    }
    else if (action_bot == "process") {
        image_action_left.src = "static/config/img/loading.gif";
        image_action_right.src = "static/config/img/loading.gif";
    }
}

function animationEye() {
    var image_action_left = document.getElementById("eye_image_left");
    image_action_left.style.opacity = "0";
    var image_action_right = document.getElementById("eye_image_right");
    image_action_right.style.opacity = "0";
    var left_eye = document.querySelector(".left_eyes_area");
    var right_eye = document.querySelector(".right_eyes_area");
    var keyframes = [
        { height: '40%' },
        { height: '0%' },
        { height: '40%' }
    ];
    var options = {
        duration: 500,
        iterations: 1,
        easing: 'linear',
        fill: 'forwards'
    };
    left_eye.animate(keyframes, options);
    right_eye.animate(keyframes, options);
}

function autoAnimationEye() {
    setTimeout(() => {
        if (continue_animation == 1) {
            animationEye();
            autoAnimationEye();
        }
    }, Math.floor(Math.random() * (((6 * 60 * 10) - (1 * 60 * 10)) + 1)) + (1 * 60 * 10));
}

function setLatestChatBot() {
    var set_latest_chat_bot_json_data = { mode: "SetLatestChatBot" };
    kbu_bot_socket.emit("tts-chat-bot", set_latest_chat_bot_json_data);
}

function changeText(change_text) {
    document.getElementById("dynamicText").innerHTML = change_text;
}



kbu_bot_socket.on("play-tts-wake-word", (play_tts_wake_word_json_data) => {
    playAudioBackground("no");
    playTTSWakeWord(play_tts_wake_word_json_data["directory"]);
});

kbu_bot_socket.on("play-tts-listen-word", (play_tts_listen_word_json_data) => {
    playAudioBackground("no");
    playTTSListenWord(play_tts_listen_word_json_data["directory"]);
});

kbu_bot_socket.on("tts-question", (play_tts_question_json_data) => {
    playAudioBackground("no");
    playTTSQuestion(play_tts_question_json_data["directory"]);
});

kbu_bot_socket.on("load-list-sound", (load_list_sound_json_data) => {
    list_sound_background = load_list_sound_json_data;
    continue_play = config_bot_json["playsound"]
    if (continue_play == 1) {
        playAudioBackground("yes");
    }
    else {
        playAudioBackground("no");
    }
});

kbu_bot_socket.on("tts-chat-bot", (play_tts_chat_bot_json_data) => {
    playAudioBackground("no");
    playTTSChatBot(play_tts_chat_bot_json_data["directory"]);
});

loadConfigJson()

wake_word.start();
resetWakeWord();

loadListSound("read");

autoAnimationEye();

setLatestChatBot();
var wake_word = new webkitSpeechRecognition();
wake_word.lang = "th-TH";
wake_word.interimResults = true;
wake_word.continuous = false;
wake_word.maxAlternatives = 1;

function resetWakeWord() {
    wake_word.onend = function () {
        wake_word.start();
    }
    wake_word.onresult = function (event) {
        for (var event_wake_word = event.resultIndex; event_wake_word < event.results.length; ++event_wake_word) {
            var speechRecognitionAlternative1 = event.results[event_wake_word][0];
            var tranScript1 = speechRecognitionAlternative1.transcript;
            var newtranScript1 = tranScript1.replace("ครับ", "");
            newtranScript1 = newtranScript1.replace("ค่ะ", "");
            newtranScript1 = newtranScript1.replace("จ้า", "");
            newtranScript1 = newtranScript1.replace("จ้ะ", "");
            newtranScript1 = newtranScript1.replace(" ", "");
            console.log(newtranScript1);
            if (newtranScript1.includes("สวัสดีน้องเกษม")) {
                wake_word.onend = null;
                wake_word.onresult = null;
                wake_word.stop();
                break;
            }
            else if (newtranScript1.includes("น้องเกษม")) {
                wake_word.onend = null;
                wake_word.onresult = null;
                wake_word.stop();
                break;
            }
        }
    }
}
resetWakeWord();
wake_word.start();
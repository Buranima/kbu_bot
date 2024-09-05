function startAnimation() {
    document.querySelector('.start-button').style.display = 'none';
    document.querySelector('.face').style.display = 'block';
    document.body.requestFullscreen();

    const audio = document.getElementById('startSound');
    audio.volume = 0.7; // ปรับระดับเสียง

    function playRandomSong(audioFiles) {
        const randomSong = audioFiles[Math.floor(Math.random() * audioFiles.length)];
        audio.src = randomSong;
        audio.play();
    }

    // โหลดไฟล์ JSON เพื่อดึงรายการเพลง
    fetch('static/temp/sound_list.json') // แก้ไข path นี้ให้ตรงกับไฟล์ JSON ของคุณ
        .then(response => response.json())
        .then(data => {
            const audioFiles = data.sound_list;

            playRandomSong(audioFiles);

            // เมื่อเพลงเล่นจบ ให้เลือกเพลงใหม่แบบสุ่มและรอเวลาสุ่มก่อนเล่นใหม่
            audio.addEventListener('ended', () => {
                const randomDelay = Math.random() * 120000 + 60000; // เวลาสุ่มระหว่าง 60,000 ถึง 180,000 มิลลิวินาที (1 ถึง 3 นาที)
                setTimeout(() => {
                    playRandomSong(audioFiles);
                }, randomDelay);
            });
        })
        .catch(error => console.error('Error loading sound list:', error));

    // โหลดไฟล์ wakeword และเรียก reset_wake หลังจากโหลดเสร็จ
    fetch('static/config/wakeword_config.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            var wakeword = data.wakeword[0];
            reset_wake(audio, wakeword); // ย้ายการเรียก reset_wake มาที่นี่
        })
        .catch(error => console.error('Error loading JSON:', error));

    // Start blinking loop
    playBlinkingLoop();
    recognition_wake.start();
}

function playBlinkingLoop() {
    eyes.startBlinking();
    setTimeout(playBlinkingLoop, Math.random() * 3000 + 1000);
}

class EyeController {
    constructor(elements = {}, eyeSize = '33.33vmin') {
        this._eyeSize = eyeSize;
        this._blinkTimeoutID = null;

        this.setElements(elements);
    }

    get leftEye() { return this._leftEye; }
    get rightEye() { return this._rightEye; }

    setElements({
        leftEye,
        rightEye,
        upperLeftEyelid,
        upperRightEyelid,
        lowerLeftEyelid,
        lowerRightEyelid,
    } = {}) {
        this._leftEye = leftEye;
        this._rightEye = rightEye;
        this._upperLeftEyelid = upperLeftEyelid;
        this._upperRightEyelid = upperRightEyelid;
        this._lowerLeftEyelid = lowerLeftEyelid;
        this._lowerRightEyelid = lowerRightEyelid;
        return this;
    }

    _createKeyframes({
        tgtTranYValUpper = 0,
        enteredOffset = 1 / 3,
        exitingOffset = 2 / 3,
    } = {}) {
        return [
            { transform: `translateY(0px)`, offset: 0.0 },
            { transform: `translateY(${tgtTranYValUpper})`, offset: enteredOffset },
            { transform: `translateY(${tgtTranYValUpper})`, offset: exitingOffset },
            { transform: `translateY(0px)`, offset: 1.0 },
        ];
    }

    startBlinking({
        duration = 100,
        maxInterval = 5000,
        tgtTranYValUpper = `calc(${this._eyeSize} / 2)`,
        tgtTranYValLower = `calc(-${this._eyeSize} / 2)`,
    } = {}) {
        if (this._blinkTimeoutID) {
            //console.warn(`Already blinking with timeoutID=${this._blinkTimeoutID}; return;`);
            return;
        }

        const options = {
            duration: duration,
        };

        const blink = () => {
            this._upperLeftEyelid.animate(this._createKeyframes({
                tgtTranYValUpper: tgtTranYValUpper,
                enteredOffset: 0.5,
                exitingOffset: 0.5,
            }), options);
            this._upperRightEyelid.animate(this._createKeyframes({
                tgtTranYValUpper: tgtTranYValUpper,
                enteredOffset: 0.5,
                exitingOffset: 0.5,
            }), options);

            this._lowerLeftEyelid.animate(this._createKeyframes({
                tgtTranYValUpper: tgtTranYValLower,
                enteredOffset: 0.5,
                exitingOffset: 0.5,
            }), options);
            this._lowerRightEyelid.animate(this._createKeyframes({
                tgtTranYValUpper: tgtTranYValLower,
                enteredOffset: 0.5,
                exitingOffset: 0.5,
            }), options);
        };

        const blinkRandomly = (timeout) => {
            this._blinkTimeoutID = setTimeout(() => {
                blink();
                blinkRandomly(Math.random() * maxInterval);
            }, timeout);
        }

        blinkRandomly(Math.random() * maxInterval);
    }

    stopBlinking() {
        clearTimeout(this._blinkTimeoutID);
    }
}

const eyes = new EyeController({
    leftEye: document.querySelector('.eye.left'),
    rightEye: document.querySelector('.eye.right'),
    upperLeftEyelid: document.querySelector('.eye.left > .eyelid.upper'),
    upperRightEyelid: document.querySelector('.eye.right > .eyelid.upper'),
    lowerLeftEyelid: document.querySelector('.eye.left > .eyelid.lower'),
    lowerRightEyelid: document.querySelector('.eye.right > .eyelid.lower'),
});

eyes.startBlinking({ duration: 300, maxInterval: 5000 });

var recognition_wake = new webkitSpeechRecognition();
recognition_wake.lang = 'th-TH';
recognition_wake.interimResults = true;
recognition_wake.continuous = false;
recognition_wake.maxAlternatives = 1;

function reset_wake(audio, wakeword) {
    recognition_wake.onend = function () {
        recognition_wake.start();
    };
    recognition_wake.onresult = function (event) {
        for (var resultIndex = event.resultIndex; resultIndex < event.results.length; ++resultIndex) {
            var speechRecognitionAlternative_wake = event.results[resultIndex][0];
            var tranScript_wake = speechRecognitionAlternative_wake.transcript;
            var newtranScript_wake = tranScript_wake.replace('ครับ', "").replace('ค่ะ', "").replace('จ้า', "").replace('จ้ะ', "").replace(' ', "");
            console.log(newtranScript_wake);

            if (newtranScript_wake.includes(wakeword)) {
                audio.pause();
                audio.currentTime = 0;
                recognition_wake.stop();
                eyes.stopBlinking(); // หยุดการกระพริบตาที่นี่

                // เพิ่มคลาส .shrink เพื่อให้ดวงตาเล็กลง
                document.querySelector('.eye.left').classList.add('shrink');
                document.querySelector('.eye.right').classList.add('shrink');

                break;
            }
        }
    };
}
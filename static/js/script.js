// Function to start the animation and play random songs
function startAnimation() {
    document.querySelector('.start-button').style.display = 'none';
    document.querySelector('.face').style.display = 'block';
    document.body.requestFullscreen();

    const audio = document.getElementById('startSound');
    audio.volume = 0.7; // Adjust volume

    function playRandomSong(audioFiles) {
        const randomSong = audioFiles[Math.floor(Math.random() * audioFiles.length)];
        audio.src = randomSong;
        audio.play();
    }

    // Load JSON file to get the list of songs
    fetch('static/temp/sound_list.json') // Update path to your JSON file
        .then(response => response.json())
        .then(data => {
            const audioFiles = data.sound_list;

            playRandomSong(audioFiles);

            // Play a new random song after the current one ends
            audio.addEventListener('ended', () => {
                const randomDelay = Math.random() * 120000 + 60000; // Random delay between 1 to 3 minutes
                setTimeout(() => {
                    playRandomSong(audioFiles);
                }, randomDelay);
            });
        })
        .catch(error => console.error('Error loading sound list:', error));

    // Load wakeword config and start recognition
    fetch('static/config/wakeword_config.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            var wakeword = data.wakeword[0];
            reset_wake(audio, wakeword); // Call reset_wake after loading
        })
        .catch(error => console.error('Error loading JSON:', error));

    // Start blinking loop
    playBlinkingLoop();
    recognition_wake.start();
}

// Function to handle blinking animation
function playBlinkingLoop() {
    eyes.startBlinking();
    setTimeout(playBlinkingLoop, Math.random() * 3000 + 1000);
}

// EyeController class
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

    resizeEyes(newSize) {
        this._eyeSize = newSize;
        document.documentElement.style.setProperty('--eye-size', newSize);
        this.stopBlinking();
        this.startBlinking({ duration: 300, maxInterval: 5000 });
    }
}

// Initialize EyeController with elements
const eyes = new EyeController({
    leftEye: document.querySelector('.eye.left'),
    rightEye: document.querySelector('.eye.right'),
    upperLeftEyelid: document.querySelector('.eye.left > .eyelid.upper'),
    upperRightEyelid: document.querySelector('.eye.right > .eyelid.upper'),
    lowerLeftEyelid: document.querySelector('.eye.left > .eyelid.lower'),
    lowerRightEyelid: document.querySelector('.eye.right > .eyelid.lower'),
});

eyes.startBlinking({ duration: 300, maxInterval: 5000 });

// Initialize speech recognition
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
                // Stop and reset the audio
                audio.pause();
                audio.currentTime = 0;

                // Gradually resize eyes
                graduallyResizeEyes('2vmin'); // Adjust size as needed

                // Stop speech recognition
                recognition_wake.stop();
                break;
            }
        }
    };
}

// Function to reset the eye size (optional)
function resizeEyes(newSize) {
    this._eyeSize = newSize;
    document.documentElement.style.setProperty('--eye-size', newSize);
    this.stopBlinking();
    // this.startBlinking({ duration: 300, maxInterval: 5000 });
}

// Function to gradually resize eyes
function graduallyResizeEyes(newSize, duration = 500) {
    const startSize = getComputedStyle(document.documentElement).getPropertyValue('--eye-size');
    const startValue = parseFloat(startSize);
    const endValue = parseFloat(newSize);
    const startTime = performance.now();

    function resize() {
        const currentTime = performance.now();
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1); // Ensure progress is between 0 and 1
        const newSizeValue = startValue + (endValue - startValue) * progress;

        eyes.resizeEyes(`${newSizeValue}vmin`);

        if (progress < 1) {
            requestAnimationFrame(resize);
        }
    }

    resize();
}
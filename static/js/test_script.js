function setBatteryLevel(level) {
    var batteryBar = document.getElementById('battery-bar');
    var batteryLabel = document.getElementById('battery-label');

    // จำกัดค่าระหว่าง 0 ถึง 100
    level = Math.max(0, Math.min(100, level));

    // ปรับความกว้างของแท่นบาร์ตามระดับแบตเตอรี่
    batteryBar.style.width = level + '%';

    // เปลี่ยนสีของแท่นบาร์ตามระดับแบตเตอรี่
    if (level > 60) {
        batteryBar.style.backgroundColor = '#4caf50'; // เขียว
    } else if (level > 30) {
        batteryBar.style.backgroundColor = '#ffeb3b'; // เหลือง
    } else {
        batteryBar.style.backgroundColor = '#f44336'; // แดง
    }

    // แสดงข้อความระดับแบตเตอรี่
    batteryLabel.textContent = level + '%';
}

setBatteryLevel(40);

// ฟังก์ชันนี้ใช้สำหรับรับสถานะจากภายนอก
function setMicrophoneStatus(isMicOn) {
    var micStatus = document.getElementById('microphone-status');

    if (isMicOn) {
        // ถ้าไมโครโฟนเปิดอยู่
        micStatus.textContent = '🎙️ Microphone Normal';
        micStatus.classList.add('mic-on'); // เปลี่ยนสีเป็นเขียว
    } else {
        // ถ้าไมโครโฟนปิดอยู่
        micStatus.textContent = '🎙️ Microphone Error!';
        micStatus.classList.remove('mic-on'); // เปลี่ยนสีเป็นแดง
    }
}

setMicrophoneStatus(false);

function toggleLight(isLightOn) {
    var button = document.getElementById('control-button');
    if (isLightOn) {
        button.classList.add('no-light');
    } else {
        button.classList.remove('no-light');
    }
}

toggleLight(false);
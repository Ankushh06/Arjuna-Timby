# 🎯 Arjuna–Timby

### AI-Based Hand Tracking Turret System

Arjuna–Timby is a real-time computer vision project that uses a webcam to track hand movements and control a servo-based turret using Arduino. The system also includes gesture-based laser control for an interactive targeting experience.

---

## 🚀 Features

* ✋ Real-time hand tracking using MediaPipe
* 🎯 Servo-based turret control (X & Y axis)
* 🔴 Laser targeting system
* ⚡ Gesture control:

  * ✊ Closed fist → Move turret
  * ✋ Open hand → Laser blink
* 🧠 Smooth motion using filtering
* 📊 Live UI with crosshair and coordinates

---

## 🧠 How It Works

```text
Camera → Hand Detection → Coordinate Calculation → Angle Conversion → 
Serial Communication → Arduino → Servo Movement + Laser Control
```

---

## 🔧 Hardware Requirements

* Arduino Uno
* 2 × Servo Motors (SG90 / MG90S)
* Laser module
* Breadboard
* Jumper wires
* External 5V power supply (recommended)
* USB cable
* Webcam (Laptop camera)

---

## 💻 Software Requirements

* Python 3.10
* Arduino IDE

### Python Libraries:

```bash
pip install opencv-python
pip install cvzone
pip install mediapipe
pip install numpy
pip install pyserial
```

---

## 📁 Project Structure

```text
Arjuna-Timby/
│
├── Arjuna.py          # Main Python script
├── Angles.py          # Angle calculation module
├── Timby.ino          # Arduino code
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Arduino Setup

* Open `Timby.ino` in Arduino IDE
* Select correct board and port
* Upload code to Arduino

---

### 2. Python Setup

* Install required libraries
* Place `Angles.py` in same folder as `Arjuna.py`

---

### 3. Update COM Port

```python
serialcomm = serial.Serial('COM6', 115200)
```

👉 Replace `COM6` with your Arduino port

---

### 4. Run the Project

```bash
python Arjuna.py
```

---

## 🎮 Controls

| Gesture       | Action      |
| ------------- | ----------- |
| ✊ Closed fist | Move turret |
| ✋ Open hand   | Laser blink |
| ❌ No hand     | Laser OFF   |

---

## 🔌 Connections

```text
Servo X → Pin 9  
Servo Y → Pin 10  
Laser → Pin 7  

External 5V → Servo VCC  
Common GND → All components
```

---

## ⚠️ Important Notes

* Use external power for servos (Arduino 5V is not enough)
* Ensure common ground between Arduino and power source
* Close Serial Monitor before running Python
* Use low-power laser module (safety first)

---

## 📌 Applications

* Robotics control
* Surveillance systems
* Gesture-based interfaces
* Smart home systems
* Educational projects

---

## 🚀 Future Improvements

* Face / object tracking (YOLO)
* Wireless communication (Bluetooth/WiFi)
* 3D movement (Z-axis hardware)
* Sound effects & UI enhancements

---

## 🏁 Conclusion

This project demonstrates the integration of computer vision and embedded systems to create a real-time interactive tracking system. It serves as a strong foundation for advanced robotics and AI-based control systems.

---
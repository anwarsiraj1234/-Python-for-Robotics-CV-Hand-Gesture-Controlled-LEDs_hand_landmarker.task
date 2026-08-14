🤖 Python for Robotics: Hand Gesture Controlled LEDs
Using Python, OpenCV, MediaPipe, Serial Communication & Arduino UNO
Made By Sir Anwar Siraj
DS & AI ROBOTICS
________________________________________
📌 Project Overview
This project demonstrates how Python, OpenCV, MediaPipe, PySerial, and Arduino UNO can work together to control physical LEDs using hand gestures.
A webcam captures the user's hand. Python processes the camera image using OpenCV and MediaPipe, detects the position of the fingers, converts the detected finger states into 0 and 1, and sends the command to Arduino through USB Serial communication.
Arduino receives the command and controls five LEDs connected to digital pins D8–D12.
🎯 Main Robotics Principle
SENSE → PROCESS / THINK → COMMUNICATE → ACT
________________________________________
🔄 Complete System Architecture
             📷 WEBCAM
                  │
                  ▼
          🐍 PYTHON PROGRAM
                  │
          ┌───────┴────────┐
          │                │
       OpenCV          MediaPipe
          │                │
          └───────┬────────┘
                  ▼
       ✋ HAND LANDMARK DETECTION
                  │
                  ▼
        ☝️ FINGER STATE DETECTION
                  │
                  ▼
           5 DIGITAL STATES
             10101
                  │
                  ▼
            USB / SERIAL
                  │
                  ▼
            🔌 ARDUINO UNO
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
      D8         D9         D10
       │          │          │
     LED 1      LED 2      LED 3

       D11                  D12
        │                    │
      LED 4                LED 5


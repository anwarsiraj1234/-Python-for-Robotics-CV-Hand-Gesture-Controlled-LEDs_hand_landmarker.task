# =====================================================================
# MADE BY SIR ANWAR SIRAJ DS AND AI ROBOTICS 
# PYTHON FOR ROBOTICS
# How to Control LEDs with Hand Gestures Using Mediapipe, OpenCV, and Arduino
# =====================================================================

import cv2
import mediapipe as mp
import serial
import time

# =====================================================================
# INITIALIZATION & SETUP
# =====================================================================

# Configured explicitly for COM7 to talk to your verified Arduino hardware setup
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=1)
time.sleep(2)  # Short delay to allow the serial connection to initialize and stabilize

# Initialize MediaPipe Hands solution and drawing utilities for visualization
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# =====================================================================
# GESTURE DETECTION LOGIC
# =====================================================================

def detect_fingers(image, hand_landmarks):
    """
    Analyzes hand landmarks to determine if fingers are extended (1) or folded (0).
    Returns a list of 5 integers corresponding to: [Thumb, Index, Middle, Ring, Pinky]
    """
    finger_tips = [8, 12, 16, 20]  # MediaPipe landmark IDs for Index, Middle, Ring, Pinky tips
    thumb_tip = 4                  # MediaPipe landmark ID for the Thumb tip
    finger_states = [0, 0, 0, 0, 0]  # Default state: all fingers closed/down

    # 1. Check Thumb State
    # Compares the X-coordinate of the thumb tip against the joint immediately below it (landmark 3).
    # Note: This logic assumes a right hand facing the camera.
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        finger_states[0] = 1  # Thumb is extended (up)

    # 2. Check Other 4 Fingers State
    # Compares the Y-coordinate of each fingertip against its PIP joint (2 nodes down from the tip).
    # In screen coordinates, a lower Y value means the point is higher up on the physical screen.
    for idx, tip in enumerate(finger_tips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states[idx + 1] = 1  # Finger is extended (up)

    return finger_states

# =====================================================================
# MAIN VIDEO CAPTURE LOOP
# =====================================================================

# Open the default webcam (Index 0)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        break

    # Flip the image horizontally for a natural 'mirror' effect, then convert BGR to RGB
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    
    # Process the image frame using MediaPipe to detect hands
    results = hands.process(image)
    
    # Convert the image back to BGR for proper display inside OpenCV window
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # If hands are detected in the frame
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the skeleton joints and connection lines on the visual output
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Extract the current state of the fingers
            fingers_state = detect_fingers(image, hand_landmarks)
            
            # Send the list of 5 finger states as raw bytes directly to the Arduino
            arduino.write(bytes(fingers_state))  
            
            # Print state array to the local terminal for debugging console output
            print(f"Fingers State: {fingers_state}")

    # Display the processed video feed in a window named 'Hand Tracking'
    cv2.imshow('Hand Tracking', image)
    
    # Break the execution loop cleanly if the 'ESC' key (ASCII code 27) is pressed
    if cv2.waitKey(5) & 0xFF == 27:
        break

# =====================================================================
# CLEANUP
# =====================================================================
cap.release()           # Release the webcam resource
cv2.destroyAllWindows() # Properly close all open GUI windows
# ============================================================
# PYTHON FOR ROBOTICS
# PROJECT: HAND GESTURE CONTROLLED LEDs
#
# Python 3.14.7
# OpenCV
# MediaPipe Tasks API
# PySerial
# Arduino UNO
#
# MADE BY: SIR ANWAR SIRAJ
#          DS & AI ROBOTICS
# ============================================================


# ============================================================
# LIBRARY INSTALLATION
# ============================================================
#
# Open CMD and run:
#
# python -m pip install --upgrade pip
# python -m pip install opencv-python
# python -m pip install mediapipe
# python -m pip install pyserial
#
# IMPORTANT:
# We are NOT using:
#
# mp.solutions.hands
#
# This code uses the NEW:
#
# mp.tasks.vision.HandLandmarker
#
# ============================================================


# ============================================================
# IMPORT LIBRARIES
# ============================================================

import cv2
import mediapipe as mp
import serial
import time
import os


# ============================================================
# ARDUINO SETTINGS
# ============================================================

# Change this if your Arduino uses another COM port.
#
# Example:
# COM3
# COM4
# COM14

ARDUINO_PORT = "COM4"


# Arduino code must also use:
#
# Serial.begin(9600);

BAUD_RATE = 9600


# ============================================================
# MEDIAPIPE MODEL
# ============================================================

# The hand_landmarker.task file must be inside:
#
# models/hand_landmarker.task

MODEL_PATH = os.path.join(
    "models",
    "hand_landmarker.task"
)


# ============================================================
# CHECK MODEL FILE
# ============================================================

if not os.path.exists(MODEL_PATH):

    print()
    print("ERROR: MediaPipe model not found!")
    print()
    print("Required file:")
    print(MODEL_PATH)
    print()
    print("Please download hand_landmarker.task")
    print("and place it inside the models folder.")
    print()

    raise SystemExit


# ============================================================
# CONNECT ARDUINO
# ============================================================

try:

    arduino = serial.Serial(
        port=ARDUINO_PORT,
        baudrate=BAUD_RATE,
        timeout=1
    )

    print()
    print("Arduino connected successfully!")
    print("Port:", ARDUINO_PORT)
    print("Baud rate:", BAUD_RATE)
    print()


except serial.SerialException as e:

    print()
    print("ERROR: Arduino could not be connected.")
    print()
    print("Check:")
    print("1. Arduino USB cable")
    print("2. Arduino COM port")
    print("3. Arduino Serial Monitor is closed")
    print()
    print("Current COM port:", ARDUINO_PORT)
    print("Details:", e)

    raise SystemExit


# ============================================================
# WAIT FOR ARDUINO RESET
# ============================================================

# Arduino UNO normally resets when Serial opens.

time.sleep(2)


# ============================================================
# INITIALIZE MEDIAPIPE TASKS API
# ============================================================

# MediaPipe main module

mp_image = mp.Image


# MediaPipe image format

mp_image_format = mp.ImageFormat


# MediaPipe Tasks

BaseOptions = mp.tasks.BaseOptions


# MediaPipe Vision

VisionRunningMode = mp.tasks.vision.RunningMode


# Hand Landmarker

HandLandmarker = mp.tasks.vision.HandLandmarker


# Hand Landmarker Options

HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions


# ============================================================
# CREATE HAND LANDMARKER
# ============================================================

options = HandLandmarkerOptions(

    # Load hand_landmarker.task

    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),

    # We are processing one camera image at a time.

    running_mode=VisionRunningMode.IMAGE,

    # Detect maximum one hand.

    num_hands=1,

    # Detection confidence.

    min_hand_detection_confidence=0.7,

    # Hand presence confidence.

    min_hand_presence_confidence=0.7,

    # Tracking confidence.

    min_tracking_confidence=0.7
)


# Create detector

detector = HandLandmarker.create_from_options(
    options
)


print("MediaPipe Hand Landmarker initialized successfully!")


# ============================================================
# FINGER DETECTION FUNCTION
# ============================================================

def detect_fingers(hand_landmarks):

    # --------------------------------------------------------
    # MediaPipe landmark numbers
    #
    # Thumb tip  = 4
    # Index tip  = 8
    # Middle tip = 12
    # Ring tip   = 16
    # Pinky tip  = 20
    # --------------------------------------------------------

    finger_tips = [8, 12, 16, 20]

    thumb_tip = 4


    # Five fingers:
    #
    # [Thumb, Index, Middle, Ring, Pinky]

    finger_states = [
        0,
        0,
        0,
        0,
        0
    ]


    # ========================================================
    # THUMB
    # ========================================================

    if (
        hand_landmarks[thumb_tip].x
        <
        hand_landmarks[thumb_tip - 1].x
    ):

        finger_states[0] = 1


    # ========================================================
    # INDEX / MIDDLE / RING / PINKY
    # ========================================================

    for index, tip in enumerate(finger_tips):

        # Smaller Y means higher on image.

        if (
            hand_landmarks[tip].y
            <
            hand_landmarks[tip - 2].y
        ):

            finger_states[index + 1] = 1


    return finger_states


# ============================================================
# SEND DATA TO ARDUINO
# ============================================================

def send_to_arduino(finger_states):

    # Example:
    #
    # [1, 0, 1, 0, 1]
    #
    # Arduino receives five bytes:
    #
    # 01 00 01 00 01

    arduino.write(
        bytes(finger_states)
    )


# ============================================================
# DRAW HAND LANDMARKS
# ============================================================

# We manually draw the landmarks because
# we are using the new MediaPipe Tasks API.


# MediaPipe hand connections.

HAND_CONNECTIONS = [

    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),

    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),

    (5, 9),
    (9, 10),
    (10, 11),
    (11, 12),

    (9, 13),
    (13, 14),
    (14, 15),
    (15, 16),

    (13, 17),
    (17, 18),
    (18, 19),
    (19, 20),

    (0, 17)
]


def draw_hand(image, hand_landmarks):

    height, width, _ = image.shape


    # --------------------------------------------------------
    # Draw connections
    # --------------------------------------------------------

    for start, end in HAND_CONNECTIONS:

        x1 = int(
            hand_landmarks[start].x * width
        )

        y1 = int(
            hand_landmarks[start].y * height
        )

        x2 = int(
            hand_landmarks[end].x * width
        )

        y2 = int(
            hand_landmarks[end].y * height
        )


        cv2.line(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )


    # --------------------------------------------------------
    # Draw landmark points
    # --------------------------------------------------------

    for landmark in hand_landmarks:

        x = int(
            landmark.x * width
        )

        y = int(
            landmark.y * height
        )


        cv2.circle(
            image,
            (x, y),
            5,
            (0, 0, 255),
            -1
        )


# ============================================================
# START CAMERA
# ============================================================

cap = cv2.VideoCapture(0)


# ============================================================
# CAMERA CHECK
# ============================================================

if not cap.isOpened():

    print()
    print("ERROR: Camera could not be opened.")
    print()

    arduino.close()
    detector.close()

    raise SystemExit


# ============================================================
# PROJECT INFORMATION
# ============================================================

print()
print("================================================")
print("        PYTHON FOR ROBOTICS")
print("     HAND GESTURE LED CONTROL")
print("================================================")
print()
print("Python: 3.14.7")
print("Camera: OpenCV")
print("AI: MediaPipe Hand Landmarker")
print("Arduino:", ARDUINO_PORT)
print()
print("Thumb  -> LED Pin 8")
print("Index  -> LED Pin 9")
print("Middle -> LED Pin 10")
print("Ring   -> LED Pin 11")
print("Pinky  -> LED Pin 12")
print()
print("Press ESC to exit.")
print("================================================")
print()


# ============================================================
# MAIN LOOP
# ============================================================

try:

    while cap.isOpened():

        # ----------------------------------------------------
        # READ CAMERA
        # ----------------------------------------------------

        success, image = cap.read()


        if not success:

            print(
                "ERROR: Could not read camera frame."
            )

            break


        # ----------------------------------------------------
        # MIRROR CAMERA
        # ----------------------------------------------------

        image = cv2.flip(
            image,
            1
        )


        # ----------------------------------------------------
        # BGR -> RGB
        # ----------------------------------------------------

        rgb_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )


        # ----------------------------------------------------
        # CREATE MEDIAPIPE IMAGE
        # ----------------------------------------------------

        mp_frame = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_image
        )


        # ----------------------------------------------------
        # DETECT HAND
        # ----------------------------------------------------

        results = detector.detect(
            mp_frame
        )


        # ----------------------------------------------------
        # DEFAULT:
        # ALL LEDs OFF
        # ----------------------------------------------------

        fingers_state = [
            0,
            0,
            0,
            0,
            0
        ]


        # ====================================================
        # CHECK HAND
        # ====================================================

        if results.hand_landmarks:

            # First hand

            hand_landmarks = (
                results.hand_landmarks[0]
            )


            # ------------------------------------------------
            # DRAW HAND
            # ------------------------------------------------

            draw_hand(
                image,
                hand_landmarks
            )


            # ------------------------------------------------
            # DETECT FINGERS
            # ------------------------------------------------

            fingers_state = detect_fingers(
                hand_landmarks
            )


            # ------------------------------------------------
            # SEND TO ARDUINO
            # ------------------------------------------------

            send_to_arduino(
                fingers_state
            )


        else:

            # ------------------------------------------------
            # NO HAND
            #
            # Turn all LEDs OFF.
            # ------------------------------------------------

            send_to_arduino(
                [0, 0, 0, 0, 0]
            )


        # ====================================================
        # DISPLAY FINGER STATES
        # ====================================================

        text = (

            f"Thumb:{fingers_state[0]}  "

            f"Index:{fingers_state[1]}  "

            f"Middle:{fingers_state[2]}  "

            f"Ring:{fingers_state[3]}  "

            f"Pinky:{fingers_state[4]}"

        )


        cv2.putText(

            image,

            text,

            (10, 30),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (0, 255, 0),

            2

        )


        # ====================================================
        # PROJECT TITLE
        # ====================================================

        cv2.putText(

            image,

            "PYTHON FOR ROBOTICS",

            (10, 65),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (255, 0, 0),

            2

        )


        # ====================================================
        # SHOW CAMERA
        # ====================================================

        cv2.imshow(

            "Hand Gesture LED Control",

            image

        )


        # ====================================================
        # ESC = EXIT
        # ====================================================

        if (
            cv2.waitKey(5) & 0xFF
            == 27
        ):

            break


# ============================================================
# CLOSE EVERYTHING
# ============================================================

finally:

    print()
    print("Closing program...")


    # --------------------------------------------------------
    # Turn LEDs OFF
    # --------------------------------------------------------

    try:

        arduino.write(
            bytes([0, 0, 0, 0, 0])
        )

    except:

        pass


    # --------------------------------------------------------
    # Close camera
    # --------------------------------------------------------

    cap.release()


    # --------------------------------------------------------
    # Close OpenCV
    # --------------------------------------------------------

    cv2.destroyAllWindows()


    # --------------------------------------------------------
    # Close MediaPipe
    # --------------------------------------------------------

    detector.close()


    # --------------------------------------------------------
    # Close Arduino
    # --------------------------------------------------------

    arduino.close()


    print("Camera closed.")
    print("MediaPipe closed.")
    print("Arduino disconnected.")
    print("Program finished.")


# ============================================================
# PROJECT FLOW
# ============================================================
#
#             WEBCAM
#                |
#                v
#             OpenCV
#                |
#                v
#       MediaPipe Hand Landmarker
#                |
#                v
#        21 Hand Landmarks
#                |
#                v
#        Finger Detection
#                |
#                v
#             Python
#                |
#                | USB / Serial
#                v
#           Arduino UNO
#                |
#       +--------+--------+
#       |        |        |
#       v        v        v
#     LED 1    LED 2    LED 3
#     Pin 8    Pin 9    Pin 10
#
#       +--------+--------+
#       |        |
#       v        v
#     LED 4    LED 5
#     Pin 11   Pin 12
#
#
# ============================================================
# FINGER -> LED
# ============================================================
#
# Thumb  -> Pin 8
# Index  -> Pin 9
# Middle -> Pin 10
# Ring   -> Pin 11
# Pinky  -> Pin 12
#
#
# 1 = ON
# 0 = OFF
#
#
# Example:
#
# [1, 0, 1, 0, 1]
#
# Thumb  = ON
# Index  = OFF
# Middle = ON
# Ring   = OFF
# Pinky  = ON
#
# ============================================================
# MADE BY SIR ANWAR SIRAJ
# DS & AI ROBOTICS
# ============================================================

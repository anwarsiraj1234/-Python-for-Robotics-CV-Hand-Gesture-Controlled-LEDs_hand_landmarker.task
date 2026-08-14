import os
import mediapipe as mp

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "hand_landmarker.task"
)

print("Python MediaPipe test")
print("--------------------")

print("MediaPipe version:", mp.__version__)
print("Model path:", MODEL_PATH)
print("Model exists:", os.path.exists(MODEL_PATH))

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=RunningMode.IMAGE,
    num_hands=1
)

detector = HandLandmarker.create_from_options(options)

print("SUCCESS!")
print("MediaPipe Hand Landmarker is working.")

detector.close()

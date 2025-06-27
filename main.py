import cv2
import tkinter as tk
from PIL import Image, ImageTk
import mediapipe as mp
import time
import csv
from datetime import datetime

# FocusCam: A simple distraction detection app using OpenCV and MediaPipe
# GUI setup
window = tk.Tk()
window.title("FocusCam 😌✨")
video_label = tk.Label(window)
video_label.pack()

cap = cv2.VideoCapture(0)

# Face Mesh setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)  # enable iris
mp_drawing = mp.solutions.drawing_utils

# Logging
log_file = "distraction_log.csv"
with open(log_file, mode="a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Distraction"])

distraction_timer = None
is_distracted = False

def log_distraction():
    with open(log_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, "No face or eyes detected"])

def update_frame():
    global distraction_timer, is_distracted

    ret, frame = cap.read()
    if not ret:
        return

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    face_detected = False
    eyes_detected = False

    if results.multi_face_landmarks:
        face_detected = True
        for face_landmarks in results.multi_face_landmarks:
            # Draw facial landmarks
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=1),
            )

            # Check eyes: landmark 145 (left) & 374 (right)
            left_eye = face_landmarks.landmark[145]
            right_eye = face_landmarks.landmark[374]

            if left_eye.visibility > 0.5 and right_eye.visibility > 0.5:
                eyes_detected = True

    # Distraction logic
    if face_detected and not eyes_detected:
        if distraction_timer is None:
            distraction_timer = time.time()
        elif time.time() - distraction_timer > 2 and not is_distracted:
            log_distraction()
            is_distracted = True
    else:
        distraction_timer = None
        is_distracted = False

    # Convert for Tkinter display
    img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    video_label.config(image=img)
    video_label.image = img
    window.after(10, update_frame)

update_frame()
window.mainloop()
cap.release()

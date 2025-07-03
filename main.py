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

status_label = tk.Label(window, text="Status: Not Running", font=("Times", 12), fg="blue")
status_label.pack()
button_frame = tk.Frame(window)
button_frame.pack(pady=50)

start_button = tk.Button(button_frame, text="Start Detection", bg="green", fg="white")
start_button.grid(row=0, column=0, padx=5)

stop_button = tk.Button(button_frame, text="Stop Detection", bg="orange", fg="white")
stop_button.grid(row=0, column=1, padx=5)

exit_button = tk.Button(button_frame, text="Exit", bg="red", fg="white")
exit_button.grid(row=0, column=2, padx=5)

def blink_label(color1="orange", color2="yellow", delay=300):
    current_color = status_label.cget("fg")
    new_color = color2 if current_color == color1 else color1
    status_label.config(fg=new_color)
    if running:
        window.after(delay, lambda: blink_label(color1, color2, delay))

# Video capture setup
cap = cv2.VideoCapture(0)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

# Logging
log_file = "distraction_log.csv"
with open(log_file, mode="a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Distraction"])

# Initialize variables
distraction_timer = None
is_distracted = False   
running = False

def log_distraction():
    with open(log_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, "No face or eyes detected"])

def update_frame():
    global distraction_timer, is_distracted
    
    if not running:
        window.after(10, update_frame)
        return

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
        status_label.config(text="Status: Distraction Detected", fg="orange")
        blink_label()
        if distraction_timer is None:
            distraction_timer = time.time()
        elif time.time() - distraction_timer > 2 and not is_distracted:
            log_distraction()
            is_distracted = True
    elif face_detected and eyes_detected:
        status_label.config(text="Status: Focused", fg="green")
        distraction_timer = None
        is_distracted = False
    else:
       status_label.config(text="Status: No Face Detected", fg="red")   
       distraction_timer = None
       is_distracted = False

    # Convert for Tkinter display
    img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    video_label.config(image=img)
    video_label.image = img
    window.after(10, update_frame)

#Button functionality
def start_detection():
    global running
    running = True
    status_label.config(text="Status: Starting...", fg="blue")
def stop_detection():
    global running
    running = False
    status_label.config(text="Status: Detection stopped", fg="gray")
def exit_app():
    cap.release()
    window.destroy()
    
# Bind buttons to functions
start_button.config(command=start_detection)
stop_button.config(command=stop_detection)
exit_button.config(command=exit_app)
 
update_frame()
window.mainloop()
cap.release()

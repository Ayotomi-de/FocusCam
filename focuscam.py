import cv2 as cv
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
import mediapipe as mp
import csv
import time
from datetime import datetime

# FocusCam: A simple distraction detection app using OpenCV and MediaPipe
# GUI setup
class FocusCamApp:
    def __init__(self):
        # Set up everything that used to be at the top
        self.window = tk.Tk()
        self.window.title("FocusCam 😌✨")
        
        # Video Feed Label
        self.video_label = tk.Label(self.window)
        self.video_label.pack()
        
        # Status Label
        self.status_label = tk.Label(self.window, text="Status: Not Running", font=("Times", 12), fg="blue")
        self.status_label.pack()
        
        # Button Frame
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=50)

        # Start, Stop, and Exit Buttons
        self.start_button = tk.Button(button_frame, text="Start Detection", bg="green", fg="white", command=self.start_detection)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = tk.Button(button_frame, text="Stop Detection", bg="orange", fg="white", command=self.stop_detection)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.exit_button = tk.Button(button_frame, text="Exit", bg="red", fg="white", command=self.exit_app)
        self.exit_button.grid(row=0, column=2, padx=5)

        # Camera setup
        self.cap = cv.VideoCapture(0)
        
        mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
        self.mp_face_mesh = mp_face_mesh
        self.mp_drawing = mp.solutions.drawing_utils

        # Logging
        self.log_file = "distraction_log.csv"
        with open(self.log_file, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Distraction"])

        # State variables
        self.distraction_timer = None
        self.is_distracted = False
        self.running = False

        # Start the camera loop
        self.update_frame()
        self.window.mainloop()
        
    def show_distraction_alert(self, message="You seem distracted! Please refocus."):
        messagebox.showwarning("Distraction Alert 🚨", message)

    def update_frame(self):
     if not self.running:
        self.window.after(10, self.update_frame)
        return

     ret, frame = self.cap.read()
     if not ret:
        print("Failed to grab frame")
        self.window.after(10, self.update_frame)
        return

     # Convert frame to RGB for MediaPipe processing
     frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
     results = self.face_mesh.process(frame_rgb)

     face_detected = False
     eyes_detected = False

     if results.multi_face_landmarks:
         face_detected = True
         for face_landmarks in results.multi_face_landmarks:
            # Draw facial landmarks
            self.mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
            )

            if self.is_eyes_open(face_landmarks):
                eyes_detected = True

     # Handle distraction check
     self.handle_distraction_status(face_detected, eyes_detected)

     # Convert the frame back to ImageTk for Tkinter
     img = ImageTk.PhotoImage(Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB)))
     self.video_label.config(image=img)
     self.video_label.image = img  # prevent garbage collection of image

     # Call update_frame() again after 10 ms
     self.window.after(10, self.update_frame)


    # Distraction logic
    def handle_distraction_status(self, face_detected, eyes_detected):
     if face_detected and not eyes_detected:
         self.status_label.config(text="Status: Distraction Detected (Eyes Closed)", fg="orange")
         if self.distraction_timer is None:
            self.distraction_timer = time.time()
         elif time.time() - self.distraction_timer > 2 and not self.is_distracted:
            self.log_event("Eyes closed for more than 2 seconds")
            self.show_distraction_alert("Eyes closed for too long!")
            self.is_distracted = True

     elif face_detected and eyes_detected:
        self.status_label.config(text="Status: Focused", fg="green")
        self.distraction_timer = None
        self.is_distracted = False

     else:
        self.status_label.config(text="Status: No Face Detected", fg="red")
        if self.distraction_timer is None:
            self.distraction_timer = time.time()
        elif time.time() - self.distraction_timer > 2 and not self.is_distracted:
            self.log_event("No face detected for more than 2 seconds")
            self.is_distracted = True

    #Logs distractions to a CSV file 
    def log_event(self, message):
     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     with open(self.log_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, message])

   
    # Check if eyes are open based on the x and y coordinates of the eyelid landmarks
    def is_eyes_open(self, face_landmarks):
     # Get the y-coordinates of eyelid landmarks
     #(Top eyelid = 159 and bottom eyelid = 145) & right (top eyelid = 386 and bottom eyelid = 374)
     left_eye_openness = abs(face_landmarks.landmark[159].y - face_landmarks.landmark[145].y)
     right_eye_openness = abs(face_landmarks.landmark[386].y - face_landmarks.landmark[374].y)

     # You can later adjust the 0.015 threshold if needed
     if left_eye_openness > 0.015 and right_eye_openness > 0.015:
         return True
     return False

    #Start button - Enables frame detection
    def start_detection(self):
       self.running = True
       self.status_label.config(text="Status: Starting...", fg="blue")
    
    #Stop button - Stops frame detection
    def stop_detection(self):
       self.running = False
       self.status_label.config(text="Status: Detection stopped", fg="gray")

    #Exit button - Releases webcam and closes the application
    def exit_app(self):
       self.cap.release()
       self.window.destroy()

if __name__ == "__main__":
    FocusCamApp()
# This is the main entry point for the FocusCam application
# It initializes the FocusCamApp class, which sets up the GUI and starts the camera feed
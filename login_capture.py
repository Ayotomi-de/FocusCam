import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import cv2 as cv
import os
import mysql.connector

# Database connection settings and image saving logic
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "focuscam",
    "charset": "utf8mb4"
}

def save_face_image(username, frame):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IMAGE_FOLDER = os.path.join(BASE_DIR, "face_images")
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    user_folder = os.path.join(IMAGE_FOLDER, username)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    image_count = len(os.listdir(user_folder))
    image_path = os.path.join(user_folder, f"{image_count + 1}.jpg")
    cv.imwrite(image_path, frame)
    return image_path

# Save the username and image path to the database
def save_user_to_db(username, image_path):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "INSERT INTO users (username, image_path) VALUES (%s, %s)"
        cursor.execute(query, (username, image_path))
        conn.commit()
    except Exception as e:
        print(f"Error saving user: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# Login + Face capture flow
def gui_login_capture(root):
    username = simpledialog.askstring("Login", "Enter your username:", parent=root)
    if not username:
        messagebox.showwarning("Login Cancelled", "Username cannot be empty.")
        return None
    
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Could not open camera.")
        return None
    
    login_window = tk.Toplevel(root)
    login_window.title("Capture Your Face")
    video_label = tk.Label(login_window)
    video_label.pack()
    
    
    def update_frame():
        ret, frame = cap.read()
        if ret:
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
        video_label.after(10, update_frame)
          
    def capture_image():
        ret, frame = cap.read()
        if ret:
            image_path = save_face_image(username, frame)
            save_user_to_db(username, image_path)
            messagebox.showinfo("Success", f"Image saved and user '{username}' registered.")
            cap.release()
            login_window.destroy()
    capture_btn = tk.Button(login_window, text="Capture", command=capture_image)
    capture_btn.pack(pady=10)

    update_frame()

# Clean missing DB entries
def clean_missing_images():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, image_path FROM users")
    users = cursor.fetchall()

    for user_id, username, path in users:
        if not os.path.exists(path):
            print(f"Image missing for {username}, deleting from DB...")
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
    conn.commit()
    cursor.close()
    conn.close()
    print("Cleanup done.")


def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main root window
    clean_missing_images()
    gui_login_capture(root)
    root.mainloop()

if __name__ == "__main__":
    main()
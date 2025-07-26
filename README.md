# 🎯 FocusCam: Distraction Detection App 😌✨

FocusCam is a lightweight desktop app that uses your webcam to track focus by detecting facial landmarks and eye visibility. Built with **OpenCV**, **MediaPipe**, and **Tkinter**, it’s your mini assistant to know when you're not paying attention. 😉

---

## Features

- Real-time face & eye detection using MediaPipe FaceMesh.
- Logs moments of distraction to a CSV file.
- Simple and clean GUI using Tkinter.
- Real-time video display using your webcam.
- Beginner-friendly codebase to learn from.
- Designed with students and focus-lovers in mind.

---

## 🧠 What I’m Learning

This is my first full solo computer vision project after lots of tutorials!  
I'm learning to:
- Use GUI frameworks (like Tkinter)
- Integrate MediaPipe for face & eye tracking
- Build real-time applications
- Handle logic for motion/distraction detection
- Log events to external files
- Debug Python library issues
- Save photos to database.

---

## 💻 Tech Stack

- Python 
- OpenCV
- MediaPipe
- Tkinter
- PIL (Pillow)
- CSV Logging
- MySQL

---

## 🛠️ How to Run

1. Clone this repo  
   `git clone https://github.com/<your-username>/FocusCam.git`

2. Install dependencies  
   `pip install opencv-python mediapipe Pillow`

3. Run the app  
   `python focuscam.py`

---

| Error                                  | Fix                                                          |
| -------------------------------------- | ------------------------------------------------------------ |
| ❌ `OSError: could not get source code` | MediaPipe doesn’t support Python 3.12 — I downgraded to 3.10 |
| ❌ Haarcascade not detecting eyes       | Switched to MediaPipe FaceMesh for better accuracy           |


## 📂 Project Files

- `focuscam.py` – Main app file
- `distraction_log.csv` – Log file for distractions
- `README.md` – This doc
- `haarcascade_frontalface_default.xml` – (Optional backup if you use it)
- `haarcascade_eye.xml`
- `database.py` - Mysql database connection code
- `test_db_connection` - To test if Mysql runs smoothly
- `focuscam.sql` - The SQL query of the Mysql databse which I created in phpMyAdmin using XAMPP.
- `banner.png` - (Coming soon: project thumbnail!)

---

## Planned Improvements
- [x] Real-time face detection using FaceMesh
- [x] Distraction logging to CSV
- [x] Start/Stop detection button
- [x] Clean exit button
- [x] Saving users faces and username in a Mysql database
- [x] Storing users info in a Mysql 
- [x] Notification system (e.g. sound or pop-up)
- [ ] Face recognition
- [ ] Export logs as summary report (particluarly as pdf files)

---

## Planned Updates and Upcoming Changes
After some deep thinking, i've decided to change focuscam to something else that can be implemented in the real-word usage, it can be a whole different logic or maybe a web app, who knows? However, I'll continue working on the logic of focuscam so stay tunded 😉.
 
---

## 🤝 Let's Connect

👩🏽‍💻 About Me
Hi, I’m **Ayotomide** — a passionate learner, tech enthusiast, and now a proud builder of FocusCam!
This project is part of my journey into computer vision and software engineering.

Got ideas? Want to contribute or learn together? Let’s connect:

📧 [My email](ayotomide.toluwani@gmail.com) 
🐦 [Ayotomide Ogunsami](www.linkedin.com/in/ayotomide-ogunsami-93aa61312)

---

> “Focus is the key to finishing. Let your camera catch what your brain might miss.”

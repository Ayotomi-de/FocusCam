# 🎯 FocusCam: Distraction Detection App 😌✨

FocusCam is a lightweight desktop app that uses your webcam to track focus by detecting facial landmarks and eye visibility. Built with **OpenCV**, **MediaPipe**, and **Tkinter**, it’s your mini assistant to know when you're not paying attention. 😉

---

## 📸 Features

- ✅ Real-time face & eye detection using MediaPipe FaceMesh
- ✅ Logs moments of distraction to a CSV file
- ✅ Simple and clean GUI using Tkinter
- ✅ Real-time video display using your webcam
- ✅ Beginner-friendly codebase to learn from
- ✅ Designed with students and focus-lovers in mind 😄

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

---

## 💻 Tech Stack

- Python 
- OpenCV
- MediaPipe
- Tkinter
- PIL (Pillow)
- CSV Logging

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
- `banner.png` - (Coming soon: project thumbnail!)

---

## Planned Improvements
- [x] Real-time detection using FaceMesh
- [x] Distraction logging to CSV
- [ ] Start/Stop detection button
- [ ] Clean exit button
- [ ] Notification system (e.g. sound or pop-up)
<!-- - [ ]Screenshot capture when distraction is logged -->
- [ ]Export logs as summary report

---

## 🤝 Let's Connect

👩🏽‍💻 About Me
Hi, I’m **Ayotomide** — a passionate learner, tech enthusiast, and now a proud builder of FocusCam!
This project is part of my journey into computer vision and software engineering.

Got ideas? Want to contribute or learn together? Let’s connect:

📧 [ayotomide.toluwani@gmail.com]  
🐦 [www.linkedin.com/in/ayotomide-ogunsami-93aa61312]

---

> “Focus is the key to finishing. Let your camera catch what your brain might miss.”

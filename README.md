# A-graphical-user-interface-for-controlling-the-Tello-drone

# Tello Drone Control GUI

This project implements a graphical user interface (GUI) for controlling
the Tello drone.

The GUI allows the user to easily operate the drone, monitor flight data,
capture media, and perform object detection for agricultural applications.

---

## 🎮 GUI Functions

The graphical user interface provides the following features:

- Drone control:
  - Takeoff and landing
  - Movement up, down, left, right, forward, and backward
- Manual flight execution through on-screen controls
- Automated flight path creation and execution
- Photo capture
- Video recording
- Live video stream from the drone’s camera
- Display of flight information:
  - speed
  - altitude
  - total flight time
- Object detection:
  - Lemon recognition using a trained YOLO model
 
---

## 🍋 Lemon Detection

The GUI includes a lemon detection function based on a YOLO object detection
model trained using:
Dataset from the platform Roboflow
The code used for training in Google colab is contained in this file google_colab.py

The trained model (best.pt) is loaded directly by the GUI and used during flight.

---

## 📂 Required Files

For the program to work correctly, the following files must be placed in
the same folder:

Final_program.py   # Main GUI and drone control program
best.pt            # Trained YOLO model
tello-drone.png    # Image displayed in the GUI

!!! All comments in the program are written in Greek.


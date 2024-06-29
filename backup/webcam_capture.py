# webcam_capture.py
import cv2 as cv
import time

def get_webcam_frame():
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream from webcam.")
        return None

    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image from webcam.")
        return None

    return cap, frame

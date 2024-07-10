import cv2
import time
import serial
from ultralytics import YOLO

# Initialize serial communication with Arduino
#arduino = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino's port

# Load the pre-trained YOLOv8 model
model = YOLO('yolov8n.pt')

# List of vehicle types to detect
vehicle_classes = ['car', 'truck', 'bus', 'motorbike', 'ambulance']

# Access the webcam
cap = cv2.VideoCapture(0)

# Initialize traffic light states and timer
left_green = True
right_green = False
last_switch_time = time.time()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Get the width of the frame
    frame_width = frame.shape[1]
    mid_x = frame_width // 2

    # Initialize counters
    left_count = 0
    right_count = 0
    left_priority = False
    right_priority = False

    from inference_sdk import InferenceHTTPClient

    CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="Qx9xrX1X9K1zcyTUxl6b"
)

    results = CLIENT.infer(your_image.jpg, model_id="ambulancedetection-4vwg4/1")
    # Run object detection
    results = model(frame)

    for result in results:
        boxes = result.boxes
        classes = result.names

        for box in boxes:
            class_id = int(box.cls[0])
            class_name = classes[class_id].lower()

            if class_name in vehicle_classes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                center_x = (x1 + x2) // 2

                if center_x < mid_x:
                    left_count += 1
                    if class_name == 'ambulance' or class_name in ['truck', 'bus']:
                        left_priority = True
                else:
                    right_count += 1
                    if class_name == 'ambulance' or class_name in ['truck', 'bus']:
                        right_priority = True

                # Draw bounding box and label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Check if 100 seconds have passed since the last switch
    current_time = time.time()
    if current_time - last_switch_time > 100:
        left_green = not left_green
        right_green = not right_green
        last_switch_time = current_time

    # Give priority to streets with detected ambulances or large vehicles
    if left_priority and not left_green:
        left_green = True
        right_green = False
        last_switch_time = current_time
    elif right_priority and not right_green:
        right_green = True
        left_green = False
        last_switch_time = current_time
    elif left_count > right_count and not left_green:
        left_green = True
        right_green = False
        last_switch_time = current_time
    elif right_count > left_count and not right_green:
        right_green = True
        left_green = False
        last_switch_time = current_time

    # Send signal to Arduino
    if left_green:
       # arduino.write(b'L')
        print("left street green")
    else:
        #arduino.write(b'R')
        print("right street green")

    # Display counts and light status
    cv2.putText(frame, f'Left: {left_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.putText(frame, f'Right: {right_count}', (mid_x + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.putText(frame, 'Left Green' if left_green else 'Left Red', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0) if left_green else (0, 0, 255), 2)
    cv2.putText(frame, 'Right Green' if right_green else 'Right Red', (mid_x + 10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0) if right_green else (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Webcam - YOLOv8 Object Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
#arduino.close()

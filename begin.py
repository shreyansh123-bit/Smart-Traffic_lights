import os
os.system('cls')
print("setting up systems...")
import serial
ser = serial.Serial('COM6', 9600)
import datetime as dt
import cv2
from ultralytics import YOLO


#best_hist provides best results
model = YOLO('best_hist.pt')

print("accessing video footge..\n")
# Open a connection to the camera
cap = cv2.VideoCapture(1)  # 0 is the default camera

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

ret,frame=cap.read()
if not ret:
    print("could not read frame")
    cap.release()
    cap.exit()

height, width, _ = frame.shape

os.system('cls')
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    # initialize variables
    emergency_right=0
    emergency_left=0
    left_vehicles=0
    right_vehicles=0   
    center_x = width // 2
    now=dt.datetime.now()

    # Perform detection
    results = model.predict(source=frame, conf=0.1)  # Adjust `conf` as needed    
    
    
    # Loop through the detected objects
    for result in results:
        for box in result.boxes:
            cls = int(box.cls)  # class id
            x1, y1, x2, y2 = box.xyxy[0].tolist()  # bounding box coordinates
            confidence = box.conf.tolist()  # confidence score

            # Calculate center coordinates
            obj_center_x = (x1 + x2) // 2
            obj_center_y = (y1 + y2) // 2

            if obj_center_x > center_x:
                right_vehicles += 1
                if cls == 1:
                    emergency_right +=1
            elif obj_center_x <= center_x:
                left_vehicles += 1
                if cls == 1:
                    emergency_left +=1

            if emergency_left>emergency_right:
                print("left green")
            elif emergency_right>left_vehicles:
                print("right green")
            elif right_vehicles > left_vehicles:
                print("right green")
            else:
                print("left green")

           
            cv2.putText(frame, str(now), (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)           
            #cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 20), 1)            
            cv2.putText(frame, f"{model.names[cls]}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)       
            cv2.circle(frame, (int(obj_center_x), int(obj_center_y)), 5, (255,0,0), -1)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Press 'q' to exit the video stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
ser.close()
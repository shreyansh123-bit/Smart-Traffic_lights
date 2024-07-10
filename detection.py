print("loading packages.....\n\n")
import cv2
import numpy as np
from send import sendbit
# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()

output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load COCO class names
with open("coco.names", "r") as f:
    classes = f.read().strip().split("\n")

# Define vehicle classes (assuming "car", "bus", "truck" are in the COCO dataset)
vehicle_classes = {"car", "bus", "truck","motorbike","bicycle"}
req_conf=.05
font = cv2.FONT_HERSHEY_SIMPLEX


print("\n accessing camera footage....")
# Open the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
   

    if not ret:
        print("Failed to capture frame")
        break

    height, width, channels = frame.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Initialize lists to hold detection data
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence >= req_conf:
                class_name = classes[class_id]
                if class_name in vehicle_classes:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

    # Apply Non-Maximum Suppression
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)

    # Initialize counters for the current frame
    left_street = 0
    right_street = 0
    truck_on_right = None
    truck_on_left = None

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            class_name = classes[class_ids[i]]
            center_x = x + w // 2

            # Determine if the vehicle is on the left or right side of the frame
            if center_x < width / 2:
                left_street += 1
                if class_name == "truck" or class_name == "bus":
                    truck_on_left = True
            else:
                right_street += 1
                if class_name == "truck" or class_name == "bus":
                    truck_on_right = True

            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 255, 0), thickness= 1)
            cv2.putText(frame, class_name, (x, y - 10), font , 0.6, (0,255,255), 2)
           
            
            

    # Display the frame with detected vehicles
    cv2.imshow("Frame", frame)

    # Print the number of vehicles detected on the left and right streets
    print(f"Left street vehicle count: {left_street}")
    print(f"Right street vehicle count: {right_street}")

    if truck_on_left:
        print("truck/ambulance on left lane")
        sendbit(0)  #left=green
    if truck_on_right:
        sendbit(1)  #right=green
        print("truck/ambulance on right lane")
    if left_street > right_street:
        sendbit(0) #left=green

    if  right_street > left_street:
        sendbit(1)  #right=green
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

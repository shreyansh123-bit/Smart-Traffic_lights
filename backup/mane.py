import cv2 as cv
import numpy as np
from backup.webcam_capture import get_webcam_frame

print("Completed loading packages")

# Load YOLO
yolo = cv.dnn.readNet(".venv\yolov3.weights", ".venv\yolov3.cfg")

# Grabbing data from coco.names
classes = []
with open("coco.names", "r") as file:
    classes = [line.strip() for line in file.readlines()]

# Get layer names and output layers
layer_names = yolo.getLayerNames()
output_layers = [layer_names[i - 1] for i in yolo.getUnconnectedOutLayers()]

Red = (255, 0, 0)
Green = (0, 255, 0)

# Initialize webcam
cap, img = get_webcam_frame()

if cap is None or img is None:
    exit()

while True:
    ret, img = cap.read()
    if not ret:
        print("Error: Failed to capture image from webcam.")
        break

    height, width, channels = img.shape

    # Detecting objects
    blob = cv.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    yolo.setInput(blob)
    outputs = yolo.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.3:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)

                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - (w / 2))
                y = int(center_y - (h / 2))

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply non-max suppression
    indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in indexes:
        i = i[0]  # Extract the index from the tuple
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        cv.rectangle(img, (x, y), (x + w, y + h), Green, 3)
        cv.putText(img, label, (x, y + 30), cv.FONT_HERSHEY_PLAIN, 2, Red, 2)  # Adjust font scale and thickness

    # Display the image
    cv.imshow("Webcam", img)

    # Break the loop if 'q' key is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv.destroyAllWindows()

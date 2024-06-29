
#import ultralytics
#ultralytics.checks()
import cv2 as cv
import numpy as np

# Load YOLO model weights and configuration
yolo = cv.dnn.readNet(".venv/yolov3.weights", ".venv/yolov3.cfg")

# Load object classes from coco.names
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Get output layer names
layer_names = yolo.getLayerNames()
output_layers = [layer_names[i - 1] for i in yolo.getUnconnectedOutLayers()]

# Define colors for bounding boxes and labels
colors = [(255, 0, 0), (0, 255, 0),(55,35,200),(66,83,0)]  # Red and Green

# Initialize video capture object from webcam (index 0)
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Error: Failed to open webcam.")
    cap.release()
    cv.destroyAllWindows()
    exit(1)  # Exit the script if the webcam cannot be opened

while True:
    # Capture frame-by-frame   
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture frame from webcam")
        break

    frame = cv.resize(frame, (320, 320))

    # Create a blob from the frame
    blob = cv.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    # Set the input to the network
    yolo.setInput(blob)

    # Forward propagation to get outputs
    outputs = yolo.forward(output_layers)

    # Initialize lists for object detection results
    class_ids = []
    confidences = []
    boxes = []
    objects_identified = []

    # Process each output layer
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.3:
                center_x = int(detection[0] * frame.shape[1])  # Width
                center_y = int(detection[1] * frame.shape[0])  # Height
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])

                x = int(center_x - (w / 2))
                y = int(center_y - (h / 2))

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-Maximum Suppression (NMS)
    indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw bounding boxes and labels on detected objects
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i] % len(colors)]  # Cycle through colors

            cv.rectangle(frame, (x, y), (x + w, y + h), color, 3)
            cv.putText(frame, label, (x + 10, y + 15), cv.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            objects_identified.append(label)
            
          
    # Display the resulting frame
    cv.imshow("Object Detection", frame)

    # Print the list of identified objects for the current frame
    print("Objects identified:", objects_identified)
    
    # Quit if 'q' key is pressed
    if cv.waitKey(1) == ord("q"):
        break

# Release resources
cap.release()
cv.destroyAllWindows()

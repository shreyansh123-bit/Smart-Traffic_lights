#import packages
print("loading packages..")

import cv2 as cv
import time
import numpy as np
#from webcam_capture import frame

print("completed loading packages")

yolo=cv.dnn.readNet(".venv\yolov3.weights",".venv\yolov3.cfg")

#grabbing data from coco.names
classes =[] 
with open ("coco.names","r")as file:
    classes = [line.strip()for line in file.readlines()]

#something something yolo
layer_names = yolo.getLayerNames()
output_layers = [layer_names[i - 1] for i in yolo.getUnconnectedOutLayers()]

Red=(255,0,0)
Green=(0,255,0)

name="images\cat1.jpeg"
img=cv.imread(name)
height ,width ,channels = img.shape

#detecting objects
blob = cv.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

yolo.setInput(blob)
outputs = yolo.forward(output_layers)

class_ids =[]
confidences=[]
boxes=[]

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

            boxes.append([x, y, w, h])  #predefined array
            confidences.append(float(confidence))
            class_ids.append(class_id)


indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        cv.rectangle(img, (x, y), (x + w, y + h), Green, 3)
        cv.putText(img, label, (x, y + 10), cv.FONT_HERSHEY_PLAIN, 8, Red, 8)

cv.imshow("image",img)
cv.waitKey(0)
cv.destroyAllWindows()
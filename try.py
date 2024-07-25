import cv2
frame=cv2.VideoCapture("test_vids/testvid5.mp4")
while True:

    ret,img = frame.read()
    height, width, _ = img.shape
    cv2.resize(img,(385,405))
    cv2.imshow("resized frame",img)
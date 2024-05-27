import os

import cv2

# Variables
width, height = 1280, 720
folderPath = "Presentation"

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Get the list of presentation images
pathImages = os.listdir(folderPath)
print(pathImages)

while True:
    success, img = cap.read()
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key & 0xFF == ord("q"):
        break
import os
import cv2
from cvzone.HandTrackingModule import HandDetector

# Variables
width, height = 1280, 720
folderPath = "Presentation"

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Variables
imgNumber = 0
hs, ws = int(120*3), int(213*3)

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Get the list of presentation images in sorted manner.
pngFiles = [file for file in os.listdir(folderPath) if file.endswith('.png')]
pathImages = sorted(pngFiles)
# print(pathImages)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)

    if hands :
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        print(fingers)
    # Adding webcam images on slides
    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws:w] = imgSmall

    cv2.imshow('Image', img)
    cv2.imshow('Slides', imgCurrent)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
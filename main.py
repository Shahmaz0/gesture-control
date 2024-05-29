import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# Variables
width, height = 1280, 720
folderPath = "Presentation"

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Get the list of presentation images
pathImages = sorted(os.listdir(folderPath))
print(pathImages)

# Variables
imgNumber = 0
hs, ws = int(120 * 2.5), int(213 * 2.5)
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 10

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    # Import Images
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand["center"]
        lmList = hand["lmList"]

        # Constraint values for easier drawing
        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold:  # if hand is at height of the face

            # Gesture 1 - Left
            if fingers == [1, 0, 0, 0, 0]:
                print("left")
                if imgNumber > 0:
                    buttonPressed = True
                    imgNumber = imgNumber - 1

            # Gesture 2 - right
            if fingers == [0, 0, 0, 0, 1]:
                print("left")
                if imgNumber < len(pathImages) - 1:
                    buttonPressed = True
                    imgNumber = imgNumber + 1

        # Gesture 3 - Show Pointer
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

    # Button Pressed iterations
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    # Adding webcam images on the slides
    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws:w] = imgSmall

    cv2.imshow("Image", img)
    cv2.imshow("slides", imgCurrent)

    key = cv2.waitKey(1)
    if key & 0xFF == ord("q"):
        break

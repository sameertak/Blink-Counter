import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
plotY= LivePlot(640,360,[20,50], invert=True)
idList = [22,23,24,26,110,157,158,159,160,161,130,243]
ratioList = []
blinkCounter = 0
counter = 0
color = (255,0,0)
while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 2, color, cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lengthVer, _ = detector.findDistance(leftUp,leftDown)
        lengthHor, _ = detector.findDistance(leftLeft,leftRight)

        cv2.line(img, leftUp, leftDown, color, 2)
        cv2.line(img, leftLeft, leftRight, color, 2)

        ratio = (lengthVer/ lengthHor)*100
        ratioList.append(ratio)
        if len(ratioList)>3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList)/len(ratioList)

        if ratioAvg<30 and counter == 0:
            blinkCounter += 1
            color = (255,0,0)
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 5:
                counter = 0
                color = (0,255,0)

        cvzone.putTextRect(img,f'Blink Count: {blinkCounter}', (100,100),colorR=color)
        imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img,imgPlot],2,1)
    else:
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, img], 2, 1)

    cv2.imshow("Image", imgStack)
    cv2.waitKey(24)

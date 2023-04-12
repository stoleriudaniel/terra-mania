import cv2.data
import mediapipe as mp
import time


class HandDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.detectionCon,
                                        self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.handClosed = False

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if (draw):
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        if len(lmList) > 0:
            x, y = lmList[9][1], lmList[9][2]

            x1, y1 = lmList[12][1], lmList[12][2]

            if y1 > y:
                self.handClosed = True
            else:
                self.handClosed = False
        return lmList

    def isHandClosed(self):
        return self.handClosed

    def getCoords(self, img):
        img = self.findHands(img)
        lmList = self.findPosition(img)
        if len(lmList) != 0:
            return lmList[9][1], lmList[9][2]

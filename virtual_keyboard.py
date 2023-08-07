import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8)
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",":"],
        ["Z","X","C","V","B","N","M",",",".","/"]]
finalText = ""
keyboard = Controller()   



# def drawAll(img,buttonList):  #without transparency
#     for button in buttonList:
#         x,y = button.pos
#         w,h = button.size
#         cv2.rectangle(img, button.pos,(x + w, y + h), (255,0,255),cv2.FILLED)
#         cv2.putText(img,button.text,(x + 20, y + 65), 
#                    cv2.FONT_HERSHEY_PLAIN, 4,(255,255,255),4)
    
#     return img

def drawAll(img, buttonList): #with transparency
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                      (255, 0, 255), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 40, y + 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

    out = img.copy()
    alpha = 0.5 #changeable
    mask = imgNew.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out

class Button():
    def __init__(self,pos, text, size =[85,85]):
        self.pos = pos
        self.text = text
        self.size = size
        
        
    
buttonList = []
for i in range (len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(Button([100 * j + 50,100 * i + 50],key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbobxInfo = detector.findPosition(img) 
    # if hands:
    #     #Hand1
    #     hand1 = hands[0]
    #     lmList1 = hand1["lmList"] #21 Landmark points
    #     bbox1 = hand1["bbox"] # Bounding box info x,y,w,h
    #     centerPoint1 = hand1['center'] #center of the hand cx, cy
    #     handType1 = hand1["type"] #left hand or right hand
        
    #     fingers1 = detector.fingersUp(hand1)
        
    #     if len(hands) == 2:
    #         hand2 = hands[1]
    #         lmList2 = hand2["lmList"] 
    #         bbox2 = hand2["bbox"]
    #         centerPoint2 = hand2['center']
    #         handType2 = hand2['type']
            
    #         fingers2 = detector.fingersUp(hand2)
            
    #         length, info, img = detector.findDistance(lmList1[8], lmList2[8], img) # type: ignore
            
        
    img = drawAll(img,buttonList)
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
                
            if x < lmList[8][0] <x+w and y< lmList[8][1] < y+h:
                cv2.rectangle(img, button.pos,(x + w, y + h), (175,0,175),cv2.FILLED)
                cv2.putText(img,button.text,(x + 20, y + 65), 
                            cv2.FONT_HERSHEY_PLAIN, 4,(255,255,255),4)
                l, _, _ = detector.findDistance(8, 12, img, draw=False) # type: ignore
                #print (l)
                
                if l < 40:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos,(x + w, y + h), (0,255,0),cv2.FILLED)
                    cv2.putText(img,button.text,(x + 20, y + 65), 
                            cv2.FONT_HERSHEY_PLAIN, 4,(255,255,255),4)
                    finalText += button.text
                    sleep(0.20)
                    
    cv2.rectangle(img, (50,350),(700,450), (175,0,175),cv2.FILLED)
    cv2.putText(img,finalText,(60, 430), 
                cv2.FONT_HERSHEY_PLAIN, 5,(255,255,255),5)
        
         
     
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    

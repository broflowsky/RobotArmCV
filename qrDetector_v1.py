import cv2
import numpy as np
import time
import sys


###############################################
def display(im,bbox):
    n = len(bbox)
    for j in range(n):
        cv2.line(im,tuple(bbox[j][0]),
                 tuple(bbox[(j+1) % n][0]),
                 (0,255,0),3)
        
###############################################
qrDetector = cv2.QRCodeDetector()

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

counter =0
print(" QRCode detector v1.0 ")
while True:
    ret, img = cap.read() # Capture frame-by-frame

    isDetected,qrCode = qrDetector.detect(img)
    
    if isDetected:
        counter+=1
        print("qrCode found ",counter)
        
    if qrCode is not None:
        display(img,qrCode)
        
    cv2.imshow('QRDetector Detector', img)
    c = cv2.waitKey(7) % 0x100
    if c == 27:
        break

cap.release()
cv2.destroyAll

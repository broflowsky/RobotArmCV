#!/usr/bin/env python3
"""
Single threaded qr reader with pyzbar
"""
from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
from threading import Thread
import cv2

#######################################
def decode(im):
#    mask = cv2.inRange(im,(0,0,0),(200,200,200))
#    thresholded = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
#    inverted = 255-thresholded # black-in-white
    decodedObjects = pyzbar.decode(im)
    count = 0
    for obj in decodedObjects:
#        print('Type : ',obj.type)
#        print('Data : ', obj.data,'\n')
        count +=1
    if count != 0:
        print('Qr code found : ', count)
    return decodedObjects
#######################################

#############################################################
def display(im, decodedObjects):
    for obj in decodedObjects:
        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(
                np.array([point for point in points],
                         dtype=np.float32))
            hull = list(map(tuple,np.squeeze(hull)))
        else:
            hull= points
        
        n = len(hull)
        for j in range(0,n):
            cv2.line(im, hull[j], hull[(j+1)%n], (0,255,0),3)
##############################################################
            
# Main   
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

counter =0
print(" QRCode detector v1.0 ")

while True:
    ret, img = cap.read() # Capture frame-by-frame
    decodedObjects = decode(img)
    display(img,decodedObjects)
    
    cv2.imshow('QRDetector Detector zbar', img)
    c = cv2.waitKey(7) % 0x100
    if c == 27:#press ESC
        break
    

cap.release()#close camera
cv2.destroyAllWindows()




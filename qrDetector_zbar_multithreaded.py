#!/usr/bin/env python3
"""
Multi-threaded qr reader with pyzbar
"""
from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
from threading import Thread
import cv2


##only can be used on rasberypi
import RPi.GPIO as GPIO
import time;

GPIO.setmode(GPIO.BOARD)


GPIO.setup(12,GPIO.OUT)
pwm = GPIO.PWM(12,100) #initalize pwm to 100hz

dc = 0;
pwm.start(dc)


class WebcamStream:
    def __init__(self,src =0):
        #init cv stream
        self.stream =cv2.VideoCapture(src)
        self.stream.set(3,640)
        self.stream.set(4,480)
        self.stopped = False
        
        #read first frame from the stream
        self.ret, self.img = self.stream.read()
    
    def start(self):
        Thread(target = self.update, args=()).start()
        return self
    
    def update(self):
        while True:
            if self.stopped:
                return
            self.ret,self.img = self.stream.read()
            
    def read(self):
        return self.img
    
    def stop(self):
        self.stopped = True
        
        

 
def decode(im):
    decodedObjects = pyzbar.decode(im)
    count = 0
    for obj in decodedObjects:
        count +=1
    if count != 0:  
     return decodedObjects




##knowing how big the physical QR code is we can find the distance to it by doing the ratio of what we see
def findMidPoint(points):
    
    middleX = 0;
    middleY = 0;

    for point in points:
        middleX = middleX + point[0]
        middleY = middleY + point[1]
    
    middleX = middleX/4
    middleY = middleY/4

    middle = (middleX,middleY)
    return middle


def findOffset(im, decodedObjects):
  if(decodedObjects is not None):
    for obj in decodedObjects:
        points = obj.polygon
        middle = findMidPoint(points)
        height, width = img.shape[:2]

        centerX = width/2
        centerY = width/2

        xOffset = middle[0] - centerX
        yOffset = middle[1] - centerY
        print(xOffset,yOffset)
    return xOffset,yOffset
      




def display(im, decodedObjects):
 if(decodedObjects is not None):
    for obj in decodedObjects:
        points = obj.polygon
        findMidPoint(points)
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


# def rotateplatform(xOffset):
#     print("rotateplatform")


# ##either relay the information to a microcontroller or do it ourselves
# def moveArmVertical():
#     print("moving arm vertically")

# def moveArmHorizontal():
#     print("moving arm horizontally")


# def movementHandler():
#     print("handling movements in thread")



        
camStream = WebcamStream()
        
counter =0
found = 0;
print(" QRCode detector v1.0 ")
camStream.start()
while True:
    img = camStream.read()
    decodedObjects = decode(img)

    offsets =  findOffset(img,decodedObjects)

    if(offsets is not None):
   	 if(offsets[0] <100 and offsets[0] > -100):
      	  found = 1

    if(found ==0):
         pwm.ChangeDutyCycle(30)
         time.sleep(0.05)
         pwm.ChangeDutyCycle(0)
         time.sleep(0.1)
    else:
     pwm.ChangeDutyCycle(0)


    #we wouldnt need to display though we just need to get the values
    #less processing power
    display(img,decodedObjects)
    
    cv2.imshow('QRDetector Detector zbar', img)
    c = cv2.waitKey(1) % 0x100
    if c == 27:#press ESC
        break
    

camStream.stop()
pwm.stop()
GPIO.cleanup()
cv2.destroyAllWindows()
            
            
            
    

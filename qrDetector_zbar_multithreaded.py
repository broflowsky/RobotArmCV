#!/usr/bin/env python3
"""
Multi-threaded qr reader with pyzbar
"""
from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
from threading import Thread
import cv2


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
        
        
camStream = WebcamStream()
        
counter =0
print(" QRCode detector v1.0 ")
camStream.start()
while True:
    img = camStream.read()
    decodedObjects = decode(img)
    display(img,decodedObjects)
    
    cv2.imshow('QRDetector Detector zbar', img)
    c = cv2.waitKey(1) % 0x100
    if c == 27:#press ESC
        break
    

camStream.stop()

cv2.destroyAllWindows()
            
            
            
    
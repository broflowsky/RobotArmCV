#!/usr/bin/env python3
"""
Multi-threaded qr reader with pyzbar
"""
from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
from threading import Thread
import cv2


#Variables
WEBCAM_RES_X = 480
WEBCAM_RES_y = 640
BWF_TOL = 150


#cv2.VideoCapture runs on its own thread
class WebcamStream:
    def __init__(self,src =0):
        #init cv stream
        self.stream =cv2.VideoCapture(src)
        self.stream.set(3,WEBCAM_RES_y)
        self.stream.set(4,WEBCAM_RES_X)
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
        print('releasing the camera')
        self.stream.stream.release()
        self.stopped = True
    
    def __del__(self):
        print('releasing the camera')
        self.stream.stream.release()
        
        

        
#######################################
def decode(im):
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
def draw_box(im, decodedObjects,):
     
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
        
def main():        
    camStream = WebcamStream()
    counter =0
    print(" QRCode detector pyzbar multithreaded ")
    camStream.start()
    while True:
        img = camStream.read()
        
        mask = cv2.inRange(img,(0,0,0),( BWF_TOL, BWF_TOL, BWF_TOL))
        thresholded = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
        bw_img = 255-thresholded # black-in-white
        
#        decodedObjects = decode(img)
        decodedBW = decode(bw_img)
        
#        draw_box(img,decodedObjects)
        draw_box(bw_img, decodedBW)
        
        cv2.imshow('QRDetector Detector zbar', img)
        cv2.imshow('QRDetector Detector zbar bw', bw_img)
        c = cv2.waitKey(1) % 0x100
        if c == 27:#press ESC
            break
        

    #cap.release()#close camera
    del camStream
    cv2.destroyAllWindows()
    print('exiting program')

main()

            
            
            
>>>>>>> b3c6e08c20ea41fa6c0f2cee967fe840988752b2
    
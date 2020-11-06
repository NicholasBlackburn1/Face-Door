"""
This is the main plate (Bulk) possessing done in my opencv Program
"""
from logging import log
from os import wait
from os.path import join

import cv2
import imutils
import numpy as np
import pytesseract
import zmq
import logging
from datetime import datetime

from zmq.sugar import frame



    # TODO: Change this into the ipcamera Stream.
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FPS, 15)


                    # Grab a single frame of video
 

while True:
    ret, frame = video_capture.read()    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    gray = cv2.bilateralFilter(gray, 13, 15, 15) 
    edged = cv2.Canny(gray, 30, 200) 
    
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = 0 

    for c in contours:
        
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        screenCnt = approx
        cv2.drawContours(frame, [approx], -1, (0, 0, 255), 3)
        
    mask = np.zeros(gray.shape,np.uint8)
    new_image = cv2.drawContours(mask,screenCnt,0,255,-1,)
    new_image = cv2.bitwise_and(frame,frame,mask=mask)

    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx+1, topy:bottomy+1]

    text = pytesseract.image_to_string(Cropped, config='--psm 11')

    print("Detected license plate Number is:",text)
    cv2.imshow('car',frame)
    cv2.imshow('gray', gray)
    cv2.imshow('canny', edged)
    #cv2.imshow('output', img)
 # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

   
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
ret, frame = video_capture.read()     
      
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
gray = cv2.bilateralFilter(gray, 13, 15, 15) 

edged = cv2.Canny(gray, 30, 200) 
contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

while True:
  
    cv2.imshow('car',frame)
   

    cv2.waitKey(0)
    cv2.destroyAllWindows()
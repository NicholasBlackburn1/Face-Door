"""
This is the main (Bulk) possessing done in my opencv Program
TODO: Need to Fix Face loading into Facial Reconition lib
TODO: Need to have a Gstreamer out to asmble an video stream Effecintly to allow user to view it live on web page hehe
TODO: REMOVE ZMQ SOCKET DATA
TODO: ASSINE USERS UUIDS TO MAKE IT EASER
"""


from os import path
from uuid import uuid1
import uuid
import ast
from collections import OrderedDict
import logging
from numbers import Number

from os.path import join
import shutil
from tokenize import Double, String
import json

import cv2
import numpy as np
import os
from datetime import datetime
import time
import logging
from prosessing.data.Database import getUserUUID
import zmq
from time import sleep
import threading
import base64
import json
import math
import prosessing.data.Database as db
import wget
from prosessing.data.CvFileHandler import CvFileHandler as filehandler
import pathlib
from configparser import ConfigParser
from PIL import Image
from prosessing.data.DataClass import UserData
import prosessing.data.KnnClassifiyer as Knn
from pathlib import Path

class VideoProsessing(object):

    imagename = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p_%s")
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    video_capture = cv2.VideoCapture(0)
    
    userList = []

    # Encodes all the Nessiscary User info into Json String so it can be easly moved arround

    def UserDataList(self):
        i = 0
        
        while True:
            # example Json string  [{"uuid":"Tesla", "name":2, "status":"New York",image:none, url:}]
            print(str("Data index ")+str(i))

            # this is Where the Data gets Wrapped into am DataList with uuid First key
            local_data = {
                db.getUserUUID(db.getFaces(), i): UserData(db.getName(db.getFaces(), i), db.getStatus(db.getFaces(), i), db.getImageName(db.getFaces(), i), db.getImageUrI(db.getFaces(), i))
            }

            self.userList.append(local_data)
         
            i += 1

            # Checks to see if i == the database amount hehe
            if(i == db.getAmountOfEntrys()):
                logging.warn(
                    "Amout of Entrys are in the array strings are"+str(db.getAmountOfEntrys()))
                return

    #

    # saves downloaded Image Converted to black and white
    def downloadFacesAndProssesThem(self, logging, userData, filepath):
       
        Path(filepath+"/").mkdir(parents=True, exist_ok=True)

        print(" this is the data yaya" + str(userData))

        if(not os.path.exists(filepath+userData.image+".jpg")):
            wget.download(userData.downloadUrl, str(filepath))
            logging.info('Downloading ' +
                         str(userData.image)+', this may take a while...')
            logging.info("output file" +
                         str(userData.image+"at" + filepath))

        # this function will load and prepare face encodes  for
    # saves owner images and sends Frame
    def saveImage(self, imagepath, imagename, frame):
        cv2.imwrite(imagepath + imagename + ".jpg", frame)

    # Fully Downloades USer Images and Returns No data

    def downloadUserFaces(self, imagePath):

        index = 0
        
        # gets users names statuses face iamges and the urls from the tuples
        while True:
            userinfo = self.userList[index][db.getUserUUID(db.getFaces(), index)]

            print("Some Initerable data"+ str(userinfo))

            self.downloadFacesAndProssesThem(logging, self.userList[index][db.getUserUUID(db.getFaces(), index)], imagePath+str(userinfo.user))
            logging.warn("downloaded"+str(index) + "out of " +str(db.getAmountOfEntrys()))
            
            index += 1

            if(index == db.getAmountOfEntrys()):
                logging.info("Done Downloading Images UWU....")
                return

                # Add names of the ecodings to thw end of list
        '''
        This Function is the Bulk of the Openv Image Prossesing Code
        '''

    def ProcessVideo(self):
        # sets rtsp vsr in python
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

        # gets Config file
        print("Example Config"+str(pathlib.Path().absolute()) +
              "/src/prosessing/"+"Config.ini")
        # Read config.ini file
        config_object = ConfigParser()
        config_object.read(str(pathlib.Path().absolute()) +
                           "/src/prosessing/"+"Config.ini")

        logconfig = config_object['LOGGING']
        zmqconfig = config_object['ZMQ']
        opencvconfig = config_object['OPENCV']
        fileconfig = config_object['FILE']
        current_time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p_%s")

        rootDirPath = fileconfig['rootDirPath']
        configPath = fileconfig['rootDirPath']+fileconfig['configPath']
        imagePath = fileconfig['rootDirPath'] + fileconfig['imagePath']
        imagePathusers = fileconfig['rootDirPath'] +fileconfig['imagePathusers']

        logging.basicConfig(filename=configPath+logconfig['filename'] + datetime.now().strftime(
            "%Y_%m_%d-%I_%M_%S_%p_%s")+".log", level=logging.DEBUG)

        if(self.video_capture == None):
            logging.error(Exception("Camera Not Found! Sorry Master.... i Faild you"))
            return

# connects to database
        # Database connection handing
        logging.info("Connecting to the Database Faces")
        logging.debug(db.getFaces())
        logging.info("connected to database Faces")
        logging.info("connecting to zmq")

# inits Zmq Server
        ZMQURI = str("tcp://"+zmqconfig['ip']+":"+zmqconfig['port'])

        ctx = zmq.Context()
        sock = ctx.socket(zmq.PUB)
        sock.bind(ZMQURI)
        logging.info("conneted to zmq")
        
        #Updates Data in the Usable data list uwu
        self.UserDataList()

        # sends setup message and sets base image name to the current date mills and image storage path
        sock.send(b"setup")
        logging.info("Setting up cv")

        # Downlaods all the Faces
        self.downloadUserFaces(imagePathusers)

        # Trains Knn
        Knn.train(train_dir=imagePathusers,
                  model_save_path=imagePathusers+"Face_Rec.model")
        logging.info("Cv setup")

        sock.send(b"starting")

        while True:

            # graps image to read
            ret, frame = VideoProsessing.video_capture.read()

            # gets video
            fps = int(VideoProsessing.video_capture.get(2))
            width = int(VideoProsessing.video_capture.get(3))   # float `width`
            # float `height`
            height = int(VideoProsessing.video_capture.get(4))

            # checks to see if frames are vaild not black or empty
            if(frame == None):
                logging.warning(str(current_time) +
                                "Frame is Not Vaild Skiping...")

            if np.sum(frame) == 0:
                logging.warning(str(current_time) +
                                "Frame is all black Skiping...")

            if (width > 0 and height > 0):
                logging.warn("cannot open Non exsting image")
                print("Broaking Image Uwu It does not Exsit fix")

            # Resize frame of video to 1/4 size for faster face detection processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

            predictions = Knn.predict(X_frame=small_frame)

            """
            This Section is Dedicated to dealing with user Seperatation via the User Stats data tag
            """
            i = 0
            status = None
            # Display the results
            for name, (top, right, bottom, left) in predictions:

                # Should return user status based on the name linked to user uuid
                if(name == VideoProsessing.user_Array[db.getUserUUID(db.getFaces(), i)].user):
                    status == VideoProsessing.user_Array[db.getUserUUID(
                        db.getFaces(), i)].status

                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                if (status == 'Admin'):
                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top),
                                  (right, bottom), (0, 255, 0), 2)

                    font = cv2.FONT_HERSHEY_DUPLEX

                    cv2.putText(frame, name, (left, top),
                                font, 0.5, (255, 255, 255), 1)
                    cv2.putText(
                        frame, "Known Person..", (0,
                                                  430), font, 0.5, (255, 255, 255), 1
                    )
                    cv2.putText(frame, status, (0, 450),
                                font, 0.5, (255, 255, 255), 1)
                    cv2.putText(frame, name, (0, 470), font,
                                0.5, (255, 255, 255), 1)

                    # sends Image and saves image to disk
                    if(not os.path.exists(imagePath+"Admin/"+self.imagename+".jpg")):

                        self.saveImage(imagePath+"Admin/",
                                       self.imagename, frame)

                        # sends person info
                        filehandler.send_person_name(sock, name, logging)
                        # send_group_status(sock,"owner")

                # User Grade Status
                if (status == 'User'):
                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top),
                                  (right, bottom), (255, 255, 0), 2)

                    font = cv2.FONT_HERSHEY_DUPLEX

                    cv2.putText(frame, name, (left, top),
                                font, 0.5, (255, 255, 255), 1)
                    cv2.putText(
                        frame, "Known Person..", (0,
                                                  430), font, 0.5, (255, 255, 255), 1
                    )
                    cv2.putText(
                        frame, status, (0,
                                        450), font, 0.5, (255, 255, 255), 1
                    )
                    cv2.putText(frame, name, (0, 470), font,
                                0.5, (255, 255, 255), 1)

                    # Distance info
                    cv2.putText(
                        frame,
                        "T&B" + str(top) + "," + str(bottom),
                        (474, 430),
                        font,
                        0.5,
                        (255, 255, 255),
                        1,
                    )
                    cv2.putText(
                        frame,
                        "L&R" + str(left) + "," + str(right),
                        (474, 450),
                        font,
                        0.5,
                        (255, 255, 255),
                        (255, 255, 255),
                        1,
                    )

                    # checks to see if image exsitis
                    if(not os.path.exists(imagePath+"User/"+self.imagename+".jpg")):

                        # sends Image and saves image to disk
                        self.saveImage(imagePath+"User/",
                                       self.imagename, frame)

                        # sends person info
                        filehandler.send_person_name(sock, name, logging)
                    #

                if (status == 'Unwanted'):

                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.rectangle(frame, (left, top),
                                  (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, name, (left, top),
                                font, 0.5, (255, 255, 255), 1)
                    # Distance info
                    cv2.putText(frame, status, (0, 450),
                                font, 0.5, (255, 255, 255), 1)
                    cv2.putText(frame, name, (0, 470), font,
                                0.5, (255, 255, 255), 1)

                    logging.warning("not letting in" + name)

                    # checks to see if image exsitis
                    if(not os.path.exists(imagePath+"Unwanted/" + self.imagename + ".jpg")):

                        # sends Image and saves image to disk
                        self.saveImage(imagePath+"Unwanted/",
                                       self.imagename, frame)

                        # sends person info
                        filehandler.send_person_name(sock, name, logging)
                        # send_group_status(sock,"Unknown")
                elif (
                    len(predictions) >= 2
                ):

                    cv2.rectangle(
                        frame, (left, top), (right,
                                             bottom), (255, 0, 255), 2
                    )

                    font = cv2.FONT_HERSHEY_DUPLEX

                    cv2.putText(frame, name, (left, top),
                                font, 0.5, (255, 255, 255), 1)

                    # Distance info
                    cv2.putText(
                        frame,
                        "There's a group..",
                        (474, 430),
                        font,
                        0.5,
                        (255, 255, 255),
                        1,
                    )
                    cv2.putText(
                        frame,
                        "be carfull now!",
                        (474, 450),
                        font,
                        0.5,
                        (255, 255, 255),
                        1,
                    )

                    logging.warning("Letting in group")

                    if(not os.path.exists(imagePath + "Group/" + self.imagename + ".jpg")):

                        # sends Image and saves image to disk
                        self.saveImage(imagePath + "Group/",
                                       self.imagename, frame)

                        # sends person info
                        filehandler.send_person_name(sock, name, logging)

                elif (name == opencvconfig['unreconizedPerson'] or status == None):
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.rectangle(frame, (left, top),
                                  (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, name, (left, top),
                                font, 0.5, (255, 255, 255), 1)
                    # Distance info
                    cv2.putText(frame, opencvconfig['unreconizedPerson'], (0, 450),
                                font, 0.5, (255, 255, 255), 1)
                    cv2.putText(frame, name, (0, 470), font,
                                0.5, (255, 255, 255), 1)

                    # checks to see if image exsitis
                    if(not os.path.exists(imagePath + "unknown/" + self.imagename + ".jpg")):
                        # sends Image and saves image to disk
                        self.saveImage(imagePath+"unknown/",
                                       self.imagename, frame)

                        # sends person info
                        filehandler.send_person_name(sock, name, logging)
                        # send_group_status(sock,"Unknown")

                # Display the resulting image
                cv2.imshow("Video", frame)

                # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

"""
This is the main (Bulk) possessing done in my opencv Program
TODO: Need to Fix Face loading into Facial Reconition lib
TODO: Need to have a Gstreamer out to asmble an video stream Effecintly to allow user to view it live on web page hehe
TODO: REMOVE ZMQ SOCKET DATA
TODO: ASSINE USERS UUIDS TO MAKE IT EASER
"""


from asyncio.log import logger
from os import path
from uuid import uuid1
import uuid
import ast
from collections import OrderedDict, UserList
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
import pathlib
from configparser import ConfigParser
from PIL import Image
from prosessing.data.DataClass import UserData
import prosessing.data.KnnClassifiyer as Knn
from pathlib import Path
import face_recognition
import imutils
import prosessing.data.UsersStat as Stat


class VideoProsessing(object):

    imagename = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p_%s")
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
    imagePathusers = fileconfig['rootDirPath'] + fileconfig['imagePathusers']
    plateImagePath = fileconfig['rootDirPath'] + fileconfig['platePath']

    # Camera Stream

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
    # Fully Downloades USer Images and Returns No data

    def downloadUserFaces(self, imagePath):

        index = 0

        # gets users names statuses face iamges and the urls from the tuples
        while True:
            userinfo = self.userList[index][db.getUserUUID(
                db.getFaces(), index)]

            print("Some Initerable data" + str(userinfo))

            self.downloadFacesAndProssesThem(logging, self.userList[index][db.getUserUUID(
                db.getFaces(), index)], imagePath+str(db.getUserUUID(db.getFaces(), index)))
            logging.warn("downloaded"+str(index) + "out of " +
                         str(db.getAmountOfEntrys()))

            index += 1

            if(index == db.getAmountOfEntrys()):
                logging.info("Done Downloading Images UWU....")
                return

                # Add names of the ecodings to thw end of list

     # sends person name to subsecriber

    # Sends Opencv Stats To Launces
    def sendProgramStatus(self, messgae, sock, logging):
        logging.info("[SOCKET Messgae]")
        sock.send_string("StatusMessage")
        sock.send_json({"message": str(messgae)})
        logging.info("[SOCKET Messafe] s")

        # sends Currenly Seen Faces to subsecriber
    def sendCurrentSeenFacesAmount(self, sock, faceAmount):
        logging.info("[SOCKET Amount] Sending Face Amount")
        sock.send_string("FaceAmount")
        sock.send_json({"amount": faceAmount})
        logging.info("[SOCKET Amount] Sent Face Amount")

    # sends Life time Face ammount to subsecriber
    def sendLifeTimeFacesAmount(self, sock, faceAmount):
        logging.info("[SOCKET Life Time Amount] Sending Face Amount")
        sock.send_string("LifeTimeFaceAmount")
        sock.send_json({"faces": faceAmount})
        logging.info("[SOCKET Life Time Amount] Sent Face Amount")

    # Get Amout Of Faces In Frame
    def getAmountofFaces(self, rec, frame):
        face_bounding_boxes = rec.face_locations(frame,model="cnn")
        return len(face_bounding_boxes)


    '''
    This Function is the Bulk of the Openv Image Prossesing Code
    '''

    def ProcessFaceVideo(self):

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
        imagePathusers = fileconfig['rootDirPath'] + fileconfig['imagePathusers']

        logging.basicConfig(filename=configPath+logconfig['filename'] + datetime.now().strftime(
            "%Y_%m_%d-%I_%M_%S_%p_%s")+".log", level=logging.DEBUG)

        # Camera Stream
        video_capture = cv2.VideoCapture('rtsp://192.168.5.27:554/out.h264')

        if(video_capture == None):
            logging.error(
                Exception("Camera Not Found! Sorry Master.... i Faild you"))
            return

        # connects to database
        # Database connection handing
        logging.info("Connecting to the Database Faces")
        logging.debug(db.getFaces())
        logging.info("connected to database Faces")
        logging.info("connecting to zmq")

        Modelpath = str(imagePathusers+'UwU.clf')
        allthefaces = 0

# inits Zmq Server
        ZMQURI = str("tcp://"+zmqconfig['ip']+":"+zmqconfig['port'])

        ctx = zmq.Context()
        sock = ctx.socket(zmq.PUB)
        sock.bind(ZMQURI)
        logging.info("conneted to zmq")

        self.sendProgramStatus(messgae="Starting Presetup",
                               sock=sock, logging=logging)

        # Updates Data in the Usable data list uwu
        self.UserDataList()

        # sends setup message and sets base image name to the current date mills and image storage path
        self.sendProgramStatus(messgae="Started setup",
                               sock=sock, logging=logging)
        logging.info("Setting up cv")

        # Downlaods all the Faces
        self.downloadUserFaces(imagePathusers)

     
        #TODO: add check to see if there are new entrys in data compared to last run to see if need to run train new knn
        print("Training Model.....")
        logging.info('Training Model....')

        self.sendProgramStatus(messgae="Training Models",
                               sock=sock, logging=logging)
        Knn.train(train_dir=imagePathusers,model_save_path=Modelpath, n_neighbors=2)
        print("Done Training Model.....")
        logging.info('Done Training Model....')

        logging.info("Cv setup")

        i = 0
        face_index =0
        process_this_frame = 29
        status = None
        while 0 < 1:

            # graps image to read
            ret, frame = video_capture.read()
           
            # gets video
            fps = int(video_capture.get(2))
            width = int(video_capture.get(3))   # float `width`
            # float `height`
            height = int(video_capture.get(4))

            # checks to see if frames are vaild not black or empty

            if (width is 0 or height is 0):
                logging.warn("cannot open Non exsting image")
                logging.error(
                    Exception("Cannnot Due reconition on an Empty Frame *Sad UwU Noises*"))
                print(
                    Exception("Cannnot Due reconition on an Empty Frame *Sad UwU Noises*"))

        

            img = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

            process_this_frame = process_this_frame + 1
            if process_this_frame % 30 == 0:
                predictions = Knn.predict(img, model_path=Modelpath)
            
                print("Looking for faces...")
                """
                    This Section is Dedicated to dealing with user Seperatation via the User Stats data tag
                """
                font = cv2.FONT_HERSHEY_DUPLEX
                # Display the results
                for name,(top, right, bottom, left) in predictions:
                    
                        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 2
                    right *= 2
                    bottom *= 2
                    left *= 2

                    print("predicting Faces..." )

                    
                    
                    if(name == 'unknown'):
                        Stat.userUnknown(sock,status,opencvconfig,name,frame,font,self.imagename,imagePath,left,right,bottom,top)
                        logging.info("unknowns Here UwU!")
                    else:
                        userinfo = self.userList[i][name]
                        status = userinfo.status
                        name = userinfo.user
                    
                        # this is for handling User Sections in a clean whay
                        faces = self.getAmountofFaces(face_recognition, frame)
                        
                        if (status == 'Admin'):
                            logging.info("got an Admin The name is"+str(name))
                            Stat.userAdmin(sock,status,name,frame,font,self.imagename,imagePath,left,right,bottom,top)

                        if (status == 'User'):
                            logging.info("got an User Human The name is"+str(name))
                            Stat.userUser(sock,status,name,frame,font,self.imagename,imagePath,left,right,bottom,top)

                        if (status == 'Unwanted'):
                            logging.info("got an Unwanted Human The name is"+str(name))
                            Stat.userUnwanted(sock,status,name,frame,faces,font,self.imagename,imagePath,left,right,bottom,top)
                        
                        if(faces >= 2):
                            Stat.userGroup(sock,frame,font,self.imagename,imagePath,left,right,bottom,top)

                        if(faces>=0 and db.getLifefaces(db.getLifetime())== 0):
                            db.setLifetimeFaceCount(db.getLifetime(),faces)
                        if(faces>=0):
                            db.setLifetimeFaceCount(db.getLifetime(),db.getLifefaces(db.getLifetime())+faces)

                           

                        if(i == len(self.userList[i]) and faces):
                            print("not going to incrament because I dont want outof bpunds")
                            logging.info("should not count up because it will through out of bounds")
                        else:
                            if(i >= len(self.userList[i])):
                                i +=1
                            else:
                                logging.info("not going to incrament because its equle")
                                print("not going to incrament because I dont want outof bpunds")

                            
                    
            if ord('q') == cv2.waitKey(10):
                cv2.destroyAllWindows()
                exit(0)
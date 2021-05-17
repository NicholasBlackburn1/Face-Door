"""
This is the main (Bulk) possessing done in my opencv Program
TODO: Need to have a Gstreamer out to asmble an video stream Effecintly to allow user to view it live on web page hehe
TODO: REMOVE ZMQ SOCKET DATA
TODO: 
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
import prosessing.messaging.SmsHandler as message
import prosessing.videoThread

class VideoProsessing(object):

    imagename = datetime.now().strftime("%Y_%m_%d-%I_%M_%S")
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
    smsconfig =  config_object['SMS']

    current_time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p_%s")
 
    rootDirPath = fileconfig['rootDirPath']
    configPath = fileconfig['rootDirPath']+fileconfig['configPath']
    imagePath = fileconfig['rootDirPath'] + fileconfig['imagePath']
    imagePathusers = fileconfig['rootDirPath'] + fileconfig['imagePathusers']
    plateImagePath = fileconfig['rootDirPath'] + fileconfig['platePath']

    Modelpath = str(imagePathusers+'UwU.clf')

    # Camera Stream
    vs = prosessing.videoThread.ThreadingClass(str(opencvconfig['Stream_intro']+opencvconfig['Stream_ip']+":"+opencvconfig['Stream_port']+opencvconfig['Stream_local']))
   


    userList = []


    #Makes startup dirs
    def makefiledirs(self):
        logging.info("Creating Folder Dirs")
        Path(self.rootDirPath).mkdir(parents=True, exist_ok=True)
        Path(self.imagePathusers).mkdir(parents=True, exist_ok=True)
        Path(self.configPath).mkdir(parents=True, exist_ok=True)
        Path(self.plateImagePath).mkdir(parents=True, exist_ok=True)
        logging.info("Made Folder Dirs")



    # Encodes all the Nessiscary User info into Json String so it can be easly moved arround

    def UserDataList(self):
        i = 0

        while True:
            # example Json string  [{"uuid":"Tesla", "name":2, "status":"New York",image:none, url:}]
            print(str("Data index ")+str(i))

            # this is Where the Data gets Wrapped into am DataList with uuid First key
            local_data = {
                db.getUserUUID(db.getFaces(), i): UserData(db.getName(db.getFaces(), i), db.getStatus(db.getFaces(), i), db.getImageName(db.getFaces(), i), db.getImageUrI(db.getFaces(), i), db.getPhoneNum(db.getFaces(), i))
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


    # Get Amout Of Faces In Frame
    def getAmountofFaces(self, rec, frame):
        face_bounding_boxes = rec.face_locations(frame,model="cnn")
        return len(face_bounding_boxes)

    # recives RTSP camra Stream
    def rtspRecive(self):
            
            # graps image to read
            frame = self.vs.read()

            width = int(self.vs.cap.get(3))   # float `width`
            height = int(self.vs.cap.get(4))  # float `height`

            # checks to see if frames are vaild not black or empty

            if (width is 0 or height is 0):
                logging.warn("cannot open Non exsting image")
                logging.error(
                    Exception("Cannnot Due reconition on an Empty Frame *Sad UwU Noises*"))
                print(
                    Exception("Cannnot Due reconition on an Empty Frame *Sad UwU Noises*"))
        


    '''
    This Function is the Bulk of the Openv Image Prossesing Code
    '''
    
    def ProcessFaceVideo(self):
        # Makes Folder Dir
        #`self.makefiledirs()
        if( not os.path.exists(self.rootDirPath)):
            logging.warn("creating Dirs")
            self.makefiledirs()
        # sets rtsp vsr in python
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

        # gets Config file
        print("Example Config"+str(pathlib.Path().absolute()) +
              "/src/prosessing/"+"Config.ini")
        # Read config.ini file
        config_object = ConfigParser()
        config_object.read(str(pathlib.Path().absolute()) +
                           "/src/prosessing/"+"Config.ini")
                           
        logging.basicConfig(filename=self.configPath+self.logconfig['filename'] + datetime.now().strftime(
            "%Y_%m_%d-%I_%M_%S_%p_%s")+".log", level=logging.DEBUG)

        # connects to database
        # Database connection handing
        logging.info("Connecting to the Database Faces")
        logging.debug(db.getFaces())
        logging.info("connected to database Faces")
        logging.info("connecting to zmq")

        
        allthefaces = 0

# inits Zmq Server
        ZMQURI = str("tcp://"+self.zmqconfig['ip']+":"+self.zmqconfig['port'])

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
        self.downloadUserFaces(self.imagePathusers)

     
        #TODO: add check to see if there are new entrys in data compared to last run to see if need to run train new knn
        print("Training Model Going to take a while UwU..... ")
        logging.info('Training Model....')

        self.sendProgramStatus(messgae="Training Models",sock=sock, logging=logging)
        
        Knn.train(train_dir=self.imagePathusers,model_save_path=self.Modelpath, n_neighbors=2)
        print("Done Training Model.....")
        logging.info('Done Training Model....')
        

        self.rtspRecive()
        logging.info("Looking for faces.....")
        print("Looking for Faces...")
     
        i = 0
        face_index =0
        process_this_frame = 29
        status = None
        while 0 < 1:
            frame = self.vs.read()

            img = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            
            process_this_frame = process_this_frame + 1
            if process_this_frame % 30 == 0:
                predictions = Knn.predict(img, model_path=self.Modelpath)
            
                """
                    This Section is Dedicated to dealing with user Seperatation via the User Stats data tag
                """
                font = cv2.FONT_HERSHEY_DUPLEX
                sent = False
                # Display the results
                for name,(top, right, bottom, left) in predictions:
                    
                        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 2
                    right *= 2
                    bottom *= 2
                    left *= 2
                    print(name)
                    

                    
                    if(name != None):
                            

                            if(name == 'unknown' and status == None):
                                Stat.userUnknown(self.opencvconfig,name,frame,font,imagename =self.imagename,imagePath=self.imagePath,left = left,right =right,bottom =bottom,top =top)
                                print("user is unknown")
                                logging.info("unknowns Here UwU!")
                                self.sendCurrentSeenFacesAmount(sock,self.getAmountofFaces(face_recognition, frame))
                            else:
                                userinfo = self.userList[i][name]
                                status = userinfo.status
                                name = userinfo.user
                                phone = userinfo.phoneNum

                                print(str(name) + "   "+ str(status))
                        
                                
                            
                                if (status == 'Admin'):
                                    logging.info("got an Admin The name is"+str(name))
                                    self.sendCurrentSeenFacesAmount(sock,self.getAmountofFaces(face_recognition, frame))
                                    Stat.userAdmin(status,name,frame,font,self.imagename,self.imagePath,left,right,bottom,top)
                                
                                    if(sent != True):
                                        message.sendCapturedImageMessage("eeeep there is an Admin Person Be Good"+" "+ "There Name is:"+ str(name),phone,'http://192.168.5.7:2000/admin',self.smsconfig['textbelt-key'])
                                        sent=True
                                    
                                if (status == 'User'):
                                    logging.info("got an User Human The name is"+str(name))
                                    Stat.userUser(status,name,frame,font,self.imagename,self.imagePath,left,right,bottom,top)
                                    message.sendCapturedImageMessage("eeeep there is an User They Might be evil so um let them in"+"  `"+"There Name is:"+ str(name),phone,'http://192.168.5.7:2000/user',self.smsconfig['textbelt-key'])

                                if (status == 'Unwanted'):
                                    logging.info("got an Unwanted Human The name is"+str(name))
                                    Stat.userUnwanted(status,name,frame,font,self.imagename,self.imagePath,left,right,bottom,top)
                                    self.sendCurrentSeenFacesAmount(sock,self.getAmountofFaces(face_recognition, frame))
                                
                                    message.sendCapturedImageMessage("eeeep there is an Unwanted Get them away from ME!"+" "+ "There Name is:"+ str(name),phone,'http://192.168.5.7:2000/unwanted',self.smsconfig['textbelt-key'])
                                    
                                if(self.getAmountofFaces(face_recognition, frame) > 1):
                                    Stat.userGroup(frame,font,self.imagename,self.imagePath,left,right,bottom,top)
                                    message.sendCapturedImageMessage("eeeep there is Gagle of Peope I dont know what to do",phone,'http://192.168.5.7:2000/group',self.smsconfig['textbelt-key'])
                    
                                if(i == len(self.userList[i]) and self.getAmountofFaces(face_recognition, frame)):
                                    print("not going to incrament because I dont want outof bpunds")
                                    logging.info("should not count up because it will through out of bounds")
                                else:
                                    if(i >= len(self.userList[i])):
                                        i +=1
                                    else:
                                        logging.info("not going to incrament because its equle")
                                        print("not going to incrament because I dont want outof bpunds")

                                    
                        
                if ord('q') == cv2.waitKey(10):
                    self.vs.release()
                    cv2.destroyAllWindows()
                    exit(0)

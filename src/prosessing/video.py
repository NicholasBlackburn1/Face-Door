"""
This is the main (Bulk) possessing done in my opencv Program
TODO: Remove RecvRstp function and Implemnt Fram Size checks to main processing code
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
import prosessing.videoThread as videoThread
import gc
from colorama import init, Fore, Back, Style
import utils.textColors as console_log


class VideoProsessing(object):
    watchdog = 0
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
    smsconfig = config_object['SMS']

    current_time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p_%s")

    rootDirPath = fileconfig['rootDirPath']
    configPath = fileconfig['rootDirPath']+fileconfig['configPath']
    imagePath = fileconfig['rootDirPath'] + fileconfig['imagePath']
    imagePathusers = fileconfig['rootDirPath'] + fileconfig['imagePathusers']
    plateImagePath = fileconfig['rootDirPath'] + fileconfig['platePath']

    Modelpath = str(imagePathusers+'UwU.clf')

    userList = []

    # Makes startup dirs

    def makefiledirs(self):
        console_log.Warning("Creating Folder Dirs")
        Path(self.rootDirPath).mkdir(parents=True, exist_ok=True)
        Path(self.imagePathusers).mkdir(parents=True, exist_ok=True)
        Path(self.configPath).mkdir(parents=True, exist_ok=True)
        Path(self.plateImagePath).mkdir(parents=True, exist_ok=True)
        console_log.Warning("Made Folder Dirs")

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
                return

    # saves downloaded Image Converted to black and white

    def downloadFacesAndProssesThem(self, userData, filepath):

        Path(filepath+"/").mkdir(parents=True, exist_ok=True)

        if(not os.path.exists(filepath+userData.image+".jpg")):
            wget.download(userData.downloadUrl, str(filepath))

        # this function will load and prepare face encodes  for
    # Fully Downloades USer Images and Returns No data

    def downloadUserFaces(self, imagePath):

        index = 0

        # gets users names statuses face iamges and the urls from the tuples
        while True:
            userinfo = self.userList[index][db.getUserUUID(
                db.getFaces(), index)]

            self.downloadFacesAndProssesThem(self.userList[index][db.getUserUUID(
                db.getFaces(), index)], imagePath+str(db.getUserUUID(db.getFaces(), index)))
            console_log.PipeLine_Data(
                "downloaded"+" "+str(index) + " out of " + str(db.getAmountOfEntrys()) + "\n")

            index += 1

            if(index == db.getAmountOfEntrys()):
                console_log.Warning("Done Downloading Images UWU....")
                return

                # Add names of the ecodings to thw end of list

     # sends person name to subsecriber

    # Get Amout Of Faces In Frame
    def getAmountofFaces(self, rec, frame):
        face_bounding_boxes = rec.face_locations(frame, model="cnn")
        return len(face_bounding_boxes)

    # recives RTSP camra Stream
    def rtspRecive(self, vs):

        # graps image to read
        frame = vs.read()

        width = int(vs.cap.get(3))   # float `width`
        height = int(vs.cap.get(4))  # float `height`

        # checks to see if frames are vaild not black or empty

        if (width is 0 or height is 0):
            self.watchdog += 1
            logging.warn("cannot open Non exsting image")
            print(
                Exception("Cannnot Due reconition on an Empty Frame *Sad UwU Noises*"))
            print(
                Exception("Cannnot Due reconition on an Empty Frame *Sad UwU Noises*"))

    # Face accurcy Calculation UwU
    def face_distance_to_conf(face_distance, face_match_threshold=0.6):
        if face_distance > face_match_threshold:
            range = (1.0 - face_match_threshold)
            linear_val = (1.0 - face_distance) / (range * 2.0)
            return linear_val
        else:
            range = face_match_threshold
            linear_val = 1.0 - (face_distance / (range * 2.0))
            return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))

    '''
    This Function is the Bulk of the Openv Image Prossesing Code
    '''

    def setsUpPipeLine(self):

        init()

        pipeline_start_setup = datetime.now()
        # detecting pipe line start

        console_log.PipeLine_init(cv2.getBuildInformation())

        gc.enable()
        # Makes Folder Dir
        # `self.makefiledirs()
        if(not os.path.exists(self.rootDirPath)):
            console_log.Warning("creating Dirs")
            self.makefiledirs()
        # sets rtsp vsr in python
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

        # gets Config file
        console_log.Debug("Example Config"+str(pathlib.Path().absolute()) +
                          "/src/prosessing/"+"Config.ini")
        # Read config.ini file
        config_object = ConfigParser()
        config_object.read(str(pathlib.Path().absolute()) +
                           "/src/prosessing/"+"Config.ini")

        # connects to database
        # Database connection handing
        console_log.Warning("Connecting to the Database Faces")
        console_log.PipeLine_Data(db.getFaces())
        console_log.Warning("connected to database Faces")

        # Updates Data in the Usable data list uwu
        self.UserDataList()

        console_log.Warning("Setting up cv")

        # Downlaods all the Faces
        self.downloadUserFaces(self.imagePathusers)

        console_log.PipeLine_Ok(
            "PipeLine Setup End time"+str(datetime.now() - pipeline_start_setup))

        # TODO: add check to see if there are new entrys in data compared to last run to see if need to run train new knn
        pipeline_train_knn = datetime.now()

        console_log.Warning("Training Model Going to take a while UwU..... ")
        Knn.train(train_dir=self.imagePathusers,
                  model_save_path=self.Modelpath, n_neighbors=2)
        console_log.PipeLine_Ok(
            "Done Train Knn pipeline timer" + str(datetime.now() - pipeline_train_knn))
        console_log.Warning("Done Training Model.....")

        # cleans mess as we keep prosessing
        gc.collect()

        # Camera Stream gst setup
        gst_str = ("rtspsrc location={} latency={}  ! rtph264depay  ! nvv4l2decoder ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert !appsink".format(
            str(self.opencvconfig['Stream_intro']+self.opencvconfig['Stream_ip']+":"+self.opencvconfig['Stream_port']), 0, 720, 480))

        console_log.Warning("Looking for Faces...")

        i = 0
        face_index = 0
        process_this_frame = 25
        status = None
        pipeline_video_prossesing = datetime.now()

        cap = videoThread.ThreadingClass(gst_str)
        
        face_processing_pipeline_timer = datetime.now()

        while 1 >0:
            process_this_frame = process_this_frame + 1

            if process_this_frame % 30 == 0:

                frame = cap.read()
                #print(cap.read().get(cv2. CV_CAP_PROP_FPS))
                #frame = cv2.imread("/mnt/SecuServe/user/people/a93121a4-cc4b-11eb-b91f-00044beaf015/a924857a-cc4b-11eb-b91f-00044beaf015 (1).jpg",cv2.IMREAD_COLOR)
                img = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                predictions = Knn.predict(
                    img, model_path=self.Modelpath, distance_threshold=0.5)
                # print(process_this_frame)

                """
                    This Section is Dedicated to dealing with user Seperatation via the User Stats data tag
                """
                font = cv2.FONT_HERSHEY_DUPLEX
                sent = False
                

                # Display t he results
                for name, (top, right, bottom, left) in predictions:

                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 2
                    right *= 2
                    bottom *= 2
                    left *= 2
                    print("frame at" + str(process_this_frame))
                    print(name)

                    if(name != None):

                        if(name == 'unknown' and status == None):
                            Stat.userUnknown(self.opencvconfig, name, frame, font, imagename=self.imagename, imagePath=self.imagePath,
                                             left=left, right=right, bottom=bottom, top=top, framenum=process_this_frame)
                        # print("user is unknown")
                            logging.info("unknowns Here UwU!")
                            #message.sendCapturedImageMessage("eeeep there is an unknown",4123891615,'http://192.168.5.7:2000/unknown',self.smsconfig['textbelt-key'])
                            console_log.PipeLine_Ok("stop face prossesing timer unknown" +str(datetime.now()-face_processing_pipeline_timer))
                            self.watchdog += 1
                            

                        else:
                            if self.watchdog == 10:
                                console_log.Error("Ending Program Watch Dog over ran!")
                                break
                            
                            if name in self.userList[i]:
                                userinfo = self.userList[i][name]
                                status = userinfo.status
                                name = userinfo.user
                                phone = userinfo.phoneNum

                                if phone == None:
                                    phone = 4123891615

                                #print("User UUID:"+ str(userinfo)+ " "+ str(name) + "   "+ str(status))

                                if (status == 'Admin'):
                                    logging.info(
                                        "got an Admin The name is"+str(name))
                                    Stat.userAdmin(status, name, frame, font, self.imagename,
                                                   self.imagePath, left, right, bottom, top, process_this_frame)
                                    message.sendCapturedImageMessage("eeeep there is an Admin Person Be Good"+" " + "There Name is:" + str(
                                        name), phone, 'http://192.168.5.8:2000/admin', self.smsconfig['textbelt-key'])
                                    console_log.PipeLine_Ok(
                                        "Stping face prossesing timer in admin" + str(datetime.now()-face_processing_pipeline_timer))
                                    self.watchdog += 1
                                    

                                if (status == 'User'):
                                    logging.info(
                                        "got an User Human The name is"+str(name))
                                    Stat.userUser(status=status, name=name, frame=frame, font=font, imagename=self.imagename,
                                                  imagePath=self.imagePath, left=left, right=right, bottom=bottom, top=top, framenum=process_this_frame)
                                    message.sendCapturedImageMessage("eeeep there is an User They Might be evil so um let them in"+"  `"+"There Name is:" + str(
                                        name), 4123891615, 'http://192.168.5.8:2000/user', self.smsconfig['textbelt-key'])
                                    console_log.Warning(
                                        "eeeep there is an User They Might be evil so um let them in"+"  `"+"There Name is:" + str(name))
                                    console_log.PipeLine_Ok(
                                        "Stping face prossesing timer in user" + str(datetime.now()-face_processing_pipeline_timer))
                                    self.watchdog += 1
                                    

                                if (status == 'Unwanted'):
                                    logging.info(
                                        "got an Unwanted Human The name is"+str(name))
                                    Stat.userUnwanted(status=status, name=name, frame=frame, font=font, imagename=self.imagename,
                                                      imagepath=self.imagePath, left=left, right=right, bottom=bottom, top=top, framenum=process_this_frame)
                                    console_log.PipeLine_Ok("Stping face prossesing timer in unwanted" + str(
                                        datetime.now()-face_processing_pipeline_timer))
                                    self.watchdog += 1
                                    #message.sendCapturedImageMessage("eeeep there is an Unwanted Get them away from ME!"+" "+ "There Name is:"+ str(name),phone,'http://192.168.5.8:2000/unwanted',self.smsconfig['textbelt-key'])
                                # print("eeeep there is an Unwanted Get them away from ME!"+" "+ "There Name is:"+ str(name)
                                    # )

                                if(self.getAmountofFaces(face_recognition, frame) > 1):
                                    Stat.userGroup(frame=frame, font=font, imagename=self.imagename,
                                                   imagepath=self.imagePath, left=left, right=right, bottom=bottom, top=top)
                                    console_log.PipeLine_Ok(
                                        "Stping face prossesing timer in Group" + str(datetime.now()-face_processing_pipeline_timer))
                                    #message.sendCapturedImageMessage("eeeep there is Gagle of Peope I dont know what to do",phone,'http://192.168.5.8:2000/group',self.smsconfig['textbelt-key'])
                                
                            else:

                                console_log.Warning(
                                    "not the correct obj in list" + str(self.userList[i]))
                                if(name != userinfo.user):
                                    i+=1
                                else:
                                    console_log.PipeLine_Ok("Users Name seen is "+str(name))
                                    

                    else:

                        console_log.PipeLine_Ok(
                            "Time For non Face processed frames" + str(datetime.now()-face_processing_pipeline_timer))



            else:
                if self.watchdog == 10:
                    console_log.Error("Ending Program Watch Dog over ran!")
                    break
                

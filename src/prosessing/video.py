"""
This is the main (Bulk) possessing done in my opencv Program
TODO: Need to Fix Face loading into Facial Reconition lib
TODO: Need to have a Gstreamer out to asmble an video stream Effecintly to allow user to view it live on web page hehe
TODO: REMOVE ZMQ SOCKET DATA
TODO: ASSINE USERS UUIDS TO MAKE IT EASER
"""


from uuid import uuid1
import uuid
from sqlalchemy.sql.elements import literal

import cardinality
import ast
from collections import OrderedDict
import logging
from numbers import Number

from os.path import join
import shutil
from tokenize import Double, String
import json

import cv2

import face_recognition
import numpy as np
import os
from datetime import datetime
import time
import logging
import zmq
import Config
from time import sleep
import threading
import base64
import json
import math
import Database as db
import wget

import pathlib
from configparser import ConfigParser
from PIL import Image
import SmsHandler
import KnnClassifiyer
# TODOD: add All Config.py Settings that arnt python fiunctions to Database


class VideoProsessing(object):
    logging.basicConfig(filename="/mnt/user/logs/" + datetime.now().strftime(
        "%Y_%m_%d-%I_%M_%S_%p_%s")+".log", level=logging.DEBUG)

    imagename = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p_%s")
    imagePath = "/mnt/user/"
    imagePathusers = "/mnt/user/people/"
    storage_array = []

    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

    video_capture = cv2.VideoCapture(0)



# handles adding data to lists so i can tuppleize it

    # sends Person count info to subscribers


    def send_person_count(self, face_encodings, sock):
        logging.info("[SOCKET PERSON] sending Seen Persons")
        sock.send_string("FACE")
        sock.send_json({"face": str(len(face_encodings))})
        logging.info("[SOCKET PERSON] Sent Seen Persons")

    
    def send_face_compare(self, face_distance, sock):
        logging.info("[SOCKET FACEMATCH] sending Seen Persons")
        sock.send_string("COMPARE")
        sock.send_json({"compare": face_distance})
        logging.info("[SOCKET FACEMATCH] Sent Seen Persons")

    # sends person name to subsecriber
    def send_person_name(self, sock, name):
        logging.info("[SOCKET Name] Sending person seen name")
        sock.send_string("NAME")
        sock.send_json({"name": name})
        logging.info("[SOCKET Name] Sent Person name")

    # saves owner images and sends Frame
    def save_owner(self, imagepath, imagename, frame):
        cv2.imwrite(imagepath + imagename + ".jpg", frame)

    def save_user(self, imagePath, imagename, frame):
        cv2.imwrite(imagePath + "user" + imagename + ".jpg", frame)

    def save_unknown(self, imagepath, imagename, frame):
        cv2.imwrite(imagepath + "unKnownPerson" + imagename + ".jpg", frame)

    def save_group(self, imagepath, imagename, frame):
        cv2.imwrite(imagepath + "Group" + imagename + ".jpg", frame)

    # decodes Json Encoded Data Created From DataList Function to retun image name
    def decodeJsonImageData(self,facedata):
        decodedjson= json.loads(facedata)
        return decodedjson['image']

    def decodeJsonString(self,facedata):
        decodedjson= json.loads(facedata)
        return decodedjson

    # Encodes all the Nessiscary User info into Json String so it can be easly moved arround
    def datalist(self):
        i = 0


        while True:
            # example Json string  [{"name":"Tesla", "age":2, "city":"New York"}]
            print(str("Indext of Data is ")+str(i))
            
            userdata = '{'+str(uuid.uuid1())+":"+'{'+'"name":'+str("[")+str(db.getName(db.getFaces(), i))+str("[")+','+'"status":'+str("[")+str(db.getStatus(db.getFaces(), i)) + str("[")+','+'"image":'+str("[")+str(db.getImageName(db.getFaces(), i))+str("[")+','+'"download_Url":'+str("[")+str(db.getImageUrI(db.getFaces(), i))+str("[")+'}'+'}'

            # prepares Mal Json strings
            basejson = userdata.replace("[", "'")
            finaljson = basejson.replace("'", '"')
            # Final Json  string replacement accoures

            self.storage_array.insert(i, finaljson)

            i += 1

            # Checks to see if i == the database amount hehe
            if(i == db.getAmountOfEntrys()):
                logging.warn("Amout of Entrys are in the array strings are"+str(db.getAmountOfEntrys()))
                return 

    #

    # saves downloaded Image Converted to black and white
    def downloadFacesAndProssesThem(self, logging, userData, filepath, i):
        # Main Storage Array for json strings
        data = userData[i]

        print(" this is the data yaya" + str(data))
        # converts json string into
        user_info = json.loads(data)

        if(not os.path.exists(filepath+user_info['image']+".jpg")):
            wget.download(user_info['download_Url'], str(filepath))
            logging.info('Downloading ' +
                         str(user_info['image'])+', this may take a while...')
            logging.info("output file" +
                         str(user_info['image']+"at" + filepath))

        # this function will load and prepare face encodes  for
    
    

    # Fully Downloades USer Images and Returns No data
    def downloadUserFaces(self, imagePath):

        index = 0
        # gets users names statuses face iamges and the urls from the tuples
        while True:

            self.downloadFacesAndProssesThem(logging, self.datalist(), imagePath, index)
            logging.warn("downloaded"+str(index) +"out of " + str(db.getAmountOfEntrys()))

            index +=1

            if(index == db.getAmountOfEntrys()):
                logging.info("Done Downloading Images UWU....")
                return
        
    # checks usr and json status
    def getUserStatusandCheckStatus(self,ogfacedata):
            i = 0 
            
            while True:
                    
                decodedogjson= json.loads(ogfacedata[i])
                decodedcomparejson= json.loads(ogfacedata[i])
                
                # Simply Checks to see if the 2 json strings equle each
                if(decodedogjson == decodedcomparejson):
                    logging.info("YaY User Json Strings Are Right UwU Now to try to check user status hehe")
                    return decodedcomparejson['status']
                    
                
                # if check fail throws error 
                if(decodedogjson  == None):
                    logging.critical("STRINGS FAILD COMPARISON")
                    raise Exception('FAILD JSON COMPARISON for user status') # Don't! If you catch, likely to hide bugs.

                i+=1
                if(i == db.getAmountOfEntrys):
                    logging.info("finished checking status")
                    return
    
    # gets USer name from Json String 
    def getUserNames(self, datalist):

        i = 0 

        logging.info("Decoding Json String for user name...")
        while True:
            # interpates json string 
            decodedstring = self.decodeJsonString(datalist[i])

            if decodedstring is not None:
                logging.info("Done decoding string sending name to other code...")
                return decodedstring['name']
            i+=1
            
            if(i == db.getAmountOfEntrys):
                logging.info("Done decoding string sending name to other code returning to main code UWU...")
                return

        
                
                # Add names of the ecodings to thw end of list
        '''
        This Function is the Bulk of the Openv Image Prossesing Code
        '''

    def ProcessVideo(self):
        # Sends Sms Message Saying Starting Server
        
        # sets rtsp vsr in python
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

# gets Config file
        print(str(pathlib.Path().absolute())+"/src/prosessing/"+"Config.ini")
        # Read config.ini file
        config_object = ConfigParser()
        config_object.read(str(pathlib.Path().absolute()) +
                           "/src/prosessing/"+"Config.ini")

        logconfig = config_object['LOGGING']
        zmqconfig = config_object['ZMQ']
        opencvconfig = config_object['OPENCV']
        fileconfig = config_object['FILE']
        current_time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p_%s")

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


# sends setup message and sets base image name to the current date mills and image storage path
        sock.send(b"setup")
        logging.info("Setting up cv")

        # Downlaods all the Faces 
        self.downloadUserFaces(VideoProsessing.imagePathusers)
        
        #Trains Knn
        KnnClassifiyer.train("/mnt/user/train",image_files_in_folder,face_recognition,neighbors)
    
        logging.info("Cv setup")

        sock.send(b"starting")

        

        while True:
            

            # graps image to read
            ret, frame = VideoProsessing.video_capture.read()

            # gets video
            fps = int(VideoProsessing.video_capture.get(2))
            width = int(VideoProsessing.video_capture.get(3))   # float `width`
            height = int(VideoProsessing.video_capture.get(4))  # float `height`

            # checks to see if frames are vaild not black or empty
            if(frame == None):
                logging.warning(str(current_time) +"Frame is Not Vaild Skiping...")
            if np.sum(frame) == 0:
                logging.warning(str(current_time) +"Frame is all black Skiping...")
            if (width > 0 and height > 0):
                logging.warn("cannot open Non exsting image")
                print("Broaking Image Uwu It does not Exsit fix")

            # Resize frame of video to 1/4 size for faster face detection processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            
            predictions =KnnClassifiyer.predict(small_frame)
            # Loads Status of people 
            status = self.getUserStatusandCheckStatus(self.datalist())

            """
            This Section is Dedicated to dealing with user Seperatation via the User Stats data tag
            """
            # Display the results
            for name,(top, right, bottom, left) in predictions:
                
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                i = 1
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
                if(not os.path.exists(self.imagePath+self.imagename+".jpg")):

                    self.save_owner(self.imagePath,self.imagename, frame)

                    # sends person info
                    self.send_person_name(sock, name)
                    # send_group_status(sock,"owner")
                  

                # Adult Section add names to here for more adults
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
                    logging.warning("letting in" + name)

                    # checks to see if image exsitis
                    if(not os.path.exists(self.imagePath+"user"+self.imagename+".jpg")):

                        # sends Image and saves image to disk
                        self.save_user(self.imagePath, self.imagename, frame)

                        # sends person info
                        self.send_person_name(sock, name)
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
                    if(not os.path.exists(self.imagePath + "unKnownPerson" + self.imagename + ".jpg")):

                        # sends Image and saves image to disk
                        self.save_unknown(self.imagePath, self.imagename, frame)

                        # sends person info
                        self.send_person_name(sock, name)
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

                    if(not os.path.exists(self.imagePath + "Group" + self.imagename + ".jpg")):

                        # sends Image and saves image to disk
                        self.save_group(self.imagePath, self.imagename, frame)

                        # sends person info
                        self.send_person_name(sock, name)

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
                    if(not os.path.exists(self.imagePath + "unKnownPerson" + self.imagename + ".jpg")):
                        # sends Image and saves image to disk
                        self.save_unknown(self.imagePath, self.imagename, frame)

                        # sends person info
                        self.send_person_name(sock, name)
                        # send_group_status(sock,"Unknown")


                # Display the resulting image
                cv2.imshow("Video", frame)

                # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

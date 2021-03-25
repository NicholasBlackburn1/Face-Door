"""
This is the main (Bulk) possessing done in my opencv Program
"""
from sqlalchemy.sql.elements import literal

import cardinality
from collections import OrderedDict
import logging 
from numbers import Number

from os.path import join
import shutil
from tokenize import Double, String

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

# TODOD: add All Config.py Settings that arnt python fiunctions to Database


class VideoProsessing(object):
    logging.basicConfig(filename="/mnt/user/logs/"+ datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p_%s")+".log", level=logging.DEBUG)
    

# handles adding data to lists so i can tuppleize it 
   

    
    # sends Person count info to subscribers 
    def send_person_count(self,face_encodings, sock):
        logging.info("[SOCKET PERSON] sending Seen Persons")
        sock.send_string("FACE")
        sock.send_json({"face": str(len(face_encodings))})
        logging.info("[SOCKET PERSON] Sent Seen Persons")
        
        # sends Person count info to subscribers 
    def send_owner_count(self,face_encodings, sock):
        logging.info("[SOCKET PERSON] sending Seen Persons")
        sock.send_string("ADMIN")
        sock.send_json({"admin": len(face_encodings)})
        logging.info("[SOCKET PERSON] Sent Seen Persons")

        
        # sends Person count info to subscribers 
    def send_user_count(self,face_encodings, sock):
        logging.info("[SOCKET PERSON] sending Seen Persons")
        sock.send_string("USER")
        sock.send_json({"user": str(len(face_encodings))})
        logging.info("[SOCKET PERSON] Sent Seen Persons")

        
        # sends Person count info to subscribers 
    def send_unkown_count(self,face_encodings, sock):
        logging.info("[SOCKET PERSON] sending Seen Persons")
        sock.send_string("UNKNOWN")
        sock.send_json({"unknown": str(len(face_encodings))})
        logging.info("[SOCKET PERSON] Sent Seen Persons")

    def send_face_compare(self,face_distance,sock):
        logging.info("[SOCKET FACEMATCH] sending Seen Persons")
        sock.send_string("COMPARE")
        sock.send_json({"compare": face_distance})
        logging.info("[SOCKET FACEMATCH] Sent Seen Persons")

    # sends person name to subsecriber 
    def send_person_name(self,sock,name):
        logging.info("[SOCKET Name] Sending person seen name")
        sock.send_string("NAME")
        sock.send_json({"name": name})
        logging.info("[SOCKET Name] Sent Person name")
        
    # saves owner images and sends Frame 
    def save_owner(self, imagepath,imagename,frame):
        cv2.imwrite(imagepath + imagename + ".jpg", frame)
        
    
        
    def save_user(self, imagePath,imagename,frame):
        cv2.imwrite(imagePath + "user" + imagename + ".jpg", frame)
        
        
        
    def save_unknown(self,imagepath,imagename,frame):
        cv2.imwrite(imagepath + "unKnownPerson" + imagename + ".jpg", frame)
        
        
    def save_group(self,imagepath,imagename,frame):
        cv2.imwrite(imagepath + "Group" + imagename + ".jpg", frame)
 
      
    def datalist(self):
        i = 0
        storage_array=[]
    
        while True:
            print(str("Indext of Data is ")+str(i))
            userdata = str({"name":db.getName(db.getFaces(),i),"status":db.getStatus(db.getFaces(),i),"image":db.getImageName(db.getFaces(),i),"download_Url":db.getImageUrI(db.getFaces(),i)})
            print(userdata)

            storage_array.insert(i,userdata)
            print("Array with all strings in it"+str(storage_array))

            i+=1

            if(str(i) == str(db.getAmountOfEntrys())):
                print("Full Storage Array"+str(storage_array))
                return storage_array
                
            
    
    # saves downloaded Image Converted to black and white 
    def downloadFacesAndProssesThem(self,logging,imagename,imageurl,filepath ):
        if(not os.path.exists(filepath+imagename+".jpg")):
            wget.download(imageurl, str(filepath))
            logging.info('Downloading '+str(imagename)+', this may take a while...')
        '''
        This Function is the Bulk of the Openv Image Prossesing Code
        '''

    def ProcessVideo(self):
        
        # sets rtsp vsr in python 
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

# gets Config file
        print(str(pathlib.Path().absolute())+"/src/prosessing/"+"Config.ini")
        # Read config.ini file
        config_object = ConfigParser()
        config_object.read(str(pathlib.Path().absolute())+"/src/prosessing/"+"Config.ini")
        
        
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
        imagename = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p_%s")
        imagePath = "/mnt/user/"
        imagePathusers = "/mnt/user/people/"


    # gets users names statuses face iamges and the urls from the tuples
        self.datalist()

        self.downloadFacesAndProssesThem(logging,userdict.s,userdict['imageurl'],fileconfig['faceStorage'])
        print("output file" +str(userdict['image']))
        

        
        # TODO: Change this into the ipcamera Stream using the config.
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        
        video_capture = cv2.VideoCapture('udpsrc port=5006 ! application/x-rtp, encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegparse ! jpegdec ! autovideosink', cv2.CAP_GSTREAMER)
        userloaded = face_recognition.load_image_file(imagePathusers+image)

        # defines all known faces for the system and how many times the dlib will train it self with that image takes min 49 sec to train
       # EthanEncode = face_recognition.face_encodings(Ethan, num_jitters=75)[0]
        userEncode = face_recognition.face_encodings(userloaded)[0]

        # Add names of the ecodings to thw end of list
        known_face_encodings = [userEncode]

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []

        process_this_frame = True
        logging.info("Cv setup")

        sock.send(b"starting")

        while True:
            #graps image to read
            ret, frame = video_capture.read()

            # gets video 
            fps = int(video_capture.get(2))
            width  = int(video_capture.get(3))   # float `width`
            height = int(video_capture.get(4))  # float `height`

            #checks to see if frames are vaild not black or empty
            if(frame == None):
                logger.warning(str(current_time)+"Frame is Not Vaild Skiping...")
            else:
                if np.sum(frame) == 0:
                     logger.warning(str(current_time)+"Frame is all black Skiping...")

            # Resize frame of video to 1/4 size for faster face detection processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            
             # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            
            # Only process every other frame of video to save time
            if True:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame,model="cnn")
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations
                )

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(
                        known_face_encodings, face_encoding, tolerance=0.6932
                    )
                    name = opencvconfig['unreconizedPerson']
                    
                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distance = face_recognition.face_distance(
                        known_face_encodings, face_encoding
                    )
                    best_match_index = np.argmin(face_distance)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                
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
                if(not os.path.exists(imagePath+imagename+".jpg")):
              
                        self.save_owner(imagePath, imagename,frame)

                        # sends person info
                        self.send_person_name(sock,name)
                        # send_group_status(sock,"owner")
                        self.send_owner_count(face_encodings,sock)
                    
                    
                # Adult Section add names to here for more adults
                if (status == 'User'):
                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 2)

                    font = cv2.FONT_HERSHEY_DUPLEX

                    cv2.putText(frame, name, (left, top), font, 0.5, (255, 255, 255), 1)
                    cv2.putText(
                        frame, "Known Person..", (0, 430), font, 0.5, (255, 255, 255), 1
                    )
                    cv2.putText(
                        frame, status, (0, 450), font, 0.5, (255, 255, 255), 1
                    )
                    cv2.putText(frame, name, (0, 470), font, 0.5, (255, 255, 255), 1)

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
                    if(not os.path.exists(imagePath+"user"+imagename+".jpg")):
                 
                        # sends Image and saves image to disk
                         self.save_user(imagePath,imagename,frame)     
                                        
                        # sends person info
                         self.send_person_name(sock,name)
                    # send_group_status(sock,"user")
                         self.send_user_count(face_encodings,sock)
                    

                if (status =='Unwanted'):
                   
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, name, (left, top), font, 0.5, (255, 255, 255), 1)
                    # Distance info
                    cv2.putText(frame, status, (0, 450),
                                font, 0.5, (255, 255, 255), 1)
                    cv2.putText(frame, name, (0, 470), font,
                                0.5, (255, 255, 255), 1)


                    
                    logging.warning("not letting in" + name)

                    
                    # checks to see if image exsitis
                    if(not os.path.exists(imagePath + "unKnownPerson" + imagename + ".jpg")):
               
                        # sends Image and saves image to disk
                         self.save_unknown(imagePath,imagename,frame)                 
                   
                        # sends person info
                         self.send_person_name(sock,name)
                        # send_group_status(sock,"Unknown")
                         self.send_unkown_count(face_encodings,sock)                    
                elif (
                    len(face_locations) >= 2
                ):

                    cv2.rectangle(
                        frame, (left, top), (right, bottom), (255, 0, 255), 2
                    )

                    font = cv2.FONT_HERSHEY_DUPLEX

                    cv2.putText(frame, name, (left, top), font, 0.5, (255, 255, 255), 1)
                   
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

                    
                    if(not os.path.exists(imagePath + "Group" + imagename + ".jpg") ):
                     
                        # sends Image and saves image to disk
                         self.save_group(imagePath,imagename,frame)                 
            
                        # sends person info
                         self.send_person_name(sock,name)
                    
                elif (name == opencvconfig['unreconizedPerson']):
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, name, (left, top), font, 0.5, (255, 255, 255), 1)
                    # Distance info
                    cv2.putText(frame, opencvconfig['unreconizedPerson'], (0, 450),
                                font, 0.5, (255, 255, 255), 1)
                    cv2.putText(frame, name, (0, 470), font,
                                0.5, (255, 255, 255), 1)

                
                    
                    logging.warning("not letting in" + name)

                    
                    # checks to see if image exsitis
                    if(not os.path.exists(imagePath + "unKnownPerson" + imagename + ".jpg")):
                        # sends Image and saves image to disk
                         self.save_unknown(imagePath,imagename,frame)                 
                   
                        # sends person info
                         self.send_person_name(sock,name)
                        # send_group_status(sock,"Unknown")
                         self.send_unkown_count(face_encodings,sock)                    



                    
                    logging.warning("not letting in" + name)
                        
                # Display the resulting image
                cv2.imshow("Video", frame)
             
             
           
            
                # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


           
  
  
"""
This is the main (Bulk) possessing done in my opencv Program
"""
from logging import log
from os import sendfile, wait
from os.path import join

import cv2
from zmq.sugar import socket
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
import Database

#TODOD: add All Config.py Settings that arnt python fiunctions to Database
class VideoProsessing(object):
    logging.basicConfig(filename="/mnt/user/cv.log", level=logging.DEBUG)
    
                    
    def ProcessVideo():
       
        known_face_names = []
        known_user_status = []
        known_user_images = []

        # Database connection handing 
        logging.info("Connecting to the Database Faces")
        logging.debug(Database.Database.getFaces())
        logging.info("connected to database Faces")
        

        ZMQURI = str("tcp://"+ipaddr+":"+port)
        
        ctx = zmq.Context()
        sock = ctx.socket(zmq.PUB)
        sock.bind(ZMQURI)

        sock.send(b"setup")
        logging.info("Setting up cv")
        imagename = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p_%s")
        imagePath = "/mnt/user/"
        
        

        # TODO: Change this into the ipcamera Stream.
        video_capture = cv2.VideoCapture(0)
        video_capture.set(cv2.CAP_PROP_FPS, 30)
        
        
        name, status,image =setLists(known_face_names,known_user_status,known_user_images)[0]
        print(name,status, image)
        
        userimage = face_recognition.load_image_file(image)
        # add more faces to be trained to be reconized

        # defines all known faces for the system and how many times the dlib will train it self with that image takes min 49 sec to train 
       # EthanEncode = face_recognition.face_encodings(Ethan, num_jitters=75)[0]
        userEncode = face_recognition.face_encodings(userimage, num_jitters=75)[0]
         
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
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgbframe = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgbframe)
                face_encodings = face_recognition.face_encodings(
                    rgbframe, face_locations
                )

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(
                        known_face_encodings, face_encoding, tolerance=0.6932
                    )
                    name = Config.UNRECONIZED
                    

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
                if (
                    status == 'Admin'
                ):
                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                    font = cv2.FONT_HERSHEY_DUPLEX

                    cv2.putText(frame, name, (left, top), font, 0.5, (255, 255, 255), 1)
                    cv2.putText(
                        frame, "Known Person..", (0, 430), font, 0.5, (255, 255, 255), 1
                    )
                    cv2.putText(frame, status, (0, 450), font, 0.5, (255, 255, 255), 1)
                    cv2.putText(frame, name, (0, 470), font, 0.5, (255, 255, 255), 1)

                    ## Distance info
                    cv2.putText(
                        frame,
                        str(matches),
                        (400, 469),
                        font,
                        0.5,
                        (255, 255, 255),
                        1,
                    )
                    
                    
                    logging.warning("letting in" + name)

                    # sends Image and saves image to disk
                    save_owner(sock,imagePath,imagename,frame)                 
                    
                    # sends person info
                    send_person_name(sock,name)
                    #send_group_status(sock,"owner")
                    send_owner_count(face_encodings,sock)
                  
                    
                # Adult Section add names to here for more adults
                elif (
                    status == 'User'
                ):
                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

                    font = cv2.FONT_HERSHEY_DUPLEX

                    cv2.putText(frame, name, (left, top), font, 0.5, (255, 255, 255), 1)
                    cv2.putText(
                        frame, "Known Person..", (0, 430), font, 0.5, (255, 255, 255), 1
                    )
                    cv2.putText(
                        frame, status, (0, 450), font, 0.5, (255, 255, 255), 1
                    )
                    cv2.putText(frame, name, (0, 470), font, 0.5, (255, 255, 255), 1)

                    ## Distance info
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
                    
            
                    # sends Image and saves image to disk
                    save_parent(sock,imagePath,imagename,frame)                 
                    # sends person info
                    send_person_name(sock,name)
                   # send_group_status(sock,"Parent")
                    send_parent_count(face_encodings,sock)
                    

                elif (status == 'unknown' or status =='Unwanted'):
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, name, (left, top), font, 0.5, (255, 255, 255), 1)
                    ## Distance info
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
                        1,
                    )
                    
                    logging.warning("not letting in" + name)
                      
                    # sends Image and saves image to disk
                    save_unknown(sock,imagePath,imagename,frame)                 
                   
                    # sends person info
                    send_person_name(sock,name)
                   # send_group_status(sock,"Unknown")
                    send_unkown_count(face_encodings,sock)                    


                elif (
                    status == 'Admin' and status == 'User' and status == 'unknown' or status == 'Unwanted'
                ):

                    cv2.rectangle(
                        frame, (left, top), (right, bottom), (255, 103, 100), 2
                    )

                    font = cv2.FONT_HERSHEY_DUPLEX

                    cv2.putText(frame, name, (left, top), font, 0.5, (255, 255, 255), 1)
                    cv2.putText(
                        frame, "Known Person..", (0, 430), font, 0.5, (255, 255, 255), 1
                    )
                    cv2.putText(frame, "Group", (0, 450), font, 0.5, (255, 255, 255), 1)
                    cv2.putText(frame, "Known and Unknown People", (0, 470), font, 0.5, (255, 255, 255), 1)

                    ## Distance info
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
                        1,
                    )
                    logging.warning("Letting in group" + name)
                     
                    # sends Image and saves image to disk
                    save_group(sock,imagePath,imagename,frame)                 
            
                    # sends person info
                    send_person_name(sock,name)
                   
            # Display the resulting image
            cv2.imshow("Video", frame)
            logging.warning("no one is here")
             
           
            
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release handle to the webcam
        video_capture.release()


# handles adding data to lists so i can tuppleize it 
def setLists(known_face_names,known_user_status,known_user_images):
    i = 0
    known_face_names.append(Database.Database.getName(Database.Database.getFaces(),i))
    known_user_status.append(Database.Database.getStatus(Database.Database.getFaces(),i))
    known_user_images.append(Database.Database.getImage(Database.Database.getFaces(),i))
    data  =zip(known_face_names,known_user_status,known_user_images)
    output = tuple(data)
    return output
            

# Sends a file name obver to subscribers  
def send_file(sock,imagename):
    logging.info("[SOCKET-IMAGE] sending image")
    sock.send_string("IMAGE", flags=zmq.SNDMORE)
    sock.send_json({"image":imagename+".jpg"})
    logging.info("[SOCKET-IMAGE] image sent\n")
    
#sends Person count info to subscribers 
def send_person_count(face_encodings, sock):
    logging.info("[SOCKET PERSON] sending Seen Persons")
    sock.send_string("FACE", flags=zmq.SNDMORE)
    sock.send_json({"face": str(len(face_encodings))})
    logging.info("[SOCKET PERSON] Sent Seen Persons")
    
    #sends Person count info to subscribers 
def send_owner_count(face_encodings, sock):
    logging.info("[SOCKET PERSON] sending Seen Persons")
    sock.send_string("ADMIN", flags=zmq.SNDMORE)
    sock.send_json({"admin": len(face_encodings)})
    logging.info("[SOCKET PERSON] Sent Seen Persons")

    
    #sends Person count info to subscribers 
def send_parent_count(face_encodings, sock):
    logging.info("[SOCKET PERSON] sending Seen Persons")
    sock.send_string("USER", flags=zmq.SNDMORE)
    sock.send_json({"user": str(len(face_encodings))})
    logging.info("[SOCKET PERSON] Sent Seen Persons")

    
    #sends Person count info to subscribers 
def send_unkown_count(face_encodings, sock):
    logging.info("[SOCKET PERSON] sending Seen Persons")
    sock.send_string("UNKNOWN", flags=zmq.SNDMORE)
    sock.send_json({"uknown": str(len(face_encodings))})
    logging.info("[SOCKET PERSON] Sent Seen Persons")

def send_face_compare(face_distance,sock):
    logging.info("[SOCKET FACEMATCH] sending Seen Persons")
    sock.send_string("COMPARE", flags=zmq.SNDMORE)
    sock.send_json({"compare": face_distance})
    logging.info("[SOCKET FACEMATCH] Sent Seen Persons")

"""
#sends Person Status info to subscribers 
def send_group_status(sock,group_status):
    logging.info("[SOCKET STATUS] sending Person Group status")
    sock.send_string("GROUP",flags=zmq.SNDMORE)
    sock.send_json({Config.GROUP: group_status})
    logging.info("[SOCKET STATUS] Sent Person Group status")
"""
    
#sends person name to subsecriber 
def send_person_name(sock,name):
    logging.info("[SOCKET Name] Sending person seen name")
    sock.send_string("NAME", flags=zmq.SNDMORE)
    sock.send_json("name": name})
    logging.info("[SOCKET Name] Sent Person name")
    
# saves owner images and sends Frame 
def save_owner(sock, imagepath,imagename,frame):
    cv2.imwrite(imagepath + imagename + ".jpg", frame)
    send_file(sock,imagename)
  
    
def save_parent(sock, imagePath,imagename,frame):
    cv2.imwrite(imagePath + "Parent" + imagename + ".jpg", frame)
    send_file(sock,"Parent"+imagename)
    
    
def save_unknown(sock, imagepath,imagename,frame):
    cv2.imwrite(imagepath + "unKnownPerson" + imagename + ".jpg", frame)
    send_file(sock,"unKnownPerson"+imagename)
    
def save_group(sock, imagepath,imagename,frame):
    cv2.imwrite(imagepath + "Group" + imagename + ".jpg", frame)
    send_file(sock,"Group"+imagename)


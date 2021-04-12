"""
This is the main (Bulk) possessing done in my opencv Program
TODO: Need to Fix Face loading into Facial Reconition lib
TODO: Need to have a Gstreamer out to asmble an video stream Effecintly to allow user to view it live on web page hehe
TODO: REMOVE ZMQ SOCKET DATA
"""


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
from face_recognition.face_recognition_cli import image_files_in_folder
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
from sklearn import neighbors
import pickle
# TODOD: add All Config.py Settings that arnt python fiunctions to Database


class VideoProsessing(object):
    logging.basicConfig(filename="/mnt/user/logs/" + datetime.now().strftime(
        "%Y_%m_%d-%I_%M_%S_%p_%s")+".log", level=logging.DEBUG)

    imagename = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p_%s")
    imagePath = "/mnt/user/"
    imagePathusers = "/mnt/user/people/"

    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

    video_capture = cv2.VideoCapture(0)



# handles adding data to lists so i can tuppleize it

    # sends Person count info to subscribers


    def send_person_count(self, face_encodings, sock):
        logging.info("[SOCKET PERSON] sending Seen Persons")
        sock.send_string("FACE")
        sock.send_json({"face": str(len(face_encodings))})
        logging.info("[SOCKET PERSON] Sent Seen Persons")

        # sends Person count info to subscribers
    def send_owner_count(self, face_encodings, sock):
        logging.info("[SOCKET PERSON] sending Seen Persons")
        sock.send_string("ADMIN")
        sock.send_json({"admin": len(face_encodings)})
        logging.info("[SOCKET PERSON] Sent Seen Persons")

        # sends Person count info to subscribers

    def send_user_count(self, face_encodings, sock):
        logging.info("[SOCKET PERSON] sending Seen Persons")
        sock.send_string("USER")
        sock.send_json({"user": str(len(face_encodings))})
        logging.info("[SOCKET PERSON] Sent Seen Persons")

        # sends Person count info to subscribers

    def send_unkown_count(self, face_encodings, sock):
        logging.info("[SOCKET PERSON] sending Seen Persons")
        sock.send_string("UNKNOWN")
        sock.send_json({"unknown": str(len(face_encodings))})
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

        storage_array = []

        while True:
            # example Json string  [{"name":"Tesla", "age":2, "city":"New York"}]
            print(str("Indext of Data is ")+str(i))
            
            userdata = '{"name":'+str("[")+str(db.getName(db.getFaces(), i))+str("[")+','+'"status":'+str("[")+str(db.getStatus(db.getFaces(), i)) + str(
                "[")+','+'"image":'+str("[")+str(db.getImageName(db.getFaces(), i))+str("[")+','+'"download_Url":'+str("[")+str(db.getImageUrI(db.getFaces(), i))+str("[")+'}'

            # prepares Mal Json strings
            basejson = userdata.replace("[", "'")
            finaljson = basejson.replace("'", '"')
            # Final Json  string replacement accoures

            storage_array.insert(i, finaljson)

            i += 1

            # Checks to see if i == the database amount hehe
            if(i == db.getAmountOfEntrys()):
                logging.warn("Amout of Entrys are in the array strings are"+str(db.getAmountOfEntrys()))
                return storage_array

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
    
    #Creates Training File Structure For Knn 
    def createTrainingDir(self,trainingdir,datalist):
        i = 0
        if(trainingdir == None):
            os.mkdir(trainingdir)
            while True:
                os.chdir(trainingdir+self.getUserNames(datalist))
                i+=1
                if(i == db.getAmountOfEntrys):
                    logging.info("Done Creating User Dirs")
                return

    # this function will load and prepare face encodes  for knn model so i can efficiently load and run face rec
    def knnfaceModeltrain(self,train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):
   
            """
            Trains a k-nearest neighbors classifier for face recognition.
            :param train_dir: directory that contains a sub-directory for each known person, with its name.
            (View in source code to see train_dir example tree structure)
            Structure:
                <train_dir>/
                ├── <person1>/
                │   ├── <somename1>.jpeg
                │   ├── <somename2>.jpeg
                │   ├── ...
                ├── <person2>/
                │   ├── <somename1>.jpeg
                │   └── <somename2>.jpeg
                └── ...
            :param model_save_path: (optional) path to save model on disk
            :param n_neighbors: (optional) number of neighbors to weigh in classification. Chosen automatically if not specified
            :param knn_algo: (optional) underlying data structure to support knn.default is ball_tree
            :param verbose: verbosity of training
            :return: returns knn classifier that was trained on the given data.
            """
            X = []
            y = []

            # Loop through each person in the training set
            for class_dir in os.listdir(train_dir):
                if not os.path.isdir(os.path.join(train_dir, class_dir)):
                    continue

                # Loop through each training image for the current person
                for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
                    image = face_recognition.load_image_file(img_path)
                    face_bounding_boxes = face_recognition.face_locations(image)

                    if len(face_bounding_boxes) != 1:
                        # If there are no people (or too many people) in a training image, skip the image.
                        if verbose:
                            print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
                    else:
                        # Add face encoding for current image to the training set
                        X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                        y.append(class_dir)

            # Determine how many neighbors to use for weighting in the KNN classifier
            if n_neighbors is None:
                n_neighbors = int(round(math.sqrt(len(X))))
                if verbose:
                    print("Chose n_neighbors automatically:", n_neighbors)

            # Create and train the KNN classifier
            knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
            knn_clf.fit(X, y)

            # Save the trained KNN classifier
            if model_save_path is not None:
                with open(model_save_path, 'wb') as f:
                    pickle.dump(knn_clf, f)

            return knn_clf

    def predictKnnFaces(X_frame, knn_clf=None, model_path=None, distance_threshold=0.5):
        """
        Recognizes faces in given image using a trained KNN classifier
        :param X_frame: frame to do the prediction on.
        :param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
        :param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
        :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
            of mis-classifying an unknown person as a known one.
        :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
            For faces of unrecognized persons, the name 'unknown' will be returned.
        """
        if knn_clf is None and model_path is None:
            raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

        # Load a trained KNN model (if one was passed in)
        if knn_clf is None:
            with open(model_path, 'rb') as f:
                knn_clf = pickle.load(f)

        X_face_locations = face_recognition.face_locations(X_frame)

        # If no faces are found in the image, return an empty result.
        if len(X_face_locations) == 0:
            return []

        # Find encodings for faces in the test image
        faces_encodings = face_recognition.face_encodings(X_frame, known_face_locations=X_face_locations)

        # Use the KNN model to find the best matches for the test face
        closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
        return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]
                

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
        known_face_encodings = []

        # gets known face encodings 
        known_face_encodings = ( self.loadFacesIntoFacialReconition())
        
    
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        
        logging.info("Cv setup")

        sock.send(b"starting")

        while True:
            # adds list of names to Facial Reconition subsystem 
            face_names.append((self.getUserNames(self.datalist())))

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
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:,:,0]
            # Only process every other frame of video to save time
            if True:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(
                    rgb_small_frame, model="cnn")
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations
                )

                
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(
                        0, face_encoding, tolerance=0.6932
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

            # Loads Status of people 
            status = self.getUserStatusandCheckStatus(self.datalist())

            """
            This Section is Deticated to dealing with user Seperatation via the User Stats data tag
            """
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

                    self.save_owner(imagePath, imagename, frame)

                    # sends person info
                    self.send_person_name(sock, name)
                    # send_group_status(sock,"owner")
                    self.send_owner_count(face_encodings, sock)

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
                    if(not os.path.exists(imagePath+"user"+imagename+".jpg")):

                        # sends Image and saves image to disk
                        self.save_user(imagePath, imagename, frame)

                        # sends person info
                        self.send_person_name(sock, name)
                    # send_group_status(sock,"user")
                        self.send_user_count(face_encodings, sock)

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
                    if(not os.path.exists(imagePath + "unKnownPerson" + imagename + ".jpg")):

                        # sends Image and saves image to disk
                        self.save_unknown(imagePath, imagename, frame)

                        # sends person info
                        self.send_person_name(sock, name)
                        # send_group_status(sock,"Unknown")
                        self.send_unkown_count(face_encodings, sock)
                elif (
                    len(face_locations) >= 2
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

                    if(not os.path.exists(imagePath + "Group" + imagename + ".jpg")):

                        # sends Image and saves image to disk
                        self.save_group(imagePath, imagename, frame)

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

                    logging.warning("not letting in" + name)

                    # checks to see if image exsitis
                    if(not os.path.exists(imagePath + "unKnownPerson" + imagename + ".jpg")):
                        # sends Image and saves image to disk
                        self.save_unknown(imagePath, imagename, frame)

                        # sends person info
                        self.send_person_name(sock, name)
                        # send_group_status(sock,"Unknown")
                        self.send_unkown_count(face_encodings, sock)

                    logging.warning("not letting in" + name)

                # Display the resulting image
                cv2.imshow("Video", frame)

                # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

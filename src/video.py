"""
This is the main (Bulk) possessing done in my opencv Program
"""
from os.path import join
import threading
from PIL.Image import NONE
import cv2
import face_recognition
import numpy as np
import os
from notify_run import Notify
from datetime import datetime
import time
from numpy.core.arrayprint import DatetimeFormat

notify = Notify()

imagename = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
imagePath = "/mnt/user/"

thread = threading.Thread(target=notify.send("Opencv Startinging..."))
thread.start()
thread.join()
# doorcontrol.setup()

# TODO: Change this into the ipcamera Stream.
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FPS, 5)
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc("M", "J", "P", "G")
out = cv2.VideoWriter(imagePath + imagename + ".avi", fourcc, 5.0, (640, 480))
# initialize WebGear app with suitable video file (for e.g `foo.mp4`)


known_face_names = [
    "Ethan Wagner",
    "Nicholas Blackburn",
    "nicks Mom",
    "Ethans mom"
]  #Ethan Grandpa"]

Ethan = face_recognition.load_image_file(os.path.dirname(__file__) + "/ethan.jpg")
Nicholas = face_recognition.load_image_file(os.path.dirname(__file__) + "/nick.jpg")
Nicksmom = face_recognition.load_image_file(os.path.dirname(__file__) + "/NicksMom.jpg")
EthansMom = face_recognition.load_image_file(
    os.path.dirname(__file__) + "/ethansMom.jpg"
)


EthanEncode = face_recognition.face_encodings(Ethan)[0]
NicholasEncode = face_recognition.face_encodings(Nicholas)[0]
NicksMom = face_recognition.face_encodings(Nicksmom)[0]
Ethansmom = face_recognition.face_encodings(EthansMom)[0]


known_face_encodings = [EthanEncode, NicholasEncode, NicksMom, Ethansmom]


# Initialize some variables
ace_locations = []
face_encodings = []
face_names = []

process_this_frame = True
thread = threading.Thread(target=notify.send("Opencv Started..."))
thread.start()
thread.join()

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
                known_face_encodings, face_encoding
            )
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding
            )
            best_match_index = np.argmin(face_distances)
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

        if name == "Nicholas Blackburn" or name == "Ethan Wagner":
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            font = cv2.FONT_HERSHEY_DUPLEX

            cv2.putText(frame, name, (left, top), font, 0.5, (255, 255, 255), 1)
            cv2.putText(
                frame, "Known Person..", (0, 430), font, 0.5, (255, 255, 255), 1
            )
            cv2.putText(frame, "Owner", (0, 450), font, 0.5, (255, 255, 255), 1)
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
                1,
            )
            
            cv2.imwrite(imagePath + imagename + ".jpg", frame)
            time.sleep(1.5)
            thread = threading.Thread(target=notify.send(message="Letting in" + name ))
            thread.start()
            thread.join()

        #  doorcontrol.doorOpen()
        #  doorcontrol.alarmOff()

        elif (
            name == "ethan's Mom"
            or name == "nicks Mom"
            or name == "ethansgrandpa"
            and not name == "Unknown"
        ):
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

            font = cv2.FONT_HERSHEY_DUPLEX

            cv2.putText(frame, name, (left, top), font, 0.5, (255, 255, 255), 1)
            cv2.putText(
                frame, "Known Person..", (0, 430), font, 0.5, (255, 255, 255), 1
            )
            cv2.putText(frame, "Parent", (0, 450), font, 0.5, (255, 255, 255), 1)
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
                1,
            )
            cv2.imwrite(imagePath + "parens" + imagename + ".jpg", frame)
            time.sleep(1.5)
            thread = threading.Thread(target=notify.send(message="Letting in" + name))
            thread.start()
            thread.join()
            # doorcontrol.doorOpen()
            # doorcontrol.alarmOff()
     
        elif name == "Unknown":
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left, top), font, 0.5, (255, 255, 255), 1)
            cv2.putText(
                frame,
                "Unknown Person sound Alarm...",
                (0, 475),
                font,
                0.5,
                (255, 255, 255),
                1,
            )
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
            cv2.imwrite(imagePath + "unKnownPerson" + imagename + ".jpg", frame)
            out.write(frame)
            time.sleep(1.5)
            thread = threading.Thread(
                target=notify.send(message="Unknown Person Sound Alarm")
            )
            thread.start()
            thread.join()
            out.release()
        # doorcontrol.doorClose()
        # doorcontrol.alarmOn()

    # Display the resulting image
   # cv2.imshow("Video", frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release handle to the webcam
out.release()
video_capture.release()
cv2.destroyAllWindows()

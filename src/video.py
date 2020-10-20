import cv2
import face_recognition
import numpy as np
import os

# testing 
video_capture = cv2.VideoCapture(0, cv2.CAP_V4L)


image = ["ethan.jpg","nick.jpg","ethansmom.jpg","NicksMom.jpg","ethansgrandpa.jpg"]
known_face_names = ["Ethan Wagner", "Nicholas Blackburn","nicks Mom"]   #"ethan's Mom", "nicks Mom", "Ethan Grandpa"]

Ethan = face_recognition.load_image_file(os.path.dirname(__file__)+"/ethan.jpg")
Nicholas = face_recognition.load_image_file(os.path.dirname(__file__)+"/nick.jpg")


Nicksmom = face_recognition.load_image_file(os.path.dirname(__file__)+"/NicksMom.jpg")



EthanEncode = face_recognition.face_encodings(Ethan)[0]
NicholasEncode = face_recognition.face_encodings(Nicholas)[0]
NicksMom = face_recognition.face_encodings(Nicksmom)[0]

#EthansMom = face_recognition.load_image_file(image[2])


known_face_encodings = [
    EthanEncode, NicholasEncode, NicksMom
]



# Initialize some variables
ace_locations = []
face_encodings = []
face_names = []

process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame,(0, 0),fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
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
        
       
        if(name == "Nicholas Blackburn" or name == "Ethan Wagner"):
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255,0 ), 2)
            
                font = cv2.FONT_HERSHEY_DUPLEX
            
                cv2.putText(frame, name, (left,top), font, .5, (255, 255, 255), 1)
                cv2.putText(frame, "Known Person..", (0,430), font, .5, (255, 255, 255), 1)
                cv2.putText(frame, "Owner", (0,450), font, .5, (255, 255, 255), 1)
                cv2.putText(frame, name, (0,470), font, .5, (255, 255, 255), 1)
            
                ## Distance info
                cv2.putText(frame, "T&B"+ str(top) +","+str(bottom), (474,430), font, .5, (255, 255, 255), 1)
                cv2.putText(frame, "L&R" + str(left) + "," +str(right), (474,450), font, .5, (255, 255, 255), 1)
                
        elif(name == "ethan's Mom" or name == "nicks Mom" or name == "ethansgrandpa" and not name == "Unknown" ):
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (255,0,0 ), 2)
                    
                font = cv2.FONT_HERSHEY_DUPLEX
                    
                cv2.putText(frame, name, (left,top), font, .5, (255, 255, 255), 1)
                cv2.putText(frame, "Known Person..", (0,430), font, .5, (255, 255, 255), 1)
                cv2.putText(frame, "Parent", (0,450), font, .5, (255, 255, 255), 1)
                cv2.putText(frame, name, (0,470), font, .5, (255, 255, 255), 1)
                    
                    ## Distance info
                cv2.putText(frame, "T&B"+ str(top) +","+str(bottom), (474,430), font, .5, (255, 255, 255), 1)
                cv2.putText(frame, "L&R" + str(left) + "," +str(right), (474,450), font, .5, (255, 255, 255), 1)
                    
        elif(name == "Unknown"):
           font = cv2.FONT_HERSHEY_DUPLEX
           cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255 ), 2)
           cv2.putText(frame, name, (left,top), font, .5, (255, 255, 255), 1)
           cv2.putText(frame, "Unknown Person sound Alarm...", (0,475), font, .5, (255, 255, 255), 1)
           ## Distance info
           cv2.putText(frame, "T&B"+ str(top) +","+str(bottom), (474,430), font, .5, (255, 255, 255), 1)
           cv2.putText(frame, "L&R" + str(left) + "," +str(right), (474,450), font, .5, (255, 255, 255), 1)
            

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
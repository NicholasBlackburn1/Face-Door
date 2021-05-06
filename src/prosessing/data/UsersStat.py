"""
this file is for holding the user stats action
"""
import logging
import os
import cv2




def send_person_name(sock, name):
    logging.info("[SOCKET Name] Sending person seen name")
    sock.send_string("NAME")
    sock.send_json({"name": name})
    logging.info("[SOCKET Name] Sent Person name")


# saves owner images and sends Frame
def saveImage(imagepath, imagename, frame):
    cv2.imwrite(imagepath + imagename + ".jpg", frame)


# this is for Handling User Admin Stats
def userAdmin(sock,status,name,frame,font,imagename,imagePath,left,right,bottom,top):
    if (status == 'Admin'):
            print(status)
            # Draw a box around the face
            cv2.rectangle(frame, (left, top),
                        (right, bottom), (0, 255, 0), 2)


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
            if(not os.path.exists(imagePath+"Admin/"+imagename+".jpg")):

                saveImage(imagePath+"Admin/",
                            imagename, frame)

                # sends person info
                send_person_name(sock, name)
                # send_group_status(sock,"owner")


 # User Grade Status
 # this is for Handling User Stats
def userUser(sock,status,name,frame,font,imagename,imagePath,left,right,bottom,top):
    if (status == 'User'):
        # Draw a box around the face
        cv2.rectangle(frame, (left, top),
                    (right, bottom), (255, 255, 0), 2)


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
        if(not os.path.exists(imagePath+"User/"+imagename+".jpg")):

            # sends Image and saves image to disk
            saveImage(imagePath+"User/",imagename, frame)

            # sends person info
            send_person_name(sock, name)
        
        #


# Handles Unwanted Usr Stats
def userUnwantedOrGroup(sock,status,name,frame,faces,font,imagename,imagePath,left,right,bottom,top):
        if (status == 'Unwanted'):
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
            if(not os.path.exists(imagePath+"Unwanted/" + imagename + ".jpg")):

                # sends Image and saves image to disk
                saveImage(imagePath+"Unwanted/",
                            imagename, frame)

                # sends person info
                send_person_name(sock, name)
                # send_group_status(sock,"Unknown")
        elif (
            faces >= 2
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

            if(not os.path.exists(imagePath + "Group/" + imagename + ".jpg")):

                # sends Image and saves image to disk
                saveImage(imagePath + "Group/",
                            imagename, frame)
                send_person_name(sock, name)

                # sends person info




# Handles unKnown User
def userUnknown(sock,status,opencvconfig,name,frame,font,imagePath,imagename,left,right,bottom,top):
    if (name == opencvconfig['unreconizedPerson'] or status == None):
                            
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
                            if(not os.path.exists(imagePath + "unknown/" +imagename + ".jpg")):
                                # sends Image and saves image to disk
                                saveImage(imagePath+"unknown/",imagename, frame)

                                # sends person info
                                send_person_name(sock, name)
                                # send_group_status(sock,"Unknown")
                            
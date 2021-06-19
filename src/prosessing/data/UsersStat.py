"""
this file is for holding the user stats action
"""
import logging
import os
import cv2
import utils.textColors as console_log




def send_person_name(sock, name):
    console_log.PipeLine_Ok("[SOCKET Name] Sending person seen name")
    sock.send_string("NAME")
    sock.send_json({"name": name})
    console_log.PipeLine_Ok("[SOCKET Name] Sent Person name")


# saves owner images and sends Frame
def saveImage(imagepath, imagename, frame):
    cv2.imwrite(imagepath + imagename + ".jpg", frame)


# this is for Handling User Admin Stats
def userAdmin(status,name,frame,font,imagename,imagePath,left,right,bottom,top,framenum):
    
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
            
        cv2.putText(frame, "Frame num" + str(framenum), (0, 480), font,
                0.5, (255, 255, 255), 1)

        # sends Image and saves image to disk
        if(not os.path.exists(imagePath+"Admin/"+imagename+".jpg")):

            saveImage(imagePath+"Admin/",
                        imagename, frame)
            console_log.PipeLine_Ok("Saved Image to"+ "  "+str(imagePath + "Admin/" +imagename + ".jpg"))
            print("Saved Image to"+ "  "+str(imagePath + "Admin/" +imagename + ".jpg"))
            


 # User Grade Status
 # this is for Handling User Stats
def userUser(status,name,frame,font,imagename,imagePath,left,right,bottom,top,framenum):

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

    
    cv2.putText(frame, "Frame num" + str(framenum), (0, 480), font,
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
    
    # checks to see if image exsitis
    if(not os.path.exists(imagePath+"User/"+imagename+".jpg")):

        # sends Image and saves image to disk
        saveImage(imagePath+"User/",imagename, frame)

        console_log.PipeLine_Ok("Saved Image to"+ "  "+str(imagePath + "User/" +imagename + ".jpg"))
      
    #


# Handles Unwanted Usr Stats
def userUnwanted(status,name,frame,font,imagename,imagePath,left,right,bottom,top):
    
        cv2.rectangle(frame, (left, top),
                    (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top),
                    font, 0.5, (255, 255, 255), 1)
        
        console_log.Warning("not letting in" + name)

        # checks to see if image exsitis
        
        if(not os.path.exists(imagePath+"Unwanted/" + imagename + ".jpg")):

            # sends Image and saves image to disk
            saveImage(imagePath+"Unwanted/",
                        imagename, frame)
            console_log.PipeLine_Ok("Saved Image to"+ "  "+str(imagePath + "Unwanted/" +imagename + ".jpg"))
            
# Handles unKnown User
def userUnknown(opencvconfig,name,frame,font,imagePath,imagename,left,right,bottom,top,framenum):

        cv2.rectangle(frame, (left, top),
                    (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top),
                    font, 0.5, (255, 255, 255), 1)
                
        cv2.putText(frame, "Frame num" + str(framenum), (0, 480), font,
                    0.5, (255, 255, 255), 1)

        # Distance info
        cv2.putText(frame, opencvconfig['unreconizedPerson'], (0, 450),
                    font, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, name, (0, 470), font,
                    0.5, (255, 255, 255), 1)
        # checks to see if image exsitis
        if(not os.path.exists(str(imagePath) + "unknown/" +str(imagename) + ".jpg")):
            # sends Image and saves image to disk
            saveImage(imagePath+"unknown/",imagename, frame)
            console_log.PipeLine_Ok("Saved Image to"+ "  "+str(imagePath) + "unknown/" +str(imagename) + ".jpg")
           
                        
# User Groups 
def userGroup(frame,font,imagePath,imagename,left,right,bottom,top):
    
            cv2.rectangle(
                frame, (left, top), (right,
                                    bottom), (255, 0, 255), 2
            )
            cv2.putText(frame, "Group", (left, top),
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

            console_log.Warning("Letting in group")

            if(not os.path.exists(imagePath + "Group/" + imagename + ".jpg")):

                # sends Image and saves image to disk
                saveImage(imagePath + "Group/"+str(imagename) + ".jpg")
                
                console_log.PipeLine_Ok("Saved Image to"+ "  "+str(imagePath) + "Group/" +str(imagename) + ".jpg")
                
                
                    

'''
This is the Main Launcher for the SecuServe Program YaY!
This will Check to see if any of the MicroServices are Already running and will launch the services that arnt allready running
@author Nicholas Blackburn
'''

from datetime import datetime
from genericpath import exists
import os
import shutil
import smtplib
import subprocess
import prosessing.video as cvVideo
import multiprocessing
import pathlib
import logging
import configparser

# Allows Micro- Serivces to Runn on sperate threads to enable easy managemnet
opencv_face_thread=multiprocessing.Process(target=cvVideo.VideoProsessing().ProcessVideo)
#webServer_thead=threading.Thread(target=webServer.Start)

prefix = "[SecuServe-Launcher]  "
broken = "(Sad UwU Noises).... Im sorry Master but, I broke Stuff Again, Please Dont hate me..."
happy = str("(Happy UwU Noises)... Both Threads Started Yay! Master Loves me Now!~").encode('utf-8')


"""
Handles Sms Messaging for Thread Status and Errors
"""

# Sends Email to sms Gateway
def sendMessageToClient(logging,usrnumber,message):


    print("path of config"+str(pathlib.Path().absolute()) +"/src/prosessing/"+"Config.ini\n")
    # Reads Config
    config_object = configparser.ConfigParser()
    config_object.read(str(pathlib.Path().absolute()) +"/src/prosessing/"+"Config.ini")

    smsconfig = config_object['SMS']

    try:
        logging.info("starting to connect to server network")

        #Connects to gmail and sends hello ping
        server = smtplib.SMTP(smsconfig['smtpserver'], int(smsconfig['smtpport']))
        logging.info(server.ehlo())

        if(server.ehlo() is not None):
            server.starttls()
            server.login(smsconfig['gatwayemail'], smsconfig['gatewaypass'])
            server.sendmail(smsconfig['sendername'], str(usrnumber)+smsconfig['gatewayOutEmail'], str(message)+smsconfig['endingmessage'])
            logging.warn("Sent Email to"+usrnumber+smsconfig['gatewayOutEmail'])
            server.close()
            logging.info("Closed connection to email server email sent UWU")
            return
    except:
        logging.warning("Could not send email!!!!! maby check address?")
        return




"""
Main Function and thread of The whole Program
"""
def main():
    
    wasStarted = False
    print("SecuServe Starting UwU!....\n")

    print("path of config"+str(pathlib.Path().absolute()) +"/src/prosessing/"+"Config.ini\n")
    # Reads Config
    config_object = configparser.ConfigParser()
    config_object.read(str(pathlib.Path().absolute()) +"/src/prosessing/"+"Config.ini")
    #

    # Pipes config file to python
    logconfig = config_object['LOGGING']
    fileconfig = config_object['FILE']
    rootDirPath = fileconfig['rootDirPath']
    configPath = fileconfig['rootDirPath']+fileconfig['configPath']
    imagePath = fileconfig['rootDirPath'] + fileconfig['imagePath']
    imagePathusers = fileconfig['rootDirPath'] + fileconfig['imagePathusers']
    loggingPath = fileconfig['rootDirPath'] + fileconfig['loggingPath']
    smsconfig = config_object['SMS']

    logging.basicConfig(filename=loggingPath+logconfig['launcher'] + datetime.now(
    ).strftime("%Y_%m_%d-%I_%M_%S_%p_%s")+".log", level=logging.DEBUG)
    

    logging.debug("===================================================\n")
    logging.debug("+= Launcher Log UwU!  Heres My Output Down below =+\n")
    logging.debug("===================================================\n")

    logging.info(prefix + "Time to Begin setting up Miro service Treads! UwU\n")
    while True:

        
        
        if(not opencv_face_thread.is_alive()):
            wasStarted = True
            #sendMessageToClient(logging,smsconfig['userphonenum'],"Starting Opencv Thread")
            logging.info(prefix+"Starting Cv thread")
            opencv_face_thread.start()
        else:
                return

         
        if(not opencv_face_thread.is_alive() and wasStarted):
             #sendMessageToClient(logging,smsconfig['userphonenum'],"Thread Opencv Was Killed Unexpectinly Check Logs For more Info")
            
    

       
        


                



if __name__ == '__main__':
    main()
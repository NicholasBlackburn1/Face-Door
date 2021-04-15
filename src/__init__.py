"""
This is the Main Launcher for the SecuServe Program YaY!
This will Check to see if any of the MicroServices are Already running and will launch the services that arnt allready running
@author Nicholas Blackburn
"""
from configparser import ConfigParser
from datetime import datetime
import os
import shutil
import prosessing.video as cvVideo
import web.run as webServer
import threading 
import pathlib
import logging




print("SecuServe Starting UwU!")



# Allows Micro- Serivces to Runn on sperate threads to enable easy managemnet 
cv_thread =threading.Thread(target=cvVideo.VideoProsessing().ProcessVideo(), daemon=True)
webserver_thread = threading.Thread(target=webServer.StartWebServer(), daemon=True)

prefix = "[SecuServe-Launcher]  "
broken = "(Sad UwU Noises).... Im sorry Master but, I broke Stuff Again, Please Dont hate me..."
happy = "(Happy UwU Noises)... Both Threads Started Yay! Master Loves me Now... heheh"

# this allows the program to create all the file folders for the program
def CreateFolders(rootDirPath, configPath,imagePathusers, imagePath):
        if(not os.path.exists(rootDirPath)):
            os.makedirs(rootDirPath)
            logging.info("Creating Root Dir of Program")

            if(not os.path.exists(configPath)):
                os.makedirs(configPath)
                logging.info("Creating COnfig Dir of Program")
                shutil.copyfile(str(pathlib.Path().absolute(
                ))+"/src/prosessing/"+"Config.ini", configPath, follow_symlinks=True)

            if(not os.path.exists(imagePathusers)):
                os.makedirs(imagePathusers)
                logging.info("Creating Training Dir For users")

            if(not os.path.exists(imagePath)):
                os.makedirs(imagePath)
                logging.info("created Caputered Image Local")

            if(not os.path.exists(imagePath+"Admin/")):
                os.makedirs(imagePath+"Admin/")
                logging.info("created  Admin Image Local")

            if(not os.path.exists(imagePath+"User/")):
                os.makedirs(imagePath+"User/")
                logging.info("created  User Image Local")

            if(not os.path.exists(imagePath+"Unwanted/")):
                os.makedirs(imagePath+"Unwanted/")
                logging.info("created  Unwanted Image Local")

            if(not os.path.exists(imagePath+"Unwated/")):
                os.makedirs(imagePath+"Unwanted/")
                logging.info("created  Unwanted Image Local")

            if(not os.path.exists(imagePath+"Group/")):
                os.makedirs(imagePath+"Group/")
                logging.info("created  Group Image Local")

            if(not os.path.exists(imagePath+"unknown/")):
                os.makedirs(imagePath+"unknown/")
                logging.info("created  unknown Image Local")

            logging.warn("Created File Dir's")

        if(os.path.exists(rootDirPath)):
            logging.info("Paths created Skipping creating newOnes")

            if(os.path.exists(configPath)):
                logging.info("config local Exsitis")
                return

def Main():
    # Reads Config
    config_object = ConfigParser()
    config_object.read(str(pathlib.Path().absolute()) +
                           "prosessing/"+"Config.ini")

    # Pipes config file to python 
    logconfig = config_object['LOGGING']
    fileconfig = config_object['FILE']
    rootDirPath = fileconfig['rootDirPath']
    configPath = fileconfig['rootDirPath']+fileconfig['configPath']

    logging.basicConfig(filename=configPath+logconfig['launcher'] + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p_%s")+".log", level=logging.DEBUG)

    logging.debug("===================================================\n")
    logging.debug("+= Launcher Log UwU!  Heres My Output Down below =+\n")
    logging.debug("===================================================\n")

    logging.info(prefix+ "Master, Im creating the Folders for you to Store Important Info in UwU...")

    


    logging.info(prefix+ "Time to Begin setting up Miro service Treads! UwU\n")

    logging.info(prefix+ "Are there any Threads alive?"+" "+"Opencv"+" "+str(cv_thread.is_alive())+" "+ "WebServer?"+" "+ str(webserver_thread.isAlive())+"\n")
    
    if(not cv_thread.is_alive() and not webserver_thread.isAlive()):
        logging.warning(prefix+"Both Important Threads Not alive.... (Sad UwU noises) Time to Start them both")

        webserver_thread.start()
        cv_thread.start()
        logging.warning(prefix+"Both Important Threads Should be alive.... (Happy UwU noises)")
        
        if(not cv_thread.is_alive() or not webserver_thread.isAlive()):
            Exception(prefix+broken+" "+ "one of the threads Did not Start call the creator Please!")
    else:
        logging.info(prefix+" "+happy)




    
    

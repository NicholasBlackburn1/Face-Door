
'''
This is the Main Launcher for the SecuServe Program YaY!
This will Check to see if any of the MicroServices are Already running and will launch the services that arnt allready running
@author Nicholas Blackburn
'''

from datetime import datetime
import os
import shutil
import prosessing.video as cvVideo
import web.run as webServer
import threading
import pathlib
import logging
import configparser


prefix = "[SecuServe-Launcher]  "
broken = "(Sad UwU Noises).... Im sorry Master but, I broke Stuff Again, Please Dont hate me..."
happy = str("(Happy UwU Noises)... Both Threads Started Yay! Master Loves me Now!~").encode('utf-8')

"""
this allows the program to create all the file folders for the program
"""


def CreateFolders(rootDirPath, configPath, imagePathusers, imagePath):
    if(not os.path.exists(rootDirPath)):
        os.makedirs(rootDirPath)
        logging.info(prefix+"Creating Root Dir of Program")

        os.makedirs(configPath)
        logging.info(prefix+"Creating COnfig Dir of Program")
        shutil.copyfile(str(pathlib.Path().absolute(
         ))+"/src/prosessing/"+"Config.ini", configPath, follow_symlinks=True)

        os.makedirs(imagePathusers)
        logging.info(prefix+"Creating Training Dir For users")

        os.makedirs(imagePath)
        logging.info(prefix+"created Caputered Image Local")

        os.makedirs(imagePath+"Admin/")
        logging.info(prefix+"created  Admin Image Local")

    
        os.makedirs(imagePath+"User/")
        logging.info(prefix+"created  User Image Local")

        os.makedirs(imagePath+"Unwanted/")
        logging.info(prefix+"created  Unwanted Image Local")

      
        os.makedirs(imagePath+"Unwanted/")
        logging.info(prefix+"created  Unwanted Image Local")

        os.makedirs(imagePath+"Group/")
        logging.info(prefix+"created  Group Image Local")


        os.makedirs(imagePath+"unknown/")
        logging.info(prefix+"created  unknown Image Local")
        logging.warn(prefix+"Created File Dir's")
    else:
        logging.warn(prefix + "Folders are created time to go back to main function")
        return

"""
Main Function and thread of The whole Program
"""
def main():
    
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

    print("Creating folders")

    try:
        CreateFolders(rootDirPath, configPath, imagePathusers, imagePath)
    except:
        logging.error(Exception(prefix+"cannot create folders because of they are there!"))

    print("finished Creating Folders")

    logging.basicConfig(filename=configPath+logconfig['launcher'] + datetime.now(
    ).strftime("%Y_%m_%d-%I_%M_%S_%p_%s")+".log", level=logging.DEBUG)
    

    logging.debug("===================================================\n")
    logging.debug("+= Launcher Log UwU!  Heres My Output Down below =+\n")
    logging.debug("===================================================\n")

    logging.info(prefix + "Time to Begin setting up Miro service Treads! UwU\n")

    # Allows Micro- Serivces to Runn on sperate threads to enable easy managemnet



    logging.info(prefix + "Are there any Threads alive?"+" "+"Opencv"+" " +str(cv_thread.is_alive())+" " + "WebServer?"+" ")

            



main()

'''
This is the Main Launcher for the SecuServe Program YaY!
This will Check to see if any of the MicroServices are Already running and will launch the services that arnt allready running
@author Nicholas Blackburn
'''

from datetime import datetime
from genericpath import exists
import os
import shutil
import subprocess
import prosessing.video as cvVideo
#import web.run as webServer
import threading
import pathlib
import logging
import configparser


# Allows Micro- Serivces to Runn on sperate threads to enable easy managemnet
opencv_thread=threading.Thread(target=cvVideo.VideoProsessing().ProcessVideo)
#webServer_thead=threading.Thread(target=webServer.StartWeb)

prefix = "[SecuServe-Launcher]  "
broken = "(Sad UwU Noises).... Im sorry Master but, I broke Stuff Again, Please Dont hate me..."
happy = str("(Happy UwU Noises)... Both Threads Started Yay! Master Loves me Now!~").encode('utf-8')

"""
this allows the program to create all the file folders for the program
"""


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
    loggingPath = fileconfig['rootDirPath'] + fileconfig['loggingPath']


    logging.basicConfig(filename=loggingPath+logconfig['launcher'] + datetime.now(
    ).strftime("%Y_%m_%d-%I_%M_%S_%p_%s")+".log", level=logging.DEBUG)
    

    logging.debug("===================================================\n")
    logging.debug("+= Launcher Log UwU!  Heres My Output Down below =+\n")
    logging.debug("===================================================\n")

    logging.info(prefix + "Time to Begin setting up Miro service Treads! UwU\n")
    
    if(not opencv_thread.is_alive() and not webServer_thead.is_alive()):

        logging.info(prefix+"Starting webserver thread")
        #webServer_thead.start()
        logging.info(prefix+"Started webserver thread")

        logging.info(prefix+"Starting Cv thread")
        opencv_thread.start()
        logging.info(prefix+"Started Cv thread")


            



main()

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
from threading import Thread
import prosessing.video as cvVideo
import multiprocessing
import pathlib
import logging
import configparser
    # Import smtplib for the actual sending function
import smtplib
import cv2

# And imghdr to find the types of our images
import imghdr

# Here are the email package modules we'll need
from email.message import EmailMessage


# Allows Micro- Serivces to Runn on sperate threads to enable easy managem
#opencv_plate_thread=multiprocessing.Process(target=cvVideo.VideoProsessing().processPlate)
#webserver_thread = multiprocessing.Process(target= web.run.Start)
#webServer_thead=threading.Thread(target=webServer.Start)

prefix = "[SecuServe-Launcher]  "
broken = "(Sad UwU Noises).... Im sorry Master but, I broke Stuff Again, Please Dont hate me..."
happy = str("(Happy UwU Noises)... Both Threads Started Yay! Master Loves me Now!~").encode('utf-8')


"""
Main Function and thread of The whole Program
"""
def main():
    
    wasStarted = False
    print("SecuServe Starting UwU!....\n")

    print("===================================================\n")
    print("+= Launcher Log UwU!  Heres My Output Down below =+\n")
    print("===================================================\n")

    print(prefix + "Time to Begin setting up Miro service Treads! UwU\n")

    cvVideo.VideoProsessing().setsUpPipeLine() 
main()


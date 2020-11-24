"""
Simple data handler class for reeciving opencv data from publisher 
"""
#!/usr/bin/env python3
import logging
from shutil import copyfile
import app
import zmq


class Data(object):
        
   # returns name of user seen
    def getName(starter, message):
        if(starter == 'NAME'):
            return message['name']
        
    # returns amount of people seen 
    def getPeopleSeen(starter, message):
        if (starter == 'OWNER'):
            return message['ownerface']
        
    # returns the group of people sceen
    def getPersonsGroup(starter, message):
        if(starter == 'GROUP'):
            return message['group']
        
    # hopefully returns python picle
    def getImageFrame(starter, message):
        if(starter == 'IMAGE'):
           copyfile("/mnt/user/"+message['image'], app.Flask.static_folder+"/faces/"+message['image'])
           app.getLogger("IMAGE LOCAL PATH"+app.Flask.static_folder+"/faces/"+message['image'] )
           return  "static/faces/"+message['image']



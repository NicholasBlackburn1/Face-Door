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
    def getTotalSeen(starter, message):
        if (starter == "FACE" and int(message['face']) is not None):
            return int(message['face'])
        else:
            return int(0) 
        
         # returns amount of people seen 
    def getOwnerPeople(starter, message):
        if (starter == 'OWNER' and int(message['ownerface'] is not None)):
            return int(message['ownerface'])
        else: 
            return int(0)
        
    def getParentPeople(starter,message):
        if(starter == 'PARENT' and int(message['parentface'] is not None)):
            return int(message['parentface'])
        else:
            return int(0)
       
    def getUnknownPeople(starter,message):
        if (starter == 'UNKNOWN'and int(message['unknown'] is not None)):
            return int(message['unknown'])
        else:
            return int(0)
        
    # returns the group of people sceen
    def getPersonsGroup(starter, message):
        if(starter == 'GROUP' and int(message['group'] is not None)):
            return int(message['group'])
        else:
            return int(0)

    # hopefully returns python picle
    def getImageFrame(starter, message):
        if(starter == 'IMAGE' and message['image'] is not None):
           copyfile("/mnt/user/"+message['image'], "app/base/static/assets/faces/"+message['image'])
           return  "/static/assets/faces/"+message['image']
        else:
            return None


    # hopefully returns python picle
    def getParentImageFrame(starter, message):
        if(starter == 'IMAGE_PR' and message['image'] is not None):
           copyfile("/mnt/user/"+"Parent"+message['image'], "app/base/static/assets/faces/"+"Parent"+message['image'])
           return  "/static/assets/faces/"+"Parent"+message['image']
        else:
            return None


    # hopefully returns python picle
    def getUnknownImageFrame(starter, message):
        if(starter == 'IMAGE_UN' and message['image'] is not None):
           copyfile("/mnt/user/"+message['image'], "static/assets/faces/"+message['image'])
           return  "/static/assets/faces/"+message['image']
        else:
            return None
        
    def getFaceCompare(starter,message):
        if(starter== 'COMPARE' and message['compare']is not None):
            return int(message['compare'])
        else:
            return int(0)


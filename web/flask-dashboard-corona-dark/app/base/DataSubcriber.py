"""
Simple data handler class for reeciving opencv data from publisher 
"""
from distutils.file_util import copy_file
from os import write

from pycparser.c_ast import Return

import logging
from shutil import copyfile
import app
import zmq
import yaml
from run import socketio

class DataSubscriber(object):
        
   # returns name of user seen
    def getName(starter, message):
        if(starter == 'NAME'):
            return message['name']
        
    # returns amount of people seen 
    def getPeopleSeen(starter, message):
        if (starter == 'FACE'):
            return message['face']
        
    # returns the group of people sceen
    def getPersonsGroup(starter, message):
        if(starter == 'GROUP'):
            return message['group']
    
    def getownerSeen(starter, message):
        if(starter == 'OWNER'):
            i = 0
            if(i >= message['ownerface'] or i >0):
                    return None
            else:
                return  i +1 
        
    def getunknownSeen(starter, message):
        i =0
        
        if(starter=='UNKNOWN'):
            unknown = int(message['unknownface'])
            if(i >= unknown and i >0):
                i = i+1
                output = 0
                return output
            else:
                return i
        
    # hopefully returns python location
    def getImageFrame(starter, message):
        if(starter == 'IMAGE'):
          copy_file("/mnt/user/"+message['image'], "app/base/static/faces/"+message['image'])
          return "static/faces/"+message['image']
       
    def getimages(starter, message):
        if(starter == 'IMAGE'):
            output = message
            return str(output)
        
        
   
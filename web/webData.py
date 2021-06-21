"""
Data for sending data to the webpage
"""

import zmq 
import logging
from datetime import datetime
from shutil import copyfile
from DataSub import Data
import json
context = zmq.Context()
#  Socket to talk to server
logging.info("Connecting server…")
client = context.socket(zmq.SUB)
client.setsockopt_string(zmq.SUBSCRIBE, "")
client.connect("tcp://127.0.0.1:5000")

# Simply prints out the client object for proof of running
logging.info(client)

date  = bytes(datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p_%s"),'utf-8')

IMAGE = 'IMAGE'
GROUP = 'GROUP'
TIME = 'TIME'
NAME = 'NAME'
FACE = 'FACE'


while True:
    #frameobj = client.recv_pyobj()
    starter = client.recv_string()
    message = client.recv_json()
      
    if (starter == 'OWNER' and int(message['ownerface'] is not None)):
            print(int(message['ownerface']))
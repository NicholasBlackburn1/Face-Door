"""
Data for sending data to the webpage
"""

import zmq 
import logging
logging.basicConfig(filename='/mnt/user/webdata.log',  level=logging.DEBUG)

context = zmq.Context()
#  Socket to talk to server
logging.info("Connecting server…")
client = context.socket(zmq.SUB)
client.setsockopt_string(zmq.SUBSCRIBE, "")
client.connect("tcp://127.0.0.1:5000")

# Simply prints out the client object for proof of running
logging.info(client)
ownerimage = None
while True:
    message = client.recv()
  
    if(message == message.strip(b'owners')):
        ownerimage = str(message.strip(b'b'),'utf-8')
        print(ownerimage)
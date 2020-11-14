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

while True:
    message = client.recv()

    if(message == b"image"):
        print('test')
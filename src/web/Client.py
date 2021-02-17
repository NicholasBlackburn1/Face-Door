
"""
this file is for controlling the alarm and door with the raspi this is the simple client
Which references the opencv camera system. useing an Subscriber base tcp server and client 
 """

from os import pathsep
import zmq
import time
import smtplib
import Config
import logging
#import doorcontrol
import philipsControl
import ClientMessageHandler
logging.basicConfig(filename='/mnt/user/Client.log',  level=logging.DEBUG)

# setups pins on pi for use 
#doorcontrol.setup()

context = zmq.Context()
#  Socket to talk to server
logging.info("Connecting server…")
client = context.socket(zmq.SUB)
client.setsockopt_string(zmq.SUBSCRIBE, "")
client.connect("tcp://127.0.0.1:5000")

# Simply prints out the client object for proof of running
logging.info(client)
# Talks to google account and sends Email
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(Config.SMSGATWAYEMAIL, Config.SMSGATEWAYPASSWORD)

# sets up vars for using the project scope
name = Config.NAME
nick = Config.NICKSPHONE
ethans = Config.ETHANSPHONE

#bridge = Bridge(Config.HUE_IP)

logging.warning("Client Started")

# runs forever to wait to reseave
while True:
    starter = client.recv_string()
    message = client.recv_json()
    
    
    ClientMessageHandler.MessageHandler.sendSms(server,Config.NAME+"   "+)
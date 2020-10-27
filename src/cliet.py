
"""
this file is for controlling the alarm and door with the raspi this is the simple client
Which references the opencv camera system. useing an Subscriber base tcp server and client 
 """
 
import zmq
import time
import smtplib
import Config

context = zmq.Context()

#  Socket to talk to server
print("Connecting server…")
client = context.socket(zmq.SUB)
client.setsockopt_string(zmq.SUBSCRIBE, "")
client.connect("tcp://127.0.0.1:5000")

# Simply prints out the client object for proof of running 
print(client)

#Talks to google account and sends Email 
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(Config.SMSGATWAYEMAIL, Config.SMSGATEWAYPASSWORD)

# sets up vars for using the project scope
name = Config.NAME
nick = Config.NICKSPHONE
ethans = Config.ETHANSPHONE

# test's smtp server by sending message to the cell network
server.sendmail(name, nick and ethans, Config.NAME + " "+ "Test message"+ "" +"from your studio security system" + "  " + Config.ENDINGMESSAGE )
time.sleep(1)

# runs forever to wait to reseave
while True:
   message = client.recv()
   info = client.recv_string()

   if(message == b"starting"):
       
       server.sendmail(name, nick, Config.NAME + " "+"Starting" + "  " + Config.ENDINGMESSAGE)
        #doorcontrol.setup()
       time.sleep(10)  
       
   elif(message == b"owners"):
       server.sendmail(name, nick, Config.NAME + " "+ "Nick or Ethan"+ "" +"is at the Studio" + "  " + Config.ENDINGMESSAGE )
        #  doorcontrol.doorOpen()
        #  doorcontrol.alarmOff()
       time.sleep(10)
   elif(message == b"parents"):
       server.sendmail(name, nick, Config.NAME + " "+"Adults is at the Studio!"+ "  " +Config.ENDINGMESSAGE)
        #  doorcontrol.doorOpen()
        #  doorcontrol.alarmOff()
       time.sleep(10)
   elif(message == b"unknown"):
       server.sendmail(name,nick,Config.NAME + " " +" IS HERE! Sounding Alarm!"+ "  " +Config.ENDINGMESSAGE)
    #  doorcontrol.doorClose()
    #  doorcontrol.alarmOn()
       time.sleep(10)
   elif(message == b"group"):
       server.sendmail(name,nick,Config.NAME + " " +" A Group of people that ethier has an owner or and Parent in it IS HERE!"+ "  " +Config.ENDINGMESSAGE)
    #  doorcontrol.doorOpen()
    #  doorcontrol.alarmOff()
       time.sleep(10)
   else:
    #  doorcontrol.doorClose()
     #  doorcontrol.alarmOff()
       server.sendmail(name,nick,Config.NAME + " " +"Error as occured "+ "  " + Config.ENDINGMESSAGE)
       print(info)
       

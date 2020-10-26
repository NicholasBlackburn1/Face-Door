
"""
this file is for controlling the alarm and door with the raspi this is the simple client
Which references the opencv camera system.
 """
import zmq
import time
import smtplib
import Config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

context = zmq.Context()
#  Socket to talk to server
print("Connecting server…")
client = context.socket(zmq.SUB)
client.setsockopt_string(zmq.SUBSCRIBE, "")
client.connect("tcp://127.0.0.1:5000")
print(client)

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(Config.SMSGATWAYEMAIL, Config.SMSGATEWAYPASSWORD)
name = Config.NAME
nick = Config.NICKSPHONE
ethans = Config.ETHANSPHONE

while True:
   string = client.recv()

   if(string == b"starting"):
       server.sendmail(name, nick, Config.NAME + " "+"Starting" + "  " + Config.ENDINGMESSAGE)
       time.sleep(10)
     #  server.sendmail(name, ethans, string + " " + " is Starting" + Config.ENDINGMESSAGE )
        #  doorcontrol.doorOpen()
        #  doorcontrol.alarmOff()
       
   elif(string == b"owners"):
       server.sendmail(name, nick, Config.NAME + " "+ "Nick or Ethan"+ "" +"is at the Studio" + "  " + Config.ENDINGMESSAGE )
       #server.sendmail(name, ethans, string + " " + " IS HERE! Opeing Door!" +Config.ENDINGMESSAGE)
        #  doorcontrol.doorOpen()
        #  doorcontrol.alarmOff()
       time.sleep(10)
   elif(string == b"parents"):
       server.sendmail(name, nick, Config.NAME + " "+"Adults is at the Studio!"+ "  " +Config.ENDINGMESSAGE)
       #server.sendmail(name, ethans, string + " " + " IS HERE! Opeing Door!"+ Config.ENDINGMESSAGE)
        #  doorcontrol.doorOpen()
        #  doorcontrol.alarmOff()
       time.sleep(10)
   elif(string == b"unknown"):
       server.sendmail(name,nick,Config.NAME + " " +" IS HERE! Sounding Alarm!"+ "  " +Config.ENDINGMESSAGE)
       #server.sendmail(name,ethans,string+ " " +" IS HERE! Sounding Alarm!"+ Config.ENDINGMESSAGE)
    #  doorcontrol.doorClose()
    #  doorcontrol.alarmOn()
       
   else:
    #  doorcontrol.doorClose()
     #  doorcontrol.alarmOff()
       server.sendmail(name,nick,Config.NAME + " " +"Error as occured "+ "  " + Config.ENDINGMESSAGE)
       #server.sendmail(name,ethans,string+ " " +"Error as occured"+ Config.ENDINGMESSAGE)
       

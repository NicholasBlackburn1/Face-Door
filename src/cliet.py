
"""
this file is for controlling the alarm and door with the raspi this is the simple client
Which references the opencv camera system.
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
print(client)

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(str(Config.SMSGATWAYEMAIL)), (str(Config.SMSGATEWAYPASSWORD))
name = str(Config.NAME)
nick = str(Config.NICKSPHONE)
ethans = str(Config.ETHANSPHONE)

while True:
   string = client.recv()

   if(string == b"starting"):
       server.sendmail(name, nick, string +" " + "is Starting" + Config.ENDINGMESSAGE )
     #  server.sendmail(name, ethans, string + " " + " is Starting" + Config.ENDINGMESSAGE )
        #  doorcontrol.doorOpen()
        #  doorcontrol.alarmOff()
       time.sleep(10)
   elif(string == b"owners"):
       server.sendmail(name, nick, string +" " + " IS HERE! Opeing Door!"+ Config.ENDINGMESSAGE)
       #server.sendmail(name, ethans, string + " " + " IS HERE! Opeing Door!" +Config.ENDINGMESSAGE)
        #  doorcontrol.doorOpen()
        #  doorcontrol.alarmOff()
       time.sleep(10)
   elif(string == b"parents"):
       server.sendmail(name, nick, string +" " + " IS HERE! Opeing Door!"+ Config.ENDINGMESSAGE)
       #server.sendmail(name, ethans, string + " " + " IS HERE! Opeing Door!"+ Config.ENDINGMESSAGE)
        #  doorcontrol.doorOpen()
        #  doorcontrol.alarmOff()
       time.sleep(10)
   elif(string == b"unknown"):
       server.sendmail(name,nick,string + " " +" IS HERE! Sounding Alarm!"+ Config.ENDINGMESSAGE)
       #server.sendmail(name,ethans,string+ " " +" IS HERE! Sounding Alarm!"+ Config.ENDINGMESSAGE)
    #  doorcontrol.doorClose()
    #  doorcontrol.alarmOn()
       
   else:
    #  doorcontrol.doorClose()
     #  doorcontrol.alarmOff()
       server.sendmail(name,nick,string + " " +"Error as occured "+ Config.ENDINGMESSAGE)
       #server.sendmail(name,ethans,string+ " " +"Error as occured"+ Config.ENDINGMESSAGE)
       

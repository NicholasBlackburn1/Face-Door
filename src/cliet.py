import zmq
import time 
from notify_run import Notify
context = zmq.Context()
message = Notify
#  Socket to talk to server
print("Connecting server…")
client = context.socket(zmq.SUB)
client.setsockopt_string(zmq.SUBSCRIBE, "")
client.connect("tcp://127.0.0.1:5000")
print(client)
i = 0


while True:
   string = client.recv()
  
   if(string == b"starting"):
       print(string)
       time.sleep(10)
   elif(string == b"owners"):
       print(string)
       time.sleep(10)
   elif(string == b"parents"):
       print(string)
       time.sleep(10)
   elif(string == b"unknown"):
       print(string)
       time.sleep(10)
   elif(string ==b"none"):
       print(string)
       
import zmq
import time 
context = zmq.Context()

#  Socket to talk to server
print("Connecting server…")
client = context.socket(zmq.SUB)
client.setsockopt_string(zmq.SUBSCRIBE, "")
client.connect("tcp://127.0.0.1:5000")
print(client)
i = 0
while True:
   string = client.recv()
    #  Do some 'work'
   time.sleep(1)

   print(string)
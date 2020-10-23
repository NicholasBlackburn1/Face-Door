"""
Main Entrypoint for Starting Micro services 
"""
import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to Cv Service")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5000")

#  Do 10 requests, waiting each time for a response
for request in range(100):
    print("Sending request %s …" % request)
    socket.send(b"start_opencv")
    
    if input()== 'stop':
         socket.send(b"stop")

    #  Get the reply.
    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))
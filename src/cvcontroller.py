"""
Opencv Service Controller
Controls the open cv Service
"""

import zmq
import time
import video

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5000")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    if message == "start_opencv":
        video.videoCv()
    elif message == "stop_opencv":
        video.stop()
    #  Do some 'work'=
    time.sleep(30.5)
    socket.send(b"OpenCv Started")
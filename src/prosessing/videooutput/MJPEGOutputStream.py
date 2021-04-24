"""
this class is for Sending the video output to a Zmq Stream for webpage
"""

# run this program on each RPi to send a labelled image stream
import socket
import time
import imagezmq


class OutputStream():

    # sends Images from processed opencv output to zmq
    def SendProssedImages(self,ip,port,frame):
        # Accept connections on all tcp addresses, port 5555
        sender = imagezmq.ImageSender(connect_to='tcp://'+ip+':'+port, REQ_REP=False)

        rpi_name = socket.gethostname() # send RPi hostname with each image
        
        time.sleep(2.0)  # allow camera sensor to warm up
       
        sender.send_image(rpi_name, frame)
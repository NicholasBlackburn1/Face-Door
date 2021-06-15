from configparser import ConfigParser
import cv2
import pathlib

# Read config.ini file
config_object = ConfigParser()
config_object.read(str(pathlib.Path().absolute()) +
                    "/src/prosessing/"+"Config.ini")
opencvconfig = config_object['OPENCV']

gst_str = ("rtspsrc location={} latency={}  ! rtph264depay  ! nvv4l2decoder ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink".format(str(opencvconfig['Stream_intro']+opencvconfig['Stream_ip']+":"+opencvconfig['Stream_port']), 20, 720, 480))  
cap = cv2.VideoCapture(gst_str,cv2.CAP_GSTREAMER)
while True:
   
    frame = cap.read()
    print(frame)


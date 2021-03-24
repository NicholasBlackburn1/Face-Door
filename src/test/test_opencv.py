import cv2
import os 
 
        # TODO: Change this into the ipcamera Stream using the config.
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    
while True:    
    video_capture = cv2.VideoCapture('udpsrc port=5006 ! application/x-rtp, encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegparse ! jpegdec ! autovideosink', cv2.CAP_GSTREAMER)
                  
                # Display the resulting image
    cv2.imshow("Video", video_capture)
             
             
           
            
                # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
